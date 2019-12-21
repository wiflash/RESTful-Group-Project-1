import json
from . import create_token, reset_db, user, app
import requests
from mock import patch, mock
from unittest import mock
from blueprints.tmdb import PublicGetTMDB, PublicGetNowplaying, PublicGetUpcoming
from unittest.mock import patch

class TestTMDB():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if len(args)>0:
            if args[0] == "https://api.themoviedb.org/3/movie/181812":
                return MockResponse({
                    "id": 181812,
                    "title": "Star Wars: The Rise of Skywalker",
                    "overview": "The surviving Resistance faces the First Order once again as the journey of Rey, Finn and Poe Dameron continues. With the power and knowledge of generations behind them, the final battle begins.",
                    "genres": [
                        {"name":"Action"},
                        {"name":"Adventure"},
                        {"name":"Science Fiction"}
                    ],
                    "release_date": "2019-12-18",
                    "status": "Released",
                    "runtime": 142,
                    "vote_average": 6.8
                }, 200)
        return MockResponse(None, 404)
    
    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_tmdb(self, test_reqget_mock, user):
        token = create_token(True)
        res = user.get('/tmdb/181812',
                headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 200

class TestInvalidTMDB():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if len(args)>0:
            if args[0] == "https://api.themoviedb.org/3/movie/181812":
                return MockResponse({
                    "status_code": 34
                }, 200)
        return MockResponse(None, 404)
    
    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_tmdb(self, test_reqget_mock, user):
        token = create_token(True)
        res = user.get('/tmdb/181812',
                headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 404

class TestUpcoming():
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if len(args)>0:
            if args[0] == "https://api.themoviedb.org/3/movie/upcoming":
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
        return MockResponse(None, 404)
    
    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_tmdb(self, test_reqget_mock, user):
        data = {
            'p':1,
            'rp':2,
            'region':'US'
        }
        res = user.get('/tmdb/upcoming', query_string=data)
        assert res.status_code == 200

class TestNowplaying():
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
        return MockResponse(None, 404)
    
    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_tmdb(self, test_reqget_mock, user):
        data = {
            'p':1,
            'rp':2,
            'region':'US'
        }
        res = user.get('/tmdb/nowplaying', query_string=data)
        assert res.status_code == 200
