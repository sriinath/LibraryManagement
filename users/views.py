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
            'is_authenticated': userData.is_authenticated,
            'user': userData,
            'user_id': userData.user_id
        }
    else:
        data = {
            'is_authenticated': userData.is_authenticated
        }
    return render(req, 'books/home.html', data)