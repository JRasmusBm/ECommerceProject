#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn berriesandgoods.wsgi:application \
  --chdir berriesandgoods \
  --bind ":8000" \
  --workers 3
