from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from users.models import get_item as get_user
from books.models import get_item as get_book
from books.models import Books
from users.models import Users
from .models import Order
from django.db.models import F, When, Case, Value, IntegerField, FilteredRelation, Q, BooleanField, Count
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def add_book(req):
    if(req.method == 'POST'):
        postBody = req.POST
        if(postBody):
            user_id = postBody.get('user_id')
            book_id = postBody.get('book_id')
            try:
                bookIns = get_book(item_id=book_id)
                userIns = get_user(item_id=user_id)
                result = add_order(userObj=userIns, bookObj=bookIns)
                if(result):
                    return JsonResponse({
                        'status': 'failure',
                        'message': result
                    },
                    status=422
                    )
                else:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Success from add_order'
                    },
                    status=200
                    )
            except Users.DoesNotExist:
                return JsonResponse({
                    'status': 'failure',
                    'message': 'User does not exist with' + str(user_id)
                },
                status=404
                )
            except Books.DoesNotExist:      
                return JsonResponse({
                    'status': 'failure',
                    'message': 'Book does not exist with' + str(user_id)
                },
                status=404
                )
        else:
            return JsonResponse({
                'status': 'failure',
                'message': 'Post Body params are mandatory'
            },
            status=422
            )
    return HttpResponse('Sending HTTP response since it is not post request')

def add_order(userObj, bookObj):
    try:
        filter_user_book = Order.objects.filter(book=bookObj, ordered_by=userObj)
        if(not filter_user_book.exists()):
            try:
                order = Order(book=bookObj, ordered_by=userObj)
                order.save()
                return ''
            except Exception as e:
                print(e)
                return e
        else:
            return 'The book selected was already in your order'
    except Exception as e:
        print(e)
        return e

@login_required(login_url='/login')
def get_order_details(req):
    if(req.method == 'GET'):
        get_params = req.GET
        user_id = int(get_params.get('user_id'))
        status = int(get_params.get('status'))
        if user_id is not None and status is not None:
            user_order = get_order_info('id', 'ordered_at', 'expected_return_date', 'ordered_by', 'status', ordered_by=user_id, status=status)
            order_info = user_order.annotate(
                name=F('book__title'),
                author=F('book__author'),
                price=F('book__price'),
                is_expired=Case(
                    When(expected_return_date__lt=timezone.now(), then=Value(True)),
                    default=False,
                    output_field=BooleanField()
                )
            ).values(
                'id',
                'ordered_at',
                'price',
                'expected_return_date',
                'name',
                'author',
                'is_expired',
                'status',
                'approved_by'
            )
            return JsonResponse({
                'data': list(order_info),
                'status': 'success'
            },
            status=200
            )
        else:
            return JsonResponse({
                'message': 'User id is mandatory to calculate the total orders',
                'status': 'success'
            }, status = 422)

    return HttpResponse('Sending HTTP response since it is not post request')

def get_order_info(*args, **kwargs):
    order_info = Order.objects.filter(**kwargs).values(*args)
    return order_info

def get_order_by_user(user_id, *args):
    if user_id is not None:
        order_info = get_order_info(*args, ordered_by=user_id)
        return order_info
    return dict()

@login_required(login_url='/login')
def get_total_order_by_user(req):
    if req.method == 'GET':
        user_id = req.GET.get('user_id')
        if user_id is not None:
            order_info = get_order_info(('id'), ordered_by=user_id)
            order_info_count=order_info.annotate(
                approved = Count('id', filter=Q(status=2)),
                pending = Count('id', filter=Q(status=1)),
                declined = Count('id', filter=Q(status=3))
            ).values(
                'approved',
                'pending',
                'declined'
            )     
            return JsonResponse({
                'data': dict(order_info_count[0]),
                'status': 'success'
            }, status = 200)
        else:
            return JsonResponse({
                'message': 'User id is mandatory to calculate the total orders',
                'status': 'success'
            }, status = 422)
    return HttpResponse('Sending HTTP response since it is not post request')    

# def get_outstanding_balance_by_user(req):
#     if req.method == 'GET':
#         user_id = req.GET.get('user_id')

#         if user_id is not None:
#             order_info = get_order_by_user(user_id, ('expected_return_date', 'status'))

#             print(order_info)
#             if order_info:
#     return HttpResponse('Sending HTTP response since it is not post request')