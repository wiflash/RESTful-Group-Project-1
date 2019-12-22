import requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
import json
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

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        parser.add_argument('region', type=str, location='args')
        args = parser.parse_args()
        page = args['p']
        per_page = args['rp']
        offset = (page-1)*per_page

        rq = requests.get(self.host + '/movie/upcoming', params={'api_key':self.api_key, 'region':args['region']})
        rq_movies = rq.json()['results']
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

        rows = []
        total_entry = len(movies)
        if total_entry%per_page != 0 or total_entry == 0: total_page = int(total_entry/per_page) + 1
        else: total_page = int(total_entry/per_page)
        if total_entry != 0:
            for i in range(0, per_page):
                rows.append(movies[i+offset])
                if i == len(movies)-1:
                    break
        return {"halaman":page, "total_halaman":total_page, "per_halaman":per_page, "hasil":rows}, 200
            
class PublicGetNowplaying(Resource):
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10)
        parser.add_argument('region', type=str, location='args')
        args = parser.parse_args()
        page = args['p']
        per_page = args['rp']
        offset = (page-1)*per_page

        rq = requests.get(self.host + '/movie/now_playing', params={'api_key':self.api_key, 'region':args['region']})
        rq_movies = rq.json()['results']
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

        rows = []
        total_entry = len(movies)
        if total_entry%per_page != 0 or total_entry == 0: total_page = int(total_entry/per_page) + 1
        else: total_page = int(total_entry/per_page)
        if total_entry != 0:
            for i in range(0, per_page):
                rows.append(movies[i+offset])
                if i == len(movies)-1:
                    break
        return {"halaman":page, "total_halaman":total_page, "per_halaman":per_page, "hasil":rows}, 200


api.add_resource(PublicGetTMDB, '/<int:movie_id>')
api.add_resource(PublicGetUpcoming, '/upcoming')
api.add_resource(PublicGetNowplaying, '/nowplaying')