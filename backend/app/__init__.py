import datetime
from dotenv import load_dotenv
from apiflask import APIFlask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
import os
import dropbox


load_dotenv()
host = os.getenv('HOST')
app = APIFlask(__name__, template_folder='../templates',
               enable_openapi=os.getenv('ENV') != 'production')
acces_expire = datetime.timedelta(
    minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_COOKIE_SAMESITE'] = os.getenv('JWT_COOKIE_SAMESITE')
app.config['JWT_COOKIE_CSRF_PROTECT'] = (
    os.getenv('JWT_COOKIE_CSRF_PROTECT') == 'true')
app.config['JWT_COOKIE_SECURE'] = (
    os.getenv('JWT_COOKIE_SECURE') == 'true')
app.config['JWT_SESSION_COOKIE'] = os.getenv('JWT_SESSION_COOKIE')
# app.config['JWT_COOKIE_DOMAIN'] = os.getenv('JWT_COOKIE_DOMAIN')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = acces_expire
app.config['URL_PASSWORD_RESET'] = os.getenv('URL_PASSWORD_RESET')

smtp_config = {
    'MAIL_TLS': os.getenv('MAIL_TLS'),
    'MAIL_SSL': os.getenv('MAIL_SSL'),
    'MAIL_PORT': os.getenv('MAIL_PORT'),
    'MAIL_SERVER': os.getenv('MAIL_SERVER'),
    'MAIL_SENDER': os.getenv('MAIL_SENDER'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD')
}

mongo: PyMongo = PyMongo(app)
jwt: JWTManager = JWTManager(app)
dbx: dropbox.Dropbox = dropbox.Dropbox(
    oauth2_access_token=os.getenv('DBX_ACCESS_TOKEN'),
    oauth2_refresh_token=os.getenv('DBX_REFRESH_TOKEN'),
    scope=['files.content.write', 'files.content.read'],
    app_key=os.getenv('DBX_KEY'),
    app_secret=os.getenv('DBX_SECRET'))
