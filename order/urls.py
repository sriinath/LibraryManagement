from django.urls import path
from .api import add_book, get_order_details
from . import views
urlpatterns = [
    path('add', add_book),
    path('view', views.index),
    path('get', get_order_details)
]
