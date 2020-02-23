from django.urls import path
from .api import add_book, get_order_details, get_total_order_by_user, get_outstanding_balance_by_user, remove_order
from . import views
urlpatterns = [
    path('add', add_book),
    path('view', views.index),
    path('get', get_order_details),
    path('count', get_total_order_by_user),
    path('balance', get_outstanding_balance_by_user),
    path('delete', remove_order)
]
