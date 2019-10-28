from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Case, When, Value, BooleanField, F, Sum, Q
from django.utils import timezone
from .models import Users
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='/login')
def index(req):
    return render(req, 'books/home.html')