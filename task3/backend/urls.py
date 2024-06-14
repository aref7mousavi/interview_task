from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def health_check(request):
    # Your endpoint logic here
    return HttpResponse("asd")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),
]

if settings.APP:
    import importlib

    url = importlib.import_module(f"{settings.APP}.urls")
    urlpatterns += url.urls
