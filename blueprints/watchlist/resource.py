from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, nonadmin_required
from sqlalchemy import desc
from password_strength import PasswordPolicy
from datetime import datetime
from .model import Watchlists

blueprint_watchlist = Blueprint('watchlist', __name__)
api = Api(blueprint_watchlist)

class WatchlistsResources(Resource):
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    # @nonadmin_required
    # def get(self):
    #     parser =reqparse.RequestParser()
    #     parser.add_argument("p", type=int, location="args", default=1)
    #     parser.add_argument("rp", type=int, location="args", default=25)
    #     parser.add_argument("title", location="args")
    #     args = parser.parse_args()
        
    def post(self):
        parser =reqparse.RequestParser()
        parser.add_argument("movie_id", type=int, location="args")
        args = parser.parse_args()

        claims = get_jwt_claims()


        client = ClientList(args['client_key'], password_digest, args['status'])
        db.session.add(client)
        db.session.commit()
        app.logger.debug('DEBUG : %s', client)

