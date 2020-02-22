from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

choiceGender = (
    ('n', 'None'),
    ('m', 'Male'),
    ('f', 'Female')
)

class Users(AbstractUser):
    id = models.AutoField(primary_key= True)
    gender = models.TextField(choices=choiceGender)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.username

def get_item(item_id):
    return Users.objects.get(pk=item_id)