from flask_restful import Resource, reqparse
from models.store  import StoreModel
from flask_jwt import jwt_required


class StoreLists(Resource):
    jwt_required()
    def get(self):
        stores = StoreModel.get_all_stores()
        print(stores)
        return { "stores": [ store.json() for store in stores ]}

class GetStoreByName(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        help="store name required."
    )

    jwt_required()
    def post(self):
        data = GetStoreByName.parser.parse_args()

        store = StoreModel.find_by_store_name(data["name"])
        if store is None:
            return { "message": "store name can't found." }, 404
        return store.json()

class NewStore(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        help="store name field is required."
    )

    jwt_required()
    def post(self):
        data = NewStore.parser.parse_args()

        old_store = StoreModel.find_by_store_name(data["name"])
        if old_store:
            return { "message": "store name is already exists." },  409
        
        new_store = StoreModel(data["name"])
        try:
            new_store.save_to_db()
        except:
            return { "message": "an error occured " }
        return { "message": "store sucessfully created." }, 201

class DeleteStore(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        help="name cannot be empty"
    )

    @jwt_required()
    def post(self):
        data = DeleteStore.parser.parse_args()
        item = StoreModel.find_by_store_name(data["name"])

        if item is None:
            return { "message": "store not found." }, 404
        
        try:
            StoreModel.delete_by_store_name(data["name"])
        except:
            return { "message": "an error occured." }, 500
        return { "message": "store successfully deleted." }