#!/bin/sh

# Exit immediately if a command exits with a non-zero status
#set -e
#rm -r client ag_creator
# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate
#python manage.py init_csv
# Collect static files (uncomment if needed)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start the Django server
echo "Starting Django server..."
exec "$@"