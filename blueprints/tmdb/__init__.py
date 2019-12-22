import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import json
from datetime import datetime
from blueprints import db, admin_required, nonadmin_required
from blueprints import db, app
bp_tmdb = Blueprint('tmdb', __name__)
api = Api(bp_tmdb)

class PublicGetTMDB(Resource):
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    def get(self, movie_id):
        rq = requests.get(self.host + '/movie/' + str(movie_id), params={'api_key':self.api_key})
        movie = rq.json()

        if "status_code" in movie:
            return {'message': "ID MOVIE NOT FOUND"}, 404
        genre_list=[]
        genre = movie['genres']
        for i in genre:
            genre_list.append(i['name'])
        hasil = {
            'movie_id': movie['id'],
            'judul': movie['title'],
            'sinopsis': movie['overview'],
            'genres': genre_list,
            'tanggal_rilis': movie['release_date'],
            'status_rilis': movie['status'],
            'durasi': movie['runtime'],
            'rating': movie['vote_average']
        }
        return hasil, 200
            

class PublicGetUpcoming(Resource):
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    def __init__(self):
        self.selection = "upcoming"

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('region', type=str, location='args', default='ID')
        args = parser.parse_args()
        param_data = {
            'api_key':self.api_key,
            'page':args['p'],
            'region':args['region']
        }
        rq = requests.get(self.host + '/movie/{}'.format(self.selection), params=param_data)
        rq_movies = rq.json()['results']
        page = rq.json()['page']
        total_page = rq.json()['total_pages']
        movies = []
        for each_movie in rq_movies:
            rq = requests.get(self.host + '/movie/' + str(each_movie['id']), params={'api_key':self.api_key})
            movie = rq.json()
            genre_list=[]
            genres = movie['genres']
            for each_genre in genres:
                genre_list.append(each_genre['name'])
            
            hasil = {
                'movie_id': each_movie['id'],
                'judul': each_movie['title'],
                'sinopsis': each_movie['overview'],
                'genres': genre_list,
                'tanggal_rilis': each_movie['release_date'],
                'durasi': movie['runtime'],
                'rating': each_movie['vote_average']
            }
            movies.append(hasil)
        return {"halaman":page, "total_halaman":total_page, "per_halaman":20, "hasil":movies}, 200


class PublicGetNowplaying(PublicGetUpcoming):
    def __init__(self):
        super().__init__()
        self.selection = "now_playing"



api.add_resource(PublicGetTMDB, '/<int:movie_id>')
api.add_resource(PublicGetUpcoming, '/upcoming')
api.add_resource(PublicGetNowplaying, '/nowplaying')