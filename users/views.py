from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Case, When, Value, BooleanField, F, Sum, Q
from django.utils import timezone
from .models import Users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# Create your views here.

from .forms import SignUp as SignUpForm

def signup(req):
    if(req.method == 'POST'):
        form = SignUpForm(req.POST)
        if(form.is_valid()):
            new_user = form.save()
            print(new_user)
            try:
                user_group = Group.objects.get(name='Library_User')
                new_user.groups.add(user_group)
            except Group.DoesNotExist:
                print('Group doesnot exist with name Library_User')
            return redirect('home')
    else:
        form=SignUpForm()
    return render(req, 'users/signup.html', {'form': form})

# @login_required(login_url='/login')
def index(req):
    return render(req, 'books/home.html')