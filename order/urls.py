from django.urls import path
from .api import add_book

urlpatterns = [
    path('add', add_book)
]
