from django.shortcuts import render
from .models import Books

# Create your views here.

def index(req):
    userData = req.user
    if(userData.is_authenticated):
        data = {
            'is_authenticated': req.user.is_authenticated,
            'user': req.user,
            'data': Books.objects.all()
        }
    else:
        data = {
            'is_authenticated': req.user.is_authenticated,
            'user': req.user
        }
    return render(req, 'books/home.html', data)