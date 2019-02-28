#!/usr/bin/env bash

python3 create_robot_db.py
export DATABASE_NAME=robot
flask run
