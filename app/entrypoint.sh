#!/bin/bash
flask createdb

if [ ! -d /opt/cryptonite/storage/db/migrations ]; then
  flask db init
fi
flask db migrate
flask db upgrade

gunicorn -w 4 -b 0.0.0.0:5000 app:app