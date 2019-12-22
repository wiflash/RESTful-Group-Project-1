import json, logging
from . import app, user, create_token, reset_db
# from mock import mock
from unittest import mock
from unittest.mock import patch

class TestRecommendationCrud():
    reset_db()

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if len(args)>0:
            if args[0] == "https://api.themoviedb.org/3/movie/now_playing":
                return MockResponse({"results":
                    [{
                        "id": 181812,
                        "title": "Star Wars: The Rise of Skywalker",
                        "overview": "The surviving Resistance faces the First Order once again as the journey of Rey, Finn and Poe Dameron continues. With the power and knowledge of generations behind them, the final battle begins.",
                        "release_date": "2019-12-18",
                        "status": "Released",
                        "vote_average": 6.8
                    },
                    {
                        "id": 181812,
                        "title": "Star Wars: The Rise of Skywalker",
                        "overview": "The surviving Resistance faces the First Order once again as the journey of Rey, Finn and Poe Dameron continues. With the power and knowledge of generations behind them, the final battle begins.",
                        "release_date": "2019-12-18",
                        "status": "Released",
                        "vote_average": 6.8
                    }]}
                , 200)
            elif args[0] == "https://api.themoviedb.org/3/movie/181812":
                return MockResponse({
                    "genres": [
                        {"name":"Drama"},
                        {"name":"Adventure"},
                        {"name":"Science Fiction"}
                    ],
                    "runtime": 142
                }, 200)
            elif args[0] == "https://geocode.xyz":
                if kwargs["params"]["scantext"] == 'bojongsoang':
                    matches=None; longt="123456"; latt="123456"
                elif kwargs['params']['scantext'] == 'papua':
                    matches=1; longt="0"; latt="0"
                else:
                    matches=1; longt="123456"; latt="123456"
                return MockResponse({
                    "longt":longt,
                    "latt":latt,
                    "matches":matches
                }, 200)
            elif args[0] == "https://api.foursquare.com/v2/venues/search":
                if kwargs['params']['ll'] == '0,0':
                    return MockResponse({
                        "response":{
                            "venues":[]
                        }
                    }, 404)
                return MockResponse({
                    "response":{
                        "venues":[
                            {
                                "name":"Dieng 21",
                                "location":{
                                    "formattedAddress":"Jalan Raya Langsep No. 3",
                                    "distance":2121
                                }
                            }
                        ]
                    }
                }, 200)
        return MockResponse(None, 404)
    
    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_get_rec(self, test_reqget_mock, user):
        token = create_token(False)

        #case1: get valid
        data = {
            "genre":"Drama",
            "lokasi":"malang,ID"
        }

        res = user.get('/user/rekomendasi', query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 200

        #case2: location unknown
        data = {
            "genre":"Drama",
            "lokasi":"bojongsoang"
        }

        res = user.get('/user/rekomendasi', query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 404

        #case3: movie not available
        data = {
            "genre":"Action",
            "lokasi":"malang,ID"
        }

        res = user.get('/user/rekomendasi', query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 404


        #case4: theater not available
        data = {
            "genre":"Drama",
            "lokasi":"papua"
        }

        res = user.get('/user/rekomendasi', query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 404

        #case5: spesific region and non genre
        data = {
            "lokasi":"malang,ID",
            "region":"ID"
        }

        res = user.get('/user/rekomendasi', query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 200

        #case6: page out of number
        data = {
            "genre":"Action",
            "lokasi":"malang",
            "p":2
        }

        res = user.get('/user/rekomendasi', query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 400