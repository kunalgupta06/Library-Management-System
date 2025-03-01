from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_caching import Cache
import redis
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    CORS(app)
    db.init_app(app)
    api = Api(app)
    cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': 0,
        'CACHE_DEFAULT_TIMEOUT': 300  # Cache expiry time in seconds
    }
    app.config.from_mapping(cache_config)
    Cache.init_app(app)

    from Backend.controllers.user_auth import register, login
    api.add_resource(register, '/register')
    api.add_resource(login, '/login')

    return app
