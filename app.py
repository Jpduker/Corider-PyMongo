from flask import Flask, request,jsonify
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['MONGO_URI'] =" "# Update this with your own MongoDB URI
mongo = PyMongo(app)
db = mongo.db
api = Api(app)


class home(Resource):
    def get(self):
        return {'message':'hello world'}

class Create(Resource):
    def post(self):
        data = request.get_json()
        result = db.users.insert_one(data)
        return {'id': str(result.inserted_id)}

import logging
logging.basicConfig(level=logging.DEBUG)

class Read(Resource):
    def get(self):
        users = db.users.find()
        output = []
        for user in users:
            output.append({'id': str(user['_id']), 'name': user['name'], 'email': user['email'], 'password': user['password']})
        return jsonify({'result': output})
    
class Read_id(Resource):
    
    def get(self, id):
        print(id)
        result = db.users.find_one({'_id': ObjectId(id)})
        print(result)
        if result:
            result['_id'] = str(result['_id'])
            return result
        else:
            return {'error': 'Not found'}, 404


class Update(Resource):
    def put(self, id):
        data = request.get_json()
        data = request.get_json()
        result = db.users.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count == 1:
            return {'message': 'Updated successfully'}
        else:
            return {'error': 'Not found'}, 404

class Delete(Resource):
    def delete(self, id):
        result = db.users.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return {'message': 'Deleted successfully'}
        else:
            return {'error': 'Not found'}, 404

api.add_resource(home, '/')
api.add_resource(Create, '/create')
api.add_resource(Read, '/read')
api.add_resource(Read_id, '/read-id/<string:id>')
api.add_resource(Update, '/update/<string:id>')
api.add_resource(Delete, '/delete/<string:id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=3000)


