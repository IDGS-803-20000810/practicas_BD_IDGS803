import os
import urllib
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY='Clave_Nueva'
    SESSION_COOKIE_SECURE=False
    

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://javier:root@localhost/practica_bd'