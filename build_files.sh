#!/bin/bash
# Build script for Render deployment

# Exit on error
set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate