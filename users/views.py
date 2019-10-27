from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Case, When, Value, BooleanField, F, Sum, Q
from django.utils import timezone
from .models import Users
# Create your views here.

from .forms import SignUp as SignUpForm

def signup(req):
    if(req.method == 'POST'):
        form = SignUpForm(req.POST)
        if(form.is_valid()):
            form.save()
            print(form.cleaned_data.get('username'))
            print(form.cleaned_data.get('password1'))
            return redirect('home')
    else:
        form=SignUpForm()
    return render(req, 'users/signup.html', {'form': form})

def index(req):
    userData = req.user
    if(userData.is_authenticated):
        user_id = userData.user_id
        order_info = userData.order_set
        total_count = order_info.filter(
            end_date__lt=timezone.now()
        ).aggregate(count= Sum(F('end_date') - timezone.now().date()))
        data = {
            'is_authenticated': userData.is_authenticated,
            'user': userData,
            'order_count': order_info.count(),
            'balance': abs(total_count['count'] * 5) or 0,
            'user_id': user_id
        }
    else:
        data = {
            'is_authenticated': userData.is_authenticated
        }
    return render(req, 'books/home.html', data)