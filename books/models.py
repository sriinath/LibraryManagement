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
    
    @property
    def order_ref(self):
        return self.order_set

    @property
    def order_list(self):
        return self.order_ref.all()

    @property
    def valid_orders(self):
        if self.order_ref is not None:
            return self.order_ref.filter(status='approved')
        return None

    @property
    def available_stock(self):
        approved_orders = 0
        if self.valid_orders is not None:
            approved_orders = self.valid_orders.count()
        return self.stock - approved_orders

def get_item(item_id):
    return Books.objects.get(pk=item_id)