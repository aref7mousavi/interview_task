# yourapp/tasks/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create the Celery application instance
app = Celery('ag_creator')  # Adjust this to match your app name

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.broker_url = 'redis://default@172.18.0.3:6379/0'
# app.conf.result_backend = 'redis://default@172.18.0.3:6379/0'

app.conf.broker_connection_retry_on_startup = True
# Auto-discover tasks in all apps included in INSTALLED_APPS setting of your Django project
app.autodiscover_tasks(["ag_creator"])
