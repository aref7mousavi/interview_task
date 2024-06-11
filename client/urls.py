from django.urls import path

from client.api import APIViewSet

urls = [
    path('1/', APIViewSet.as_view(), name='1'),
]