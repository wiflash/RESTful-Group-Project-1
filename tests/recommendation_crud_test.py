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
                        {"name":"Action"},
                        {"name":"Adventure"},
                        {"name":"Science Fiction"}
                    ],
                    "runtime": 142
                }, 200)
            elif args[0] == "https://geocode.xyz":
                return MockResponse({
                    "longt":"123456",
                    "latt":"123456"
                })
            elif args[0] == "https://api.foursquare.com/v2/venues/search":
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
                })
        return MockResponse(None, 404)
    
    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_get_rec(self, user):
        token = create_token(False)

        #case1: post valid
        data = {
            "genre":"Drama",
            "lokasi":"malang,ID"
        }

        res = user.get('/rekomendasi', query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 200

