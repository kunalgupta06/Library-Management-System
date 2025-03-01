from flask import Flask
from flask_restful import Api
from flask_caching import Cache
from flask_cors import CORS
from database import db
from config import Config
from celery_app import make_celery
from controllers.user_auth import (ApproveRequest, DailyReminder, GetBookRequests, Register, Login, RejectRequest, RentBook, ReturnBook, RevokeRequest, TriggerExportCSV, 
                                     delete_book, libBook, members, 
                                    stats, add_book, updatebook,ReturnBook)
import os
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

# make_celery.conf.update(app.config)

# Initialize CORS with correct origins and methods
# CORS(app, resources={r'/*': {'origins': 'http://localhost:8080'}}, supports_credentials=True)
from flask_cors import CORS

CORS(app, resources={r'/*': {'origins': '*', 'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']}})
load_dotenv()

# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
# app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')
# app.config['MAIL_SERVER'] = os.getenv('smtp.gmail.com')
# app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
# app.config['MAIL_USERNAME'] = os.getenv('kunalg2022@gmail.com')
# app.config['MAIL_PASSWORD'] = os.getenv('Kunal@2004')
# app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
# app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

# app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER']=''
# app.config['SECURITY_TOKEN_MAX_AGE']=3600
# app.config['SECURITY_LOGIN_WITHOUT_CONFIRMATION']=True
cache = Cache()
app.config['CACHE_TYPE'] = "RedisCache"
app.config['REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/0"
app.config['CACHE_DEFAULT_TIMEOUT'] = 120
app.config['CACHE_KEY_PREFIX'] = "library"

app.config["CELERY_BROKER_URL"]="redis://localhost:6379/1"
app.config["CELERY_RESULT_BACKEND"]="redis://localhost:6379/2"
app.config["ENABLE_UTC"]=False

app.config["SMTP_SERVER_HOST"] = "localhost"
app.config["SMTP_SERVER_PORT"] = 1025
app.config["SENDER_ADDRESS"] = "kunalg2022@gmail.com"
app.config["SENDER_PASSWORD"] = "Kunal@2004"

cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': 0,
        'CACHE_DEFAULT_TIMEOUT': 300  
    }
app.config.from_mapping(cache_config)


cache.init_app(app)


app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = './Library-Management/Backend/controllers/static/book_images/'


app.config.from_object(Config)


cache.init_app(app)
db.init_app(app)

from flask_mail import Mail
mail = Mail(app)
app.extensions['mail'] = mail



# Add resource routes
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(stats, '/stats')
api.add_resource(add_book, '/addbook')
api.add_resource(libBook, '/libBook')

api.add_resource(RentBook, '/rentbook')
api.add_resource(members, '/members')
api.add_resource(updatebook, '/updatebook/<int:book_id>')
api.add_resource(delete_book, '/deletebook/<int:book_id>')
api.add_resource(DailyReminder, '/daily-reminder')
# api.add_resource(TriggerMonthlyReport, '/monthly-report')
api.add_resource(TriggerExportCSV, '/export-csv')
api.add_resource(GetBookRequests, '/book_requests')
api.add_resource(ApproveRequest, '/approve_request/<int:request_id>')
api.add_resource(RejectRequest, '/reject_request/<int:request_id>')
api.add_resource(ReturnBook, '/returnbook')
api.add_resource(RevokeRequest,'/revoke_request/<int:request_id>')

# Run the Flask app
# celery = make_celery(app)
if __name__ == '__main__':
    app.run(debug=True)

