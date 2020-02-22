from django.db import models
from books.models import Books
from users.models import Users
from datetime import timedelta, datetime

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    ordered_at = models.DateTimeField(auto_now=True)
    expected_return_date = models.DateTimeField(null=True, blank=True)
    actual_return_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=((1, 'pending'), (2, 'approved'), (3, 'declined')), default=1)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, default=None)
    ordered_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user', default=None)
    approved_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='admin', default=None)

    def __str__(self):
        return str(self.id)

    def is_expired(self):
        return self.expected_return_date < datetime.now()