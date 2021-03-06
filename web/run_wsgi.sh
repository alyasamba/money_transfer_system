#!/bin/bash
chmod 777 /tmp
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
celery worker -A project --beat -l DEBUG -f /tmp/celery.log &
gunicorn --preload -c /etc/gunicorn/gunicorn.py mts_django.wsgi:application
