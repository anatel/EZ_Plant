"""
Main flask application
"""
import sys
import json
import glob
import os.path
from flask import Flask, jsonify, render_template, request
import flask.ext.login as flask_login
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from ez_plant.hashing_handler import HashingHandler
from ez_plant.user import User
from ez_plant.moisture_data import MoistureData
from ez_plant.plant_controller import PlantController

sys.path.append(os.path.dirname(__file__))
PLANT_IMAGES_FOLDER = 'static/plant_images'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             PLANT_IMAGES_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '3\xbb\xd8X\x07\x19\xad[\x1eB\xbb!\x8d\x9eES&\tf\x10\x19P\xac\x18'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    if current_user.is_authenticated:
        return jsonify(is_logged_in=True, first_name=current_user.first_name,
                       last_name=current_user.last_name)

    return jsonify(is_logged_in=False)


@app.route('/templates/<page_name>')
def angularPage(page_name):
    return render_template(page_name)


@login_manager.user_loader
def load_user(username):
    user = User.get_from_database(username)
    if not user:
        return None

    return User(user['username'], user['password'], user['first_name'],
                user['last_name'], user['plants'])


@app.route('/login', methods=['POST'])
def login():
    hashing_handler = HashingHandler()
    data = request.get_json()
    user_doc = User.get_from_database(data['username'])
    if user_doc and hashing_handler.verify(data['password'], user_doc['password']):
        user = User(user_doc['username'], user_doc['password'], user_doc['first_name'], user_doc['last_name'], user_doc['plants'])
        login_user(user)
        return jsonify(is_logged_in=True, first_name=current_user.first_name,
                       last_name=current_user.last_name)

    return jsonify(is_logged_in=False)


@flask_login.login_required
@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'logged_out': True})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashing_handler = HashingHandler()
    encrypted_password = hashing_handler.encrypt(data['password'])
    user = User(data['username'], encrypted_password, data['firstName'],
                data['lastName'])
    user.save_to_database()
    login_user(user)

    return jsonify(result="success", is_logged_in=True,
                   first_name=current_user.first_name,
                   last_name=current_user.last_name)


@flask_login.login_required
@app.route('/plants', methods=['GET', 'POST', 'DELETE'])
def plant():
    plant_controller = PlantController(current_user)
    if request.method == 'POST':
        image_file = None
        if request.files:
            if 'file' in request.files:
                image_file = request.files['file']

        image_dir = None if image_file is None else PLANT_IMAGES_FOLDER
        image_type = None if image_file is None else image_file.filename.rsplit('.', 1)[1]

        if 'plant_id' in request.form:
            new_plant = plant_controller.update_plant(
                        request.form['plant_id'],
                        request.form['moisture_sensor_port'],
                        request.form['water_pump_port'],
                        request.form['plant_type'],
                        request.form['name'],
                        json.loads(request.form['water_data']),
                        image_dir, image_type)
        else:
            new_plant = plant_controller.create_plant(
                        request.form['moisture_sensor_port'],
                        request.form['water_pump_port'],
                        request.form['plant_type'],
                        request.form['name'],
                        json.loads(request.form['water_data']),
                        image_dir, image_type)

        if image_dir:
            for filename in glob.iglob('%s/*' % (app.config['UPLOAD_FOLDER'])):
                if new_plant['plant_id'] in filename:
                    os.remove(filename)

            image_filename = new_plant['image_url'].rsplit('/', 1)[1]
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        return jsonify(result="success", plant=new_plant)
    elif request.method == 'GET':
        return jsonify(plant_controller.get_plants())

    else:
        if request.args.get('plant_id'):
            plant_to_delete = current_user.get_plant(
                              request.args.get('plant_id'))
            if plant_to_delete.image_url:
                image_to_delete = plant_to_delete.image_url.rsplit('/', 1)[1]
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                          image_to_delete))

            plant_controller.delete_plant(request.args.get('plant_id'))
            return jsonify(result="success")

        return jsonify(result="error")


@flask_login.login_required
@app.route('/get_free_ports', methods=['GET'])
def get_free_ports():
    free_moisture_ports = current_user.get_free_ports('moisture')
    free_water_pump_ports = current_user.get_free_ports('water_pump')
    return jsonify(free_moisture_ports=free_moisture_ports,
                   free_water_pump_ports=free_water_pump_ports)


@app.route('/get_config', methods=['GET'])
def get_watering_config():
    user_doc = User.get_from_database(request.args.get('username'))
    user = User(user_doc['username'], user_doc['password'],
                user_doc['first_name'], user_doc['last_name'],
                user_doc['plants'])
    plants = {'plants': []}
    if user.plants:
        for plant in user.plants:
            water_data_json = vars(plant.water_data)
            plant_json = {}
            plant_json['water_mode'] = water_data_json['water_mode']
            plant_json['low_threshold'] = water_data_json['low_threshold']
            plants['plants'].append(plant_json)

    return jsonify(plants)


@app.route('/push_moisture_data', methods=['POST'])
def push_moisture_data():
    if 'username' in request.args and 'plant_id' in request.args and 'moisture' in request.args:
        moisture_data = MoistureData(request.args.get('username'),
                                     request.args.get('plant_id'),
                                     request.args.get('moisture'))
        moisture_data.save_to_database()
        return jsonify(result="success")

    return jsonify(result="error")


@flask_login.login_required
@app.route('/get_plant_stats', methods=['GET'])
def get_stats():
    plant_controller = PlantController(current_user)
    if 'plant_id' not in request.args:
        return jsonify(result="error")

    plant_stats = plant_controller.get_plant_stats(request.args.get('plant_id'))

    return jsonify(stats=plant_stats, result="success")

@flask_login.login_required
@app.route('/water_now', methods=['GET', 'POST'])
def water_now():
    plant_controller = PlantController(current_user)
    if request.method == 'POST':
        if 'plant_id' not in request.args:
            return jsonify(result="error")

        plant_controller.set_water_now(request.args.get('plant_id'))
        return jsonify(result="success")
    else:
        return jsonify(plant_controller.get_water_now_data(), result="success")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
