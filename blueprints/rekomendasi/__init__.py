from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, nonadmin_required
import requests

bp_rekomendasi = Blueprint('rekomendasi', __name__)
api = Api(bp_rekomendasi)

class RekomendasiResource(Resource):
    geocode_host = 'https://geocode.xyz'
    foursquare_host = 'https://api.foursquare.com/v2/venues/search'
    #hos & api_key tmdb
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'

    @jwt_required
    @nonadmin_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('genre', location='args', default=None)
        parser.add_argument('lokasi', location='args', default='Jakarta,ID')
        parser.add_argument('region', location='args', default='ID')
        args = parser.parse_args()
        
        #request api tmdb
        rq = requests.get(self.host + '/movie/now_playing', params={'api_key':self.api_key, 'region':args['region'], 'page':args['p']})            

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
            if args['genre'] is not None:
                if args['genre'] in hasil['genres']:
                    movies.append(hasil)
            else:
                movies.append(hasil)

        #request api geolocode.xyz
        rq = requests.get(self.geocode_host, params={
            'scantext':args['lokasi'],
            'geoit':'json'})

        georq = rq.json()
        if georq['matches'] is not None:
            lon = georq['longt']
            lat = georq['latt']
        else:
            return {'message':'Location Unknown'}, 404

        #request api foursquare
        rq = requests.get(self.foursquare_host, params={
            'client_id':'QJKKM3AWZP0R1GYQXOPDOXXDAH4M43R5Z0TJ2AWY4EQR4UVZ', 
            'client_secret':'IPX1CYTP32FG0A5NWQKAMIKQPUDDI3KVL103YA04OX5JCV1M', 
            'v':'20191221',
            'll':str(lat)+','+str(lon),
            'radius':5000,
            'categoryId':'4bf58dd8d48988d17f941735',
            'limit':3
            })

        fsrq = rq.json()
        listfs = []
        for venue in fsrq['response']['venues']:
            place = {
                'name':venue['name'],
                'location':venue['location']['formattedAddress'],
                'distance':venue['location']['distance']
            }
            listfs.append(place)
        
        if (movies == []) or (listfs == []):
            if movies == []:
                return {'message': 'Sorry, movie with this genre not available now'}, 404
            else:
                return {'message': "Sorry, there's no movie theater recommendation near your area"}, 404
        else:                
            return {
                'rekomendasi film': movies,
                'rekomendasi tempat nonton': listfs
            }, 200


api.add_resource(RekomendasiResource,'')