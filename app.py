from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
app.config["MONGO_DBNAME"] = "mydatabase"



print(app.config["MONGO_URI"])
mongo = PyMongo(app)
db = mongo.db

#route for home page and return a json response
@app.route('/',methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to my API'})


# GET all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = db.users.find()
    output = []
    for user in users:
        output.append({'id': str(user['_id']), 'name': user['name'], 'email': user['email'], 'password': user['password']})
    return jsonify({'result': output})

# GET user by id
@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    if user:
        output = {'id': str(user['_id']), 'name': user['name'], 'email': user['email'], 'password': user['password']}
    else:
        output = 'User not found'
    return jsonify({'result': output})
#test
@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        db.collection_names()
        return jsonify({'message': 'Successfully connected to MongoDB'})
    except Exception as e:
        return jsonify({'message': 'Could not connect to MongoDB', 'error': str(e)})

# POST a new user
@app.route('/users', methods=['POST'])
def add_user():
    user = {'name': request.json['name'], 'email': request.json['email'], 'password': request.json['password']}
    db.users.insert_one(user)
    return jsonify({'result': 'User added successfully'})

# PUT (update) user by id
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    if user:
        db.users.update_one({'_id': ObjectId(id)}, {'$set': {'name': request.json['name'], 'email': request.json['email'], 'password': request.json['password']}})
        output = 'User updated successfully'
    else:
        output = 'User not found'
    return jsonify({'result': output})

# DELETE user by id
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    if user:
        db.users.delete_one({'_id': ObjectId(id)})
        output = 'User deleted successfully'
    else:
        output = 'User not found'
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(debug=True)