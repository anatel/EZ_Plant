from flask import Flask, jsonify, render_template, request, redirect, url_for
import flask.ext.login as flask_login
from flask.ext.login import LoginManager, login_user, logout_user
from ez_plant.hashing_handler import HashingHandler
import os.path
from user import User
from moisture_data import MoistureData
from plant import Plant
import sys

sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = '3\xbb\xd8X\x07\x19\xad[\x1eB\xbb!\x8d\x9eES&\tf\x10\x19P\xac\x18'
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/get_user_data')
def get_user_data():
    if flask_login.current_user.is_authenticated:
        return jsonify({'is_logged_in': True, 'first_name': flask_login.current_user.first_name, 'last_name': flask_login.current_user.last_name})

    return jsonify({'is_logged_in': False})

@app.route('/templates/<page_name>')
def angularPage(page_name):
    return render_template(page_name)

@login_manager.user_loader
def load_user(username):
    user = User.get_from_database(username)
    if not user:
        return None

    return User(user['username'], user['password'], user['first_name'], user['last_name'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    hashing_handler = HashingHandler()
    data = request.get_json()
    user_doc = User.get_from_database(data['username'])
    if user_doc and hashing_handler.verify(data['password'], user_doc['password']):
        user = User(user_doc['username'], user_doc['password'], user_doc['first_name'], user_doc['last_name'])
        login_user(user)
        return jsonify({'is_logged_in': True, 'first_name': flask_login.current_user.first_name, 'last_name': flask_login.current_user.last_name})

    return jsonify({'is_logged_in': False})


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.username

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'logged_out': True})
    # return redirect(url_for('login'))

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
    print(data['moisture_value'])
    print(data['plant_id'])
    moisture_data = MoistureData(data['plant_id'], data['moisture_value'])
    moisture_data.save_to_database()
    return jsonify(success="true")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
