from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token
from blueprints.user.model import *
import hashlib

blueprint_auth = Blueprint("auth", __name__)
api = Api(blueprint_auth)

class CreateTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="args", required=True)
        parser.add_argument("password", location="args", required=True)
        args = parser.parse_args()
        password = hashlib.md5(args["password"].encode()).hexdigest()
        if args["username"] == "admin" and args["password"] == "W@wew123":
            user_claims_data = {}
            user_claims_data["is_admin"] = True
        else:
            qry = Users.query.filter_by(username=args["username"])
            qry = qry.filter_by(password=password)
            qry = qry.filter_by(status=True).first()
            if qry is None:
                return {"status": "UNAUTHORIZED", "message": "Invalid username or password"}, 401, {"Content-Type": "application/json"}
            user_claims_data = marshal(qry, Users.jwt_claim_fields)
            user_claims_data["is_admin"] = False
        token = create_access_token(identity=args["username"], user_claims=user_claims_data)
        return {"token": token, "message": "Token is successfully created"}, 200, {"Content-Type": "application/json"}

api.add_resource(CreateTokenResources, "")