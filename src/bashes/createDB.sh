#!/usr/bin/env bash

python3 manage.py makemigrations security_service &

python3 manage.py migrate &

python3 manage.py runserver 0.0.0.0:8000
#gunicorn config.wsgi -c ./gunicorn/gunicorn.py -b 0.0.0.0:80
