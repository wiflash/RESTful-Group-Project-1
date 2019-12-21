from blueprints import db
from flask_restful import fields
import datetime

class Movies():
    response_fields={
        'movie_id': fields.Integer,
        'judul': fields.String,
        'sinopsis': fields.String,
        # 'genres': movie['genres'],
        'genres': fields.List,
        'tanggal_rilis': fields.datetime,
        'status_rilis': fields.String,
        'durasi': fields.Integer,
        'rating': fields.Float
    }