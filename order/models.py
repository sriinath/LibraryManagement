from django.db import models
from books.models import Books
from users.models import Users
from datetime import timedelta, datetime

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    ordered_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, default=None)
    ordered_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user', default=None)
    status = models.TextField(choices=(('pending', 1), ('approved', 2), ('declined', 3), ('done', 4)), default='pending')
    is_cancelled = models.BooleanField(default=False)
    expected_return_date = models.DateTimeField(null=True, blank=True)
    actual_return_date = models.DateTimeField(null=True, blank=True)
    admin_action_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='order_approval')
    admin_action_at = models.DateTimeField(null=True, blank=True)
    return_approved_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='return_aproval')

    def __str__(self):
        return str(self.id)

    @property
    def is_expired(self):
        if self.expected_return_date is not None:
            return self.expected_return_date < datetime.now()
        else:
            return False