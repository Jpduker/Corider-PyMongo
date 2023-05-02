## Docker:

To use Docker to run a Flask app, you will need to create a Dockerfile that specifies how to build your container. Here's an example Dockerfile:

```json
FROM python:3.9-alpine

WORKDIR /Corider-PyMongo

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD [ "python", "app.py" ]
```

This Dockerfile specifies the environment for building and running a Python Flask app with PyMongo. Here are the steps it follows:

1. It starts from a base image of Python 3.9 running on Alpine Linux, which is a lightweight distribution of Linux.
2. It sets the working directory inside the container to **`/Corider-PyMongo`**.
3. It copies the **`requirements.txt`** file to the container.
4. It installs the required Python packages from the **`requirements.txt`** file using pip.
5. It copies the rest of the files in the current directory to the container.
6. It exposes port 3000 to allow connections to the Flask app.
7. It sets the default command to run the Flask app using the command **`python app.py`**.

So, this Dockerfile creates a container that installs the required Python packages and runs a Flask app with PyMongo on port 3000.

### Building the container:

```json
docker build -t myflaskapp .
```

### Running the dockerized Flask app:

```json
docker run -p 3000:3000 myflaskapp
```

since we exposed port 3000 we need to map our port to docker’s 3000 port.

![Screenshot from 2023-05-02 19-33-57.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2a6ffd37-1cb3-46bf-9c56-3956dc53b356/Screenshot_from_2023-05-02_19-33-57.png)

## app.py

This is a Flask application that provides an API to perform CRUD operations on a MongoDB database. 

### Import Necessary Libraries:

```python
from flask import Flask, request,jsonify
from flask_restful import Api, Resource, reqparse
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
```

### Initialize Flask app and Create new instance of MongoDB Client:

```python
app = Flask(__name__)
app.config['MONGO_URI'] =" "# Update this with your own MongoDB URI
mongo = PyMongo(app)
db = mongo.db
api = Api(app)
```

### REST API

```python
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
```

- The **`home`** class defines a simple **`/`** endpoint that returns a hello world message.
- The **`Create`** class defines a **`/create`** endpoint that accepts a JSON payload via a POST request and inserts the data into the MongoDB **`users`** collection. The newly inserted document's ID is returned in the response.
- The **`Read`** class defines a **`/read`** endpoint that retrieves all the documents in the **`users`** collection and returns them in a JSON format.
- The **`Read_id`** class defines a **`/read-id/<string:id>`** endpoint that accepts a document ID as a parameter and retrieves the corresponding document from the **`users`** collection. If the document is found, it is returned in a JSON format; otherwise, an error message is returned.
- The **`Update`** class defines an **`/update/<string:id>`** endpoint that accepts a document ID as a parameter and a JSON payload via a PUT request. The payload contains the updated fields for the corresponding document, which are updated in the **`users`** collection. If the update is successful, a success message is returned; otherwise, an error message is returned.
- The **`Delete`** class defines a **`/delete/<string:id>`** endpoint that accepts a document ID as a parameter and deletes the corresponding document from the **`users`** collection. If the delete is successful, a success message is returned; otherwise, an error message is returned.

### Binding Resource URL:

```json
api.add_resource(home, '/')
api.add_resource(Create, '/create')
api.add_resource(Read, '/read')
api.add_resource(Read_id, '/read-id/<string:id>')
api.add_resource(Update, '/update/<string:id>')
api.add_resource(Delete, '/delete/<string:id>')
```

The **`api.add_resource()`** statements register each endpoint with the Flask app.

### Main method:

```python
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=3000)
```

Testing:

I have made use of postman to test out all the API endpoints and was sucessfully able to Create,Read,Update and Delete from the MongoDB database I created using MongoDB Atlas.

### Read User:

1. Open Postman and create a new request of type GET.
2. Enter the URL for the endpoint you want to test, e.g. **`[http://](http://127.0.0.1:3000/)127.0.0.1:3000/read`**.
3. Send the request and check the response in the "Body" tab. It should return a JSON object containing all the users present in the database if the request was successful.

![Screenshot from 2023-05-02 19-23-26.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/bd107ef6-379c-439a-bfb7-5c14c9119d68/Screenshot_from_2023-05-02_19-23-26.png)

### From the Localhost:

![Screenshot from 2023-05-02 19-21-33.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c6044ddc-ad33-40f8-b3e1-a674ee3beb00/Screenshot_from_2023-05-02_19-21-33.png)

### Read User(by id):

1. Open Postman and create a new request **`[http://](http://127.0.0.1:3000/)127.0.0.1:3000/read-id/644bc21958e221462949dd7d`**.
2. Set the HTTP method to GET.
3. Click on the Send button to send the request.
4. Postman will display the response from the server in the Response section, which should contain the user details if the user is found, or a message saying "User not found" if the user is not found.

![Screenshot from 2023-05-02 19-23-12.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9a143cb3-02cd-49f0-b98f-d1afb225e2d4/Screenshot_from_2023-05-02_19-23-12.png)

### Update User (by id):

1. Open Postman and create a new request of type PUT.
2. Enter the URL for the endpoint you want to test, e.g. **`http://127.0.0.1:3000/update/<string:id>`** where **`<id>`** is the ID of the user you want to update.
3. In the request body, select the "raw" format and choose "JSON" from the dropdown menu.
4. Enter the JSON object containing the updated user data, e.g. **`{"name": "John", "email": "john@example.com", "password": "newpassword"}`**.
5. Send the request and check the response in the "Body" tab. It should return a JSON object containing a "result" key with the message "User updated successfully" if the update was successful, or "User not found" if the user with the given ID does not exist in the database.

![Screenshot from 2023-05-02 19-24-59.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/deec3692-19e7-4b9c-a6e1-f0135f44665b/Screenshot_from_2023-05-02_19-24-59.png)

### Create User:

1. Open Postman and create a new request.
2. Set the request method to POST and enter the URL of your API endpoint, which should be **`http://127.0.0.1:3000/create`**.
3. Select the "Body" tab and choose "raw" as the input format. Set the content type to "JSON (application/json)".
4. In the request body, enter the user data in JSON format. For example:
    
    ```json
    
    {
      "name": "John Smith",
      "email": "john.smith@example.com",
      "password": "password123"
    }
    
    ```
    
5. Click the "Send" button to send the request to your API endpoint.
6. The response will be displayed in the "Body" tab of the response panel. It should contain a JSON object with a "result" field that says "User added successfully".

![create_.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/7ed91057-4af8-4c9f-9c8f-092fe1667f20/create_.png)

### Delete User( by id):

To evaluate the **`delete_user`** method in Postman, follow these steps:

1. Open Postman and create a new request.
2. Set the request method to "DELETE".
3. Enter the URL **`http://127.0.0.1:3000/delete/<string:id>`**, where **`id`** is the ID of the user you want to delete.
4. Click the "Send" button to send the request.
5. Check the response to see if the user was deleted successfully. The response will be in JSON format and will contain a message indicating whether the user was deleted or not.

![delete_.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/47450ea8-5d42-48be-a664-0dcf49718b70/delete_.png)

# MonogDB database: