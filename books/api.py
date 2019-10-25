from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count, When, Case, Value, BooleanField, F
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
                limit = postBody.get('limit')
                offset = postBody.get('offset')
            start_idx = offset * limit
            end_idx = start_idx + limit
            books_data = Books.objects.all()[start_idx : end_idx]
            books_data = books_data.annotate(
                count=Count('user_info'),
                user_count=Count('user_info',condition=Q(user_info__user_id=user_id))
            ).annotate(
                user_bought= Case(
                    When(
                        user_count__gt=0, then=Value(True)
                    ),
                    default=Value(False),
                    output_field=BooleanField()
                ),
                in_stock=Case(
                    When(
                        count__lt=F('stock_count'), then=Value(True)
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
                'in_stock'
            )
            return JsonResponse(list(books_data), safe=False)
        else:
            return JsonResponse({
                'status': 'failure',
                'message': 'Need to sign in to access this API. No user id found'
            },
            status=456
            )
    return HttpResponse('Sending HTTP response since it is not post request')