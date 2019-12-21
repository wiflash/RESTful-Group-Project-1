import json, hashlib, logging
from . import user, create_token, reset_db
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, nonadmin_required

class TestUserRUD():
    # GET METHOD
    def test_user_get(self, user):
        reset_db()
        token = create_token(is_admin=False)
        data = {}
        res = user.get("/user", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    
    # PUT METHOD
    def test_user_put(self, user):
        token = create_token(is_admin=False)
        data = {"username": "user1 (edited)", "password": "W@wew123"}
        res = user.put("/user", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["username"] == data["username"]
        assert res_json["password"] == hashlib.md5(data["password"].encode()).hexdigest()
    def test_user_put_invalid_username(self, user):
        token = create_token(is_admin=False)
        data = {"username": "user2", "password": "W@wew123"}
        res = user.put("/user", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["message"] == "Username already exists"
        assert res_json["status"] == "FAILED"
    def test_user_put_invalid_password_length(self, user):
        token = create_token(is_admin=False)
        data = {"username": "user1", "password": "W@w3w"}
        res = user.put("/user", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["message"] == "Password is not accepted"
        assert res_json["status"] == "FAILED"
    def test_user_put_invalid_password_numeric(self, user):
        token = create_token(is_admin=False)
        data = {"username": "user1", "password": "W@wewewewew"}
        res = user.put("/user", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["message"] == "Password is not accepted"
        assert res_json["status"] == "FAILED"
    def test_user_put_invalid_password_uppercase(self, user):
        token = create_token(is_admin=False)
        data = {"username": "user1", "password": "w@wew123"}
        res = user.put("/user", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["message"] == "Password is not accepted"
        assert res_json["status"] == "FAILED"
    def test_user_put_invalid_password_special(self, user):
        token = create_token(is_admin=False)
        data = {"username": "user1", "password": "Waw3w123"}
        res = user.put("/user", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["message"] == "Password is not accepted"
        assert res_json["status"] == "FAILED"

    # DELETE METHOD
    def test_user_delete(self, user):
        token = create_token(is_admin=False)
        res = user.delete("/user", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["message"] == "Succesfully deleted"
    

    # ADMIN
    def test_admin_access_to_user_get(self, user):
        token = create_token(is_admin=True)
        data = {}
        res = user.get("/user", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
        assert res_json["message"] == "You should be a user to access this point"