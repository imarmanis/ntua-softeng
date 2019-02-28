import os
class Config(object):
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:root@localhost:5432/{}'.format(
        os.environ.get('DATABASE_NAME') or 'restapi'
    )
