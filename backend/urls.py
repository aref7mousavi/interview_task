from django.conf import settings
from django.contrib import admin
from django.urls import path

from client.urls import urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.APP:
    import importlib

    url = importlib.import_module(f"{settings.APP}.urls")
    urlpatterns += urls
