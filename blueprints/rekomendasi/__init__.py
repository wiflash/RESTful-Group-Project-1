from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
import requests

blueprint_rekomendasi = Blueprint('rekomendasi', __name__)
api = Api(blueprint_rekomendasi)

class RekomendasiResource(Resource):
    geocode_host = 'https://geocode.xyz'
    foursquare_host = 'https://api.foursquare.com/v2/venues/search'
    tmdb_host = 'https://api.themoviedb.org/3/'

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('genre', location='args', default=None, required=True)
        parser.add_argument('lokasi', location='args', default=None, required=True)
        args = parser.parse_args()

        #request api tmdb

        #request api geolocode.xyz
        rq = requests.get(self.geocode_host, params={
            'scantext':args['lokasi'],
            'geoit':'json'})

        georq = rq.json()
        lon = georq['longt']
        lat = georq['latt']

        #request api foursquare
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

        return {
            'rekomendasi tempat nonton': listfs
        }

        # return fsrq

api.add_resource(RekomendasiResource,'')