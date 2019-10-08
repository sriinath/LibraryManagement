from django.db import models
from books.models import Books
from users.models import Users
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from users.models import get_item as get_user
from books.models import get_item as get_book
import json

# Create your models here.
class Order(models.Model):
    cart_id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    returned_date = models.DateField(null=True)
    book_id = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

def add_book(req):
    if(req.method == 'POST'):
        postBody = req.POST
        if(postBody):
            user_id = postBody.get('user_id')
            book_id = postBody.get('book_id')
            bookIns = get_book(item_id=book_id)
            userIns = get_user(item_id=user_id)
            result = add_order(userObj=userIns, bookObj=bookIns)
            if(result):
                return HttpResponse('Success from add_order')
            else:
                return HttpResponse('Result failure from add_order')
    return HttpResponse('Failed to process')

def add_order(userObj, bookObj):
    st_date = timezone.now()
    en_date = st_date + timezone.timedelta(days=15)
    order = Order(start_date=st_date, end_date=en_date, book_id=bookObj, user_id=userObj)
    order.save()
    # Need to validate whether db is successfully saved
    return True