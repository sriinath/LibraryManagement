from django.urls import path
from .api import get_books, upload_product_data, process_product_data

urlpatterns = [
    path('get', get_books),
    path('api/v1/upload', upload_product_data),
    path('api/v1/process_data', process_product_data)
]
