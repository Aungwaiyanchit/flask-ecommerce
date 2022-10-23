import os
from flask_restful import Api
from flask import Flask
from security import authenticate, identity
from flask_jwt import JWT
from flask_uuid import FlaskUUID

from resources.user import UserRegister
from resources.item import DeleteItem, ItemList, UpdateItem, NewItem, GetItemByName
from resources.store import NewStore, GetStoreByName, StoreLists, DeleteStore


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

flask_uuid = FlaskUUID()
flask_uuid.init_app(app)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'aSBsb3ZlIGthcmluYQ=='
api = Api(app)

jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_table():
    db.create_all()

#endpoint for auth
api.add_resource(UserRegister, "/register")

#endpoint for items
api.add_resource(ItemList, "/items/all")
api.add_resource(GetItemByName, "/items/search")
api.add_resource(NewItem, "/items/create")
api.add_resource(DeleteItem, "/items/delete")
api.add_resource(UpdateItem, "/items/update")

#endpoint for stores
api.add_resource(StoreLists, "/stores/all")
api.add_resource(GetStoreByName, "/stores/search")
api.add_resource(NewStore, "/stores/create")
api.add_resource(DeleteStore, "/stores/delete")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000)
