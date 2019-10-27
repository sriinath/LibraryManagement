from django.shortcuts import render
from django.db.models import F, Sum
from django.utils import timezone
# Create your views here.

def index(req):
    userData = req.user
    if(userData.is_authenticated):
        user_id = userData.user_id
        order_info = userData.order_set
        total_count = order_info.filter(
            end_date__lt=timezone.now()
        ).aggregate(count= Sum(F('end_date') - timezone.now().date()))
        data = {
            'is_authenticated': userData.is_authenticated,
            'user': userData,
            'order_count': order_info.count(),
            'balance': abs(total_count['count'] * 5) or 0,
            'user_id': user_id
        }
    else:
        data = {
            'is_authenticated': userData.is_authenticated
        }
    return render(req, 'orders/my_orders.html', data)