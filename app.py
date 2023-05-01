from flask import Flask
from flask_restful import Api
import os
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource

app = Flask(__name__)
api = Api(app)

from pymongo import MongoClient

# Replace the connection string with your own
client = MongoClient(os.getenv('MONGO_URI'))

# Replace "mydatabase" with the name of your database
db = client.mydatabase


class Create(Resource):
    def post(self):
        data = request.get_json()
        result = db.mycollection.insert_one(data)
        return {'id': str(result.inserted_id)}

class Read(Resource):
    def get(self, id):
        result = db.mycollection.find_one({'_id': ObjectId(id)})
        if result:
            result['_id'] = str(result['_id'])
            return result
        else:
            return {'error': 'Not found'}, 404

class Update(Resource):
    def put(self, id):
        data = request.get_json()
        result = db.mycollection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.modified_count == 1:
            return {'message': 'Updated successfully'}
        else:
            return {'error': 'Not found'}, 404
        
class Delete(Resource):
    def delete(self, id):
        result = db.mycollection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return {'message': 'Deleted successfully'}
        else:
            return {'error': 'Not found'}, 404
            
api.add_resource(Create, '/create')
api.add_resource(Read, '/read/string:id')
api.add_resource(Update, '/update/string:id')
api.add_resource(Delete, '/delete/string:id')


if __name__ == '__main__':
    app.run(debug=True)