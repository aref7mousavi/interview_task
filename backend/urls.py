from django.contrib import admin
from django.urls import path

from client.urls import urls

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += urls