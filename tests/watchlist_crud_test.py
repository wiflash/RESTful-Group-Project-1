import json, logging
from . import app, user, create_token, reset_db

class TestWatchlistCrud():
    reset_db()
    def test_post_watchlist(self, user):
        token = create_token(False)

        #case1: post valid
        data = {
            "movie_id":550,
        }

        res = user.post('/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 200

        #case2: movie id already added 
        data = {
            "movie_id":550,
        }

        res = user.post('/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_get_watchlist(self, user):
        token = create_token(False)

        #case1: get valid movie

        res = user.get('/watchlist',
            headers={'Authorization':'Bearer '+token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 200

        #case2: get invalid movie
        data = {
            "movie_id":1,
        }
        res = user.post('/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        res = user.get('/watchlist',
            headers={'Authorization':'Bearer '+token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_delete_watchlist(self, user):
        token = create_token(False)

        #case1: deleted success
        data = {
            "movie_id":1,
        }

        res = user.delete('/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )

        res_json = json.loads(res.data)
        assert res.status_code == 200

        #case2: id movie invalid
        data = {
            "movie_id":2,
        }

        res = user.delete('/watchlist',
            query_string=data,
            headers={'Authorization':'Bearer '+token}
        )
        res_json = json.loads(res.data)
        assert res.status_code == 404
