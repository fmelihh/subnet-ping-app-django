#!/bin/bash

poetry shell
python manage.py collectstatic --noinput
python manage.py makemigrations subnet_ping
python manage.py migrate
