from django.urls import path
from . import models

urlpatterns = [
    path('order/add', models.add_book)
]
