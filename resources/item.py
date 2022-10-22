from unicodedata import name
from flask_restful import Resource, reqparse
from models.items import ItemModle
from flask import jsonify

class ItemList(Resource):
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

    def get(self):
        items = ItemModle.get_items()
        result = []
        for item in items:
            result.append({
                'name': item.name,
                "price": item.price
            })
        return { "items": result }
            

    def post(self):
        data = ItemList.parser.parse_args()
        old = ItemModle.find_item_by_name(data["name"])
        if old:
            return { "message": f"item with this name already exisit."}
        new_item = ItemModle(data["name"], data["price"])
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

    def post(self):
        data = ItemList.parser.parse_args()
        item = ItemModle.find_item_by_name(data["name"])

        if item is None:
            return { "message": "item not found." }, 404
        
        try:
            ItemModle.update_by_item_name(data["name"], data["price"])
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

    def post(self):
        data = ItemList.parser.parse_args()
        item = ItemModle.find_item_by_name(data["name"])

        if item is None:
            return { "message": "item not found." }, 404
        
        try:
            ItemModle.delete_by_item_name(data["name"])
        except:
            return { "message": "an error occured." }, 500
        return { "message": "item successfully deleted." }