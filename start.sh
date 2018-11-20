#!/bin/bash

# Collect Static Files
echo Collecting Static Files.
cd berriesandgoods/
python manage.py collectstatic --no-input
cd ..

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn berriesandgoods.wsgi:application \
  --chdir berriesandgoods \
  --bind ":8000" \
  --workers 3
