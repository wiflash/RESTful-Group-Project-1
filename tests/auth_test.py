import json, logging
from . import reset_db, user
from password_strength import PasswordPolicy

class TestAuthCrud():
    reset_db()
    def test_invalid_user(self, user):
        data = {"username": "wawawaw", "password": "W@wew123"}
        res = user.get("/login", query_string=data)
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 401
        assert res_json["status"] == "UNAUTHORIZED"
        assert res_json["message"] == "Invalid username or password"