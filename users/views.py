from django.http import HttpResponse
from django.shortcuts import render, redirect

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
        data = {
            'is_authenticated': req.user.is_authenticated,
            'user': req.user
        }
    else:
        data = {
            'is_authenticated': req.user.is_authenticated,
            'user': req.user
        }
    return render(req, 'books/home.html', data)