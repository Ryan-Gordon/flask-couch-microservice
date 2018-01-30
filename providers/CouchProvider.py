import requests
import couchdb
import os
import flask
import bcrypt
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pass'
COUCHDB_URL = 'http://'+ADMIN_USERNAME+':'+ADMIN_PASSWORD+'@'+os.environ['SERVER_URL']

couch = couchdb.Server(COUCHDB_URL)
class CouchProvider(object):
    def __init__(self):
        self.hashed = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf8'), bcrypt.gensalt())
        
    def create_product(self,payload):
        # Step 1; Check if the auth header has been provided
        if 'Authorization' not in flask.request.headers:
            return {"error": "Not correctly authorized"}, 401
        # Step 2; Check the password provided by the user. (Maybe be better to provide the hash)
        if bcrypt.hashpw(flask.request.authorization.password.encode('utf8'), self.hashed) == self.hashed:
            print(os.environ['SERVER_URL'])
            couch = couchdb.Server(os.environ['SERVER_URL'])
            db = couch['products']
            if payload['_id'] in db:
                return {"error":"Found product with existing ID"}, 409
            else:
                db.save(payload)
                return payload,201
    def read_product(self, prod_id) -> str:
        db = couch['products']
        if(prod_id in db):
            product = db[prod_id]
            return product, 200
        else:
            return {"error": "Product not found"}, 400
    def update_product(self,payload):
        # Step 1; Check if the auth header has been provided
        if 'Authorization' not in flask.request.headers:
            return {"error": "Not correctly authorized"}, 401
        # Step 2; Check the password provided by the user. (Maybe be better to provide the hash)
        if bcrypt.hashpw(flask.request.authorization.password.encode('utf8'), self.hashed) == self.hashed:
            couch = couchdb.Server('http://'+os.environ['ADMIN_USERNAME']+':'+flask.request.authorization.password+'@'+os.environ['SERVER_URL'])
            db = couch['products'] # Select our db
            if payload['_id'] in db: # Check if product exists in DB
                print("Found a product in DB with this _id")
                doc = db[payload['_id']]
                payload['_rev'] = doc['_rev'] # Add the docs _rev prop to the payload or a conflict will occur
                db.save(payload) # Save the new details
                return {"message": "Success"}, 201
            else:
                #Product not found 
                return {"error": "Product not found"}, 409 
        else:
            # Reaching here means the provided password was not valid
            print("It does not match")
            return {"error": "Not correctly authorized"}, 409
    def delete_product(self,id):
        # Step 1; Check if the auth header has been provided
        if 'Authorization' not in flask.request.headers:
            return {"error": "Not correctly authorized"}, 401
        # Step 2; Check the password provided by the user. (Maybe be better to provide the hash)
        if bcrypt.hashpw(flask.request.authorization.password.encode('utf8'), self.hashed) == self.hashed:
            couch = couchdb.Server(os.environ['SERVER_URL'])
            print("It matches")
            try:
                db = couch['products']
                prod_to_delete = db[id]
                
                db.delete(prod_to_delete) 
                return {"message": "Success"}, 200
            except:
                return {"error": "Product not found"}, 400

        else:
            # Reaching here means the provided password was not valid
            print("It does not match")
            return {"error": "Not correctly authorized: Wrong password. Password provided :"+flask.request.headers['Authorization']}, 409
        