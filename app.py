from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

# GET all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = mongo.db.users.find()
    output = []
    for user in users:
        output.append({'id': str(user['_id']), 'name': user['name'], 'email': user['email'], 'password': user['password']})
    return jsonify({'result': output})

# GET user by id
@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        output = {'id': str(user['_id']), 'name': user['name'], 'email': user['email'], 'password': user['password']}
    else:
        output = 'User not found'
    return jsonify({'result': output})

# POST a new user
@app.route('/users', methods=['POST'])
def add_user():
    user = {'name': request.json['name'], 'email': request.json['email'], 'password': request.json['password']}
    mongo.db.users.insert_one(user)
    return jsonify({'result': 'User added successfully'})

# PUT (update) user by id
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {'name': request.json['name'], 'email': request.json['email'], 'password': request.json['password']}})
        output = 'User updated successfully'
    else:
        output = 'User not found'
    return jsonify({'result': output})

# DELETE user by id
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        output = 'User deleted successfully'
    else:
        output = 'User not found'
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(debug=True)
