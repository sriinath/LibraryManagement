from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from users.models import get_item as get_user
from books.models import get_item as get_book
from books.models import Books
from users.models import Users
from .models import Order
from django.db.models import F, When, Case, Value, IntegerField, FilteredRelation, Q, BooleanField
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
                        'status': 'success',
                        'message': 'Success from add_order'
                    },
                    status=200
                    )
                else:
                    return JsonResponse({
                        'status': 'failure',
                        'message': 'Failed to add the book to order'
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
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False

@login_required(login_url='/login')
def get_order_details(req):
    if(req.method == 'POST'):
        user_info = req.user
        order_info = user_info.order_set.annotate(
            name=F('books__name'),
            author=F('books__author'),
            due_date=F('end_date'),
            is_expired=Case(
                When(end_date__lt=timezone.now(), then=Value(True)),
                default=False,
                output_field=BooleanField()
            ),
            outstanding_days=Case(
                When(end_date__lt=timezone.now(), then=F('end_date') - timezone.now().date()),
                output_field=IntegerField()
            )
        ).values(
            'start_date',
            'end_date',
            'name',
            'author',
            'outstanding_days',
            'is_expired'
        )
        return JsonResponse({
            'data': list(order_info),
            'status': 'success'
        },
        status=200
        )
    return HttpResponse('Sending HTTP response since it is not post request')

def get_order_by_user(user_id, values):
    if user_id is not None and values is not None:
        order_info = Order.objects.filter(ordered_by=user_id).values(values)        
        print(order_info)
        return order_info
    return dict()

@login_required(login_url='/login')
def get_total_order_by_user(req):
    if req.method == 'GET':
        user_id = req.GET.get('user_id')
        order_info_count = 0
        if user_id is not None:
            order_info_count = get_order_by_user(user_id, ('id')).count()        
            return JsonResponse({
                'count': order_info_count,
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