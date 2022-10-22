import os
from flask_restful import Api
from flask import Flask
from security import authenticate, identity
from flask_jwt import JWT

from resources.user import UserRegister
from resources.item import DeleteItem, ItemList, UpdateItem



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'aSBsb3ZlIGthcmluYQ=='
api = Api(app)

jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(UserRegister, "/register")
api.add_resource(ItemList, "/items")
api.add_resource(DeleteItem, "/items/delete")
api.add_resource(UpdateItem, "/items/update")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000)
