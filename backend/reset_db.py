#!/usr/bin/env python3


import sys
from app import create_app
from app.models import db, User


try:
    DB_NAME = sys.argv[1]
except IndexError:
    DB_NAME = 'robot'
try:
    DB_USER = sys.argv[2]
except IndexError:
    DB_USER = 'root'
DB_PASS = DB_USER
DB_URI = 'postgresql+psycopg2://' + DB_USER + ':' + DB_PASS + '@localhost:5432/' + DB_NAME
print('Reset database \'' + DB_NAME + '\'')

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(User(username='root', password='root'))
    db.session.commit()
