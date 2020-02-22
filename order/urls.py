from django.urls import path
from .api import add_book, get_order_details, get_total_order_by_user
from . import views
urlpatterns = [
    path('add', add_book),
    path('view', views.index),
    path('get', get_order_details),
    path('count', get_total_order_by_user)
]
