from flask import Flask, jsonify, render_template, request
import os.path
from user import User
from moisture_data import MoistureData
from plant import Plant
import sys

sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/templates/<page_name>')
def angularPage(page_name):
    return render_template(page_name)

@app.route('/login', methods=['POST']) #TODO: build authentication
def login():
    data = request.get_json()
    username = data['username'];
    password = data['password'];

    return jsonify(result="success")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(data['username'], data['password'], data['firstName'], data['lastName'])
    user.save_to_database()

    print(data['username'])
    #print(data['userName'])
    print(data['password'])
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
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
