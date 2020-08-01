from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, When, Case, Value, BooleanField, F, FilteredRelation, IntegerField
from .models import Books
from django.contrib.auth.decorators import permission_required

@permission_required('books.view_books', raise_exception=True)
def get_books(req):
    if(req.method == 'GET'):
        params = req.GET
        user_id = params.get('user_id')
        if user_id is not None:
            limit = int(params.get('limit', 10))
            offset = int(params.get('offset', 0))
            start_idx = offset * limit
            end_idx = start_idx + limit
            books_data = Books.objects.all()
            total_count = books_data.count()
            filtered_books_data = books_data[start_idx : end_idx]
            books_data = list(filtered_books_data.values(
                'id',
                'title',
                'description',
                'author'
            ))

            for index, books in enumerate(filtered_books_data):
                orders = books.valid_orders
                temp_curr_book =  books_data[index]
                temp_curr_book['stock_left'] = books.available_stock
                if orders is not None:
                    user_order=orders.filter(ordered_by=user_id).all()
                    if user_order and user_order.exists():
                        temp_curr_book['is_expired'] = user_order[0].is_expired
                        temp_curr_book['expiry_date'] = user_order[0].expected_return_date
                books_data[index]=temp_curr_book

            return JsonResponse({
                'data': books_data,
                'count': total_count,
                'status': 'success'
            },
            status=200,
            safe=False
            )
        else:
            return JsonResponse({
                'message': 'User id is mandatory to get the books',
                'status': 'success'
            }, status = 422)

    return HttpResponse('Sending HTTP response since it is not post request')