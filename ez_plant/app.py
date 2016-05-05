from flask import Flask, jsonify, render_template, request
import os.path
from user import User
from plant import Plant
import sys

sys.path.append(os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')
    # Comment for github
    #return jsonify(username="shibi", email="shibi@gmail.com")
    # return('Hello World')

@app.route('/templates/<page_name>')
def angularPage(page_name):
    return render_template(page_name)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = User(data['email'], data['password'], data['firstName'], data['lastName'])
    user.save_to_database()

    print(data['email'])
    #print(data['userName'])
    print(data['password'])
    return jsonify(success="true")

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
