from django.urls import path
from . import api

urlpatterns = [
    path('get', api.get_books)
]
