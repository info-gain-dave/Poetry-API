import os
from datetime import timedelta

class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    permanent_session_lifetime = timedelta(minutes=100)