from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
import requests

<<<<<<< HEAD
blueprint_rekomendasi = Blueprint('rekomendasi', __name__)
api = Api(blueprint_rekomendasi)
=======
bp_rekomendasi = Blueprint('rekomendasi', __name__)
api = Api(bp_rekomendasi)
>>>>>>> 7b7d1d6883a177956d67ae8f46241fc3f2452604

class RekomendasiResource(Resource):
    geocode_host = 'https://geocode.xyz'
    foursquare_host = 'https://api.foursquare.com/v2/venues/search'
<<<<<<< HEAD
    #hos & api_key tmdb
    host = 'https://api.themoviedb.org/3'
    api_key = 'df1a34ae3c1705433378bc967b244227'
=======
>>>>>>> 7b7d1d6883a177956d67ae8f46241fc3f2452604

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('genre', location='args', default=None, required=True)
        parser.add_argument('lokasi', location='args', default=None, required=True)
        args = parser.parse_args()

<<<<<<< HEAD
        #request api tmdb
        rq = requests.get(self.host + '/movie/now_playing', params={'api_key':self.api_key, 'region':'ID'})

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
            if args['genre'] in hasil['genres']:
                movies.append(hasil)
 
        #request api geolocode.xyz
=======
>>>>>>> 7b7d1d6883a177956d67ae8f46241fc3f2452604
        rq = requests.get(self.geocode_host, params={
            'scantext':args['lokasi'],
            'geoit':'json'})

        georq = rq.json()
<<<<<<< HEAD
        if georq['matches'] is not None:
            lon = georq['longt']
            lat = georq['latt']
        else:
            return {'message':'Location Unknown'}, 404

        #request api foursquare
=======
        lon = georq['longt']
        lat = georq['latt']

>>>>>>> 7b7d1d6883a177956d67ae8f46241fc3f2452604
        rq = requests.get(self.foursquare_host, params={
            'client_id':'QJKKM3AWZP0R1GYQXOPDOXXDAH4M43R5Z0TJ2AWY4EQR4UVZ', 
            'client_secret':'IPX1CYTP32FG0A5NWQKAMIKQPUDDI3KVL103YA04OX5JCV1M', 
            'v':'20191221',
            'll':str(lat)+','+str(lon),
            'near':args['lokasi'],
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
<<<<<<< HEAD
        
        if (movies == []) or (listfs == []):
            if movies == []:
                return {'message': 'Sorry, movie with genre '+args['genre']+' not available now'}, 200
            else:
                return {'message': "Sorry, there's no movie theater recommendation near your area"}, 200
        else:
            return {
                'rekomendasi film': movies,
                'rekomendasi tempat nonton': listfs
            }, 200
=======

        return {
            'rekomendasi tempat nonton': listfs
        }
>>>>>>> 7b7d1d6883a177956d67ae8f46241fc3f2452604


api.add_resource(RekomendasiResource,'')