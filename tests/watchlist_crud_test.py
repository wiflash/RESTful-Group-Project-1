import json, logging
from . import app, user, create_token, reset_db
from unittest import mock
from unittest.mock import patch

class TestWatchlistCrud():
    reset_db()
    def test_post_watchlist(self, user):
        token = create_token(False)

        #case1: post valid
        data = {
            "movie_id":550,
        }

        res = user.post('/user/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 200

        #case2: movie id already added 
        data = {
            "movie_id":550,
        }

        res = user.post('/user/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return self.json_data
        if len(args)>0:
            if args[0] == "https://api.themoviedb.org/3/movie/550":
                return MockResponse({
                    "id": 550,
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
            elif args[0] == "https://api.themoviedb.org/3/movie/1":
                return MockResponse({
                    "status_code":1
                })
        return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect = mocked_requests_get)
    def test_get_watchlist(self, test_reqget_mock, user):
        token = create_token(False)

        #case1: get valid movie filter by genre
        data = {
            "genre":"Action",
        }

        res = user.get('/user/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        assert res.status_code == 200

        #case1: get valid movie not filter
        res = user.get('/user/watchlist',
            headers={'Authorization':'Bearer '+token}
        )
        assert res.status_code == 200

    def test_delete_watchlist(self, user):
        token = create_token(False)

        #case1: deleted success
        data = {
            "movie_id":550,
        }

        res = user.delete('/user/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        assert res.status_code == 200

        #case2: id movie invalid
        data = {
            "movie_id":2,
        }

        res = user.delete('/user/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        assert res.status_code == 404
