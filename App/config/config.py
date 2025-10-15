from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
from decouple import config
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


db = SQLAlchemy()


class Config():
    SECRET_KEY = config('secret_key', 'secret')
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_ACCESS_TOKEN = timedelta(minutes= 20)
    JWT_REFRESH_TOKEN = timedelta(minutes=30)
    JWT_SECRET_KEY = config("JWT_SECRET_KEY",)


class DevConfig(Config):
    DEBUG= config("DEBUG", cast = bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI="sqlite:///book.sqlite3"


class TestConfig():
    pass

class ProdConfig():
    pass

config_dict={
    "Dev":DevConfig(),
    "Test":TestConfig(),
    "Prod":ProdConfig(),
    }