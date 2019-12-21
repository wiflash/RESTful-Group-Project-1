import json, hashlib, logging
from . import user, create_token, reset_db
from password_strength import PasswordPolicy
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, admin_required, nonadmin_required

class TestAdminCRUD():
    # POST METHOD
    def test_admin_post(self, user):
        reset_db()
        token = create_token(is_admin=True)
        data = {"username":"user5", "password": "W@wew123"}
        res = user.post("/admin", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["username"] == data["username"]
        assert res_json["password"] == hashlib.md5(data["password"].encode()).hexdigest()
    def test_admin_post_username_already_exists(self, user):
        token = create_token(is_admin=True)
        data = {"username":"user5", "password": "W@wew123"}
        res = user.post("/admin", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Username already exists"
    def test_admin_post_invalid_password_length(self, user):
        token = create_token(is_admin=True)
        data = {"username":"user5", "password": "W@w3w"}
        res = user.post("/admin", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"
    def test_admin_post_invalid_password_numeric(self, user):
        token = create_token(is_admin=True)
        data = {"username":"user5", "password": "W@wewewewew"}
        res = user.post("/admin", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"
    def test_admin_post_invalid_password_uppercase(self, user):
        token = create_token(is_admin=True)
        data = {"username":"user5", "password": "w@w3w123"}
        res = user.post("/admin", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"
    def test_admin_post_invalid_password_special(self, user):
        token = create_token(is_admin=True)
        data = {"username":"user5", "password": "Waw3w123"}
        res = user.post("/admin", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"
    
    # GET METHOD
    def test_admin_get_all_users(self, user):
        token = create_token(is_admin=True)
        res = user.get("/admin", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_admin_get_all_users_filtered(self, user):
        token = create_token(is_admin=True)
        data = {"p": 1, "rp": 10, "status": True}
        res = user.get("/admin", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_admin_get_user_by_id(self, user):
        token = create_token(is_admin=True)
        res = user.get("/admin/1", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    def test_admin_get_user_by_id_but_doesnt_exist(self, user):
        token = create_token(is_admin=True)
        res = user.get("/admin/100", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "ID is not found"
    
    # PUT METHOD
    def test_admin_put_by_user_id(self, user):
        token = create_token(is_admin=True)
        data = {"username": "user2 (edited)", "password": "W@wew123", "status":True}
        res = user.put("/admin/2", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["username"] == data["username"]
        assert res_json["password"] == hashlib.md5(data["password"].encode()).hexdigest()
        assert res_json["status"] == data["status"]
    def test_admin_put_by_user_id_but_username_already_exists(self, user):
        token = create_token(is_admin=True)
        data = {"username": "user1", "password": "W@wew123", "status":True}
        res = user.put("/admin/2", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Username already exists"
    def test_admin_put_by_user_id_but_not_found(self, user):
        token = create_token(is_admin=True)
        data = {"username": "user2", "password": "W@wew123", "status":True}
        res = user.put("/admin/100", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "ID is not found"
    def test_admin_put_by_user_id_but_invalid_password_length(self, user):
        token = create_token(is_admin=True)
        data = {"username": "user1", "password": "W@wew", "status":True}
        res = user.put("/admin/1", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"
    def test_admin_put_by_user_id_but_invalid_password_uppercase(self, user):
        token = create_token(is_admin=True)
        data = {"username": "user1", "password": "w@wew123", "status":True}
        res = user.put("/admin/1", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"
    def test_admin_put_by_user_id_but_invalid_password_numeric(self, user):
        token = create_token(is_admin=True)
        data = {"username": "user1", "password": "W@wewewewew", "status":True}
        res = user.put("/admin/1", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"
    def test_admin_put_by_user_id_but_invalid_password_special(self, user):
        token = create_token(is_admin=True)
        data = {"username": "user1", "password": "Wawew123", "status":True}
        res = user.put("/admin/1", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400
        assert res_json["status"] == "FAILED"
        assert res_json["message"] == "Password is not accepted"

    # DELETE METHOD
    def test_admin_delete_by_user_id(self, user):
        token = create_token(is_admin=True)
        res = user.delete("/admin/2", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
        assert res_json["message"] == "Succesfully deleted"
    def test_admin_delete_but_no_user_id_path(self, user):
        token = create_token(is_admin=True)
        res = user.delete("/admin", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "ID is not found"
    def test_admin_delete_by_user_id_but_not_found(self, user):
        token = create_token(is_admin=True)
        res = user.delete("/admin/100", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404
        assert res_json["message"] == "ID is not found"
    

    # USER
    def test_user_access_to_admin_get(self, user):
        token = create_token(is_admin=False)
        res = user.get("/admin", headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 403
        assert res_json["status"] == "FORBIDDEN"
        assert res_json["message"] == "You should be an admin to access this point"