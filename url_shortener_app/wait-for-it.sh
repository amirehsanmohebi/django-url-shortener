#!/bin/bash
until nc -z -v -w30 db 5432
do
    echo db
    echo 5455
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done
python3 manage.py migrate
python3 manage.py runserver 8000
