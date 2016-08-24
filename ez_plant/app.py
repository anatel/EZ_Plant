from flask import Flask, jsonify, render_template, request, redirect, url_for
import flask.ext.login as flask_login
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from ez_plant.hashing_handler import HashingHandler
import os.path
from user import User
from moisture_data import MoistureData
from plant import Plant
import sys
import json

sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = '3\xbb\xd8X\x07\x19\xad[\x1eB\xbb!\x8d\x9eES&\tf\x10\x19P\xac\x18'
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    if current_user.is_authenticated:
        plants = { 'plants': [] }
        if current_user.plants:
            for plant in current_user.plants:
                water_data_json = vars(plant.water_data)
                plant_json = vars(plant)
                plant_json['water_data'] = water_data_json
                plants['plants'].append(plant_json)

        return jsonify(is_logged_in=True, first_name=current_user.first_name, last_name=current_user.last_name, plants=plants)

    return jsonify({'is_logged_in': False})

@app.route('/templates/<page_name>')
def angularPage(page_name):
    return render_template(page_name)

@login_manager.user_loader
def load_user(username):
    user = User.get_from_database(username)
    if not user:
        return None

    return User(user['username'], user['password'], user['first_name'], user['last_name'], user['plants'])

@app.route('/login', methods=['POST'])
def login():
    hashing_handler = HashingHandler()
    data = request.get_json()
    user_doc = User.get_from_database(data['username'])
    if user_doc and hashing_handler.verify(data['password'], user_doc['password']):
        user = User(user_doc['username'], user_doc['password'], user_doc['first_name'], user_doc['last_name'], user_doc['plants'])
        login_user(user)
        return jsonify({'is_logged_in': True, 'first_name': current_user.first_name, 'last_name': current_user.last_name})

    return jsonify({'is_logged_in': False})

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
    user = User(data['username'], encrypted_password, data['firstName'], data['lastName'])
    user.save_to_database()

    return jsonify(result="success")

@app.route('/push_moisture_data', methods=['POST'])
def push_moisture_data():
    data = request.get_json()
    if 'plant_id' in data and 'moisture_value' in data:
        moisture_data = MoistureData(data['plant_id'], data['moisture_value'])
        moisture_data.save_to_database()
        return jsonify(result="success")

    return jsonify(result="error")

@flask_login.login_required
@app.route('/plant', methods=['GET', 'POST', 'DELETE'])
def plant():
    if request.method == 'POST':
        if not request.files:
            print("request files is empty")
        if 'file' not in request.files:
            print("no image sent.")

        file = request.files['file']
        print(file)
    #     data = request.get_json()
    #     if 'plant_name' in data and 'water_data' in data:
    #         current_user.add_plant(data['plant_name'], data['water_data'])
    #         return jsonify(result="success")
    #
    #     return jsonify(result="error")
    # elif request.method == 'GET':
    #     plant = current_user.get_plant(request.args.get('plant_id'))
    #     if plant:
    #         return plant
    #
    #     return jsonify(result="error")
    # else:
    #     current_user.delete_plant(int(request.args.get('plant_id')))
    #     return jsonify(result="success")

@app.route('/get_config', methods=['GET'])
def get_watering_config():
    user_doc = User.get_from_database(request.args.get('username'))
    user = User(user_doc['username'], user_doc['password'], user_doc['first_name'], user_doc['last_name'], user_doc['plants'])
    plants = { 'plants': [] }
    if user.plants:
        for plant in user.plants:
            water_data_json = vars(plant.water_data)
            plant_json = {}
            plant_json['water_mode'] = water_data_json['water_mode']
            plant_json['low_threshold'] = water_data_json['low_threshold']
            plants['plants'].append(plant_json)

    return jsonify(plants)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
