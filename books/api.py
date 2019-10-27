from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, When, Case, Value, BooleanField, F, FilteredRelation
from .models import Books

def get_books(req):
    user_data = req.user
    if(req.method == 'GET'):
        if(hasattr(user_data, 'user_id')):
            user_id = user_data.user_id
            postBody = req.GET
            limit = 10
            offset= 0
            if(postBody):
                limit = int(postBody.get('limit') or limit)
                offset = int(postBody.get('offset') or offset)
            start_idx = offset * limit
            end_idx = start_idx + limit
            books_data = Books.objects.all()[start_idx : end_idx]
            books_data = books_data.annotate(
                count=Count('user_info'),
                user_list=FilteredRelation('order',condition=Q(users__user_id=user_id))
            ).annotate(
                user_count=Count('user_list'),
                expiry_date=F('user_list__end_date'),
                stock=F('stock_count') - F('count')
            ).annotate(
                user_bought=Case(
                    When(
                        user_count__gt=0, then=Value(True)
                    ),
                    default=Value(False),
                    output_field=BooleanField()
                ),
                is_expired=Case(
                    When(
                        expiry_date__lt=timezone.now(), then=Value(True)
                    ),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).values(
                'book_id',
                'name',
                'description',
                'author',
                'user_bought',
                'expiry_date',
                'stock',
                'is_expired'
            )
            return JsonResponse({
                'data': list(books_data),
                'status': 'success'
            },
            status=200,
            safe=False
            )
        else:
            return JsonResponse({
                'status': 'failure',
                'message': 'Need to sign in to access this API. No user id found'
            },
            status=456
            )
    return HttpResponse('Sending HTTP response since it is not post request')