from models.user import UserModel
from flask_restful import Resource, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        help="username can't be empty."
    )
    parser.add_argument(
        'password',
        type=str,
        help="password can't be empty."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        old_user = UserModel.find_user_by_username(data['username'])
        if old_user:
            return { "message": f"username already exists." }, 409
        
        user = UserModel(data["username"], data["password"])
        try:
            user.save_to_db()
        except: 
            return { "message": "an error occured while creating user." }, 500
        return {
            "message": "user register successfully."
        }
