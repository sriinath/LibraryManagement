from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from users.models import get_item as get_user
from books.models import get_item as get_book
from books.models import Books
from users.models import Users
from .models import Order
from django.db.models import F, When, Case, Value, IntegerField, FilteredRelation, Q, BooleanField

def add_book(req):
    if(req.method == 'POST'):
        postBody = req.POST
        if(postBody):
            user_id = postBody.get('user_id')
            book_id = postBody.get('book_id')
            try:
                bookIns = get_book(item_id=book_id)
                try:
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
    st_date = timezone.now()
    en_date = st_date + timezone.timedelta(days=15)
    try:
        filter_user_book = Order.objects.filter(books=bookObj, users=userObj)
        if(not filter_user_book.exists()):
            try:
                order = Order(start_date=st_date, end_date=en_date, books=bookObj, users=userObj)
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

def get_order_details(req):
    if(req.method == 'GET'):
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