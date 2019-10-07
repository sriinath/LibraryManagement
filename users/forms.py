from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

choiceGender = (
    ('n', 'None'),
    ('m', 'Male'),
    ('f', 'Female')
)

class SignUp(UserCreationForm):
    gender = forms.ChoiceField(choices=choiceGender, required=False)
    phone = forms.IntegerField(min_value=1000000000, max_value=999999999, required=False)

    class Meta:
        model = Users
        fields = ('username', 'email', 'gender', 'phone', 'password1', 'password2')