from backend.default_settings import *

redis_host = os.environ.get("DEFAULT_REDIS_HOST", config("DEFAULT_REDIS_HOST", ''))

CELERY_BROKER_URL = f'redis://default@{redis_host}:6379/0'
CELERY_RESULT_BACKEND = f'redis://default@{redis_host}:6379/0'


# Celery settings
CELERY_APP_NAME = "ag_creator"

INSTALLED_APPS += ["ag_creator.apps.AGCreateConfig", "rest_framework"]
