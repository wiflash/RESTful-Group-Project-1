import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required
import json
from blueprints import db, app
bp_tmdb = Blueprint('tmdb', __name__)
api = Api(bp_tmdb)

class PublicGetTMDB(Resource):
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    # @jwt_required
    def get(self, movie_id):

        rq = requests.get(self.host + '/movie/' + str(movie_id), params={'api_key':self.api_key})
        movie = rq.json()
        nama_genre=[]
        genre = movie['genres']
        for i in genre:
            nama_genre.append(i['name'])
        return{
            'movie_id': movie['id'],
            'judul': movie['title'],
            'sinopsis': movie['overview'],
            # 'genres': movie['genres'],
            'genres': nama_genre,
            'tanggal_rilis': movie['release_date'],
            'status_rilis': movie['status'],
            'durasi': movie['runtime'],
            'rating': movie['vote_average']
        }

class PublicGetUpcoming(Resource):
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    # @jwt_required
    def get(self):

        rq = requests.get(self.host + '/movie/upcoming', params={'api_key':self.api_key})

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']

        movie = rq.json()
        movie = movie['results']
        movies = []
        for i in movie:
            rq2 = requests.get(self.host + '/movie/' + str(i['id']), params={'api_key':self.api_key})
            movie2 = rq2.json()
            nama_genre=[]
            genre = movie2['genres']
            for j in genre:
                nama_genre.append(j['name'])
            
            hasil = {
                'movie_id': i['id'],
                'judul': i['title'],
                'sinopsis': i['overview'],
                'genres': nama_genre,
                'tanggal_rilis': i['release_date'],
                'durasi': movie2['runtime'],
                'rating': i['vote_average']
            }
            movies.append(hasil)

        return movies, 200
            
class PublicGetNowplaying(Resource):
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    # @jwt_required
    def get(self):

        rq = requests.get(self.host + '/movie/now_playing', params={'api_key':self.api_key})

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']

        movie = rq.json()
        movie = movie['results']
        movies = []
        for i in movie:
            rq2 = requests.get(self.host + '/movie/' + str(i['id']), params={'api_key':self.api_key})
            movie2 = rq2.json()
            nama_genre=[]
            genre = movie2['genres']
            for j in genre:
                nama_genre.append(j['name'])
            
            hasil = {
                'movie_id': i['id'],
                'judul': i['title'],
                'sinopsis': i['overview'],
                'genres': nama_genre,
                'tanggal_rilis': i['release_date'],
                'durasi': movie2['runtime'],
                'rating': i['vote_average']
            }
            movies.append(hasil)

        return movies, 200            
        
api.add_resource(PublicGetTMDB, '/<int:movie_id>')
api.add_resource(PublicGetUpcoming, '/upcoming')
api.add_resource(PublicGetNowplaying, '/nowplaying')