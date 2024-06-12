#!/bin/bash

# Install libraries for GeoDjango
apt-get install postgis*
apt-get install binutils libproj-dev gdal-bin

# Apply database migrations
python manage.py migrate

# Start server
exec "$@"