#!/usr/bin/env python3

from app import create_app
from app.models import db
import os

ROBOT_DB_URL = 'postgresql+psycopg2://root:root@localhost:5432/robot'
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = ROBOT_DB_URL
with app.app_context():
    db.drop_all()
    db.create_all()

