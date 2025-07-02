import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '12981709210dcc27bbbf43666280178c'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app', 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
