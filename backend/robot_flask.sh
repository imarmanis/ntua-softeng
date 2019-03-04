#!/usr/bin/env bash

python3 reset_db.py robot
export DATABASE_NAME=robot
flask run
