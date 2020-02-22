from django.db import models
# Create your models here.

class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.CharField(max_length=750)
    stock = models.IntegerField()
    price = models.FloatField(default=None, null=True)
    
    def __str__(self):
        return self.title

def get_item(item_id):
    return Books.objects.get(pk=item_id)