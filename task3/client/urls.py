from django.urls import path

from client.api import ClientAPIViewSet

urls = [
    path('api/', ClientAPIViewSet.as_view(), name='client-api'),
]
