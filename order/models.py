from django.db import models
from books.models import Books
from users.models import Users

# Create your models here.
class Order(models.Model):
    cart_id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    books = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.cart_id)