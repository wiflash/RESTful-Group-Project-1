from blueprints import db
from flask_restful import fields
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    response_fields = {
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime,
        "id": fields.Integer,
        "username": fields.String,
        "password": fields.String,
        "status": fields.Boolean
    }

    jwt_claim_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "admin_status": fields.Boolean
    }

    def __init__(self, key, secret):
        self.username = key
        self.password = secret

    def __repr__(self):
        return "<Users %r>" % self.id