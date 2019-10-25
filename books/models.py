from django.db import models
# Create your models here.

class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.CharField(max_length=750)
    stock_count = models.IntegerField()
    user_info = models.ManyToManyField('users.Users', through='order.Order')
    
    def __str__(self):
        return self.name

def get_item(item_id):
    return Books.objects.get(pk=item_id)