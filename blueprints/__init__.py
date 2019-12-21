from flask import Flask, request
from flask_restful import Resource, Api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import json, logging, os
from logging.handlers import RotatingFileHandler

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps

app = Flask(__name__)

app.config['APP_DEBUG'] = True

#JWT Config
app.config['JWT_SECRET_KEY'] = 'YoyoayoYoayoyoYoayoYoaYoYoAyoAyo'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] == 0: #non-internal statusnya false (0), internal statusnya true (1)
            return{'status':'FORBIDDEN', 'message':'Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# SQLAlchemy Config
try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/rest_training_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/rest_training'
except Exception as e:
    raise e

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/rest_training'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#after request
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s",
    json.dumps({
        'status_code': response.status_code,
        'method': request.method,
        'code': response.status,
        'uri': request.full_path,
        'request':requestData,
        'response': json.loads(response.data.decode('utf-8')) }))
    else: #untuk error 400, 404, dll
        app.logger.error("REQUEST_LOG\t%s",
    json.dumps({
        'status_code': response.status_code,
        'method': request.method,
        'code': response.status,
        'uri': request.full_path,
        'request':requestData,
        'response':json.loads(response.data.decode('utf-8')) }))
    return response

#Import Blueprint & Routes
from blueprints.rekomendasi import bp_rekomendasi
app.register_blueprint(bp_rekomendasi, url_prefix='/rekomendasi')

db.create_all()