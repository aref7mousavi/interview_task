from django.urls import path

from ag_creator.api import AGAPIViewSet

urls = [
    path('start/', AGAPIViewSet.as_view(), name='aggregate-api'),
]
