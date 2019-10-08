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