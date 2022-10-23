from flask_restful import Resource, reqparse
from models.items import ItemModel
from flask import request
from flask_jwt import jwt_required

class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.get_items()
        return {"items" : [ item.json() for item in items ]}
            


class GetItemByName(Resource):
    @jwt_required()
    def post(self):
        name = request.get_json()["name"]
        item = ItemModel.find_item_by_name(name)
        if item is not None:
            return item.json()
        return { "message": "not found" }, 404

class NewItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        help="name cannot be empty"
    )
    parser.add_argument(
        'price',
        type=float,
        help="name cannot be empty"
    )
    parser.add_argument(
        'store_id',
        type=float,
        help="name cannot be empty"
    )
    @jwt_required()
    def post(self):
        data = NewItem.parser.parse_args()
        old = ItemModel.find_item_by_name(data["name"])
        if old:
            return { "message": f"item with this name already exisit."}
        new_item = ItemModel(data["name"], data["price"], data["store_id"])
        try:
            new_item.save_to_db();
        except:
            return { "message": "an error occured"}, 500
        return { "message": "item successfully added." }, 201

class UpdateItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        help="name cannot be empty"
    )
    parser.add_argument(
        'price',
        type=float,
        help="price cannot be empty"
    )
    parser.add_argument(
        'store_id',
        type=float,
        help="name cannot be empty"
    )

    @jwt_required()
    def post(self):
        data = UpdateItem.parser.parse_args()
        item = ItemModel.find_item_by_name(data["name"])

        if item is None:
            return { "message": "item not found." }, 404
        
        try:
            ItemModel.update_by_item_name(data["name"], data["price"], data["store_id"])
        except:
            return { "message": "an error occured." }, 500
        return { "message": "item successfully updated." }

class DeleteItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        help="name cannot be empty"
    )

    @jwt_required()
    def post(self):
        data = DeleteItem.parser.parse_args()
        item = ItemModel.find_item_by_name(data["name"])

        if item is None:
            return { "message": "item not found." }, 404
        
        try:
            ItemModel.delete_by_item_name(data["name"])
        except:
            return { "message": "an error occured." }, 500
        return { "message": "item successfully deleted." }