from django.http import HttpResponse, JsonResponse
from datetime import datetime
from users.models import get_item as get_user
from books.models import get_item as get_book
from books.models import Books
from users.models import Users
from .models import Order
from django.db.models import F, When, Case, Value, IntegerField, FilteredRelation, Q, BooleanField, Count, Sum
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/login')
def add_book(req):
    if(req.method == 'POST'):
        postBody = req.POST
        if(postBody):
            user_id = postBody.get('user_id')
            book_id = postBody.get('book_id')
            try:
                bookObj = get_book(item_id=book_id)
                userObj = get_user(item_id=user_id)
                result = add_order(userObj=userObj, bookObj=bookObj)
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
                        'message': 'Successfully added book to the order'
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
                    'message': 'Book does not exist with' + str(book_id)
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
        filter_user_book = Order.objects.filter(Q(status='approved') | Q(status='pending'), book=bookObj, ordered_by=userObj)
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
        status = get_params.get('status')
        if user_id is not None and status is not None:
            try:
                user_order = get_order_info('id', 'ordered_at', 'expected_return_date', 'ordered_by', 'status', ordered_by=user_id, status=status)
                order_info = user_order.annotate(
                    name=F('book__title'),
                    author=F('book__author'),
                    price=F('book__price'),
                    is_expired=Case(
                        When(expected_return_date__lt=datetime.now(), then=Value(True)),
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
                    'admin_action_by'
                )
                return JsonResponse({
                    'data': list(order_info),
                    'status': 'success'
                },
                status=200
                )
            except Order.DoesNotExist:      
                return JsonResponse({
                    'status': 'failure',
                    'message': 'Order does not exist'
                },
                status=404
                )
        else:
            return JsonResponse({
                'message': 'User id is mandatory to calculate the total orders',
                'status': 'success'
            }, status = 422)

    return HttpResponse('Sending HTTP response since it is not post request')

def get_order_info(*args, **kwargs):
    order_info = Order.objects.filter(**kwargs).values(*args)
    if order_info.exists():
        return order_info
    else:
        raise Order.DoesNotExist

def get_order_by_user(user_id, *args, **kwargs):
    if user_id is not None:
        try:
            get_user(item_id=user_id)
            return get_order_info(*args, ordered_by=user_id, **kwargs)
        except Users.DoesNotExist:
            raise Users.DoesNotExist
    raise Exception('User id is mandatory and cannot be empty')

def get_order_by_id(order_id):
    if order_id is not None:
        return Order.objects.get(id=order_id)
    raise Exception('Order id is manatory')


@login_required(login_url='/login')
def get_total_order_by_user(req):
    if req.method == 'GET':
        user_id = req.GET.get('user_id')
        if user_id is not None:
            try:
                order_info = get_order_info('status', ordered_by=user_id)
                order_info_count=order_info.annotate(
                    approved_count = Count('id', filter=Q(status='approved')),
                    pending_count = Count('id', filter=Q(status='pending')),
                    declined_count = Count('id', filter=Q(status='declined'))
                ).values(
                    'approved_count',
                    'pending_count',
                    'declined_count'
                ).aggregate(
                    approved = Sum('approved_count'),
                    pending = Sum('pending_count'),
                    declined = Sum('declined_count'),
                )
                return JsonResponse({
                    'data': dict(order_info_count),
                    'status': 'success'
                }, status = 200)
            except Order.DoesNotExist:      
                return JsonResponse({
                    'status': 'failure',
                    'message': 'Order does not exist'
                },
                status=404
                )
        else:
            return JsonResponse({
                'message': 'User id is mandatory to calculate the total orders',
                'status': 'success'
            }, status = 422)
    return HttpResponse('Sending HTTP response since it is not post request')    

def get_outstanding_balance_by_user(req):
    if req.method == 'GET':
        user_id = req.GET.get('user_id')
        outstanding_days = 0
        try:
            order_info = get_order_by_user(user_id, ordered_at__day__lt=datetime.now().day)
            order_result = order_info.annotate(
                outstanding_days = Sum(datetime.now() - F('ordered_at'))
            ).values(
                'outstanding_days'
            )
            if order_result is not None and '0.outstanding_days.day' in order_result[0]:
                outstanding_days = order_result[0]['outstanding_days'].day
            return JsonResponse({
                'balance': outstanding_days,
                'status': 'success'
            }, status = 200)
        except Users.DoesNotExist:
                return JsonResponse({
                    'status': 'failure',
                    'message': 'User does not exist with' + str(user_id)
                },
                status=404
                )
        except Order.DoesNotExist:      
            return JsonResponse({
                'status': 'failure',
                'message': 'Order does not exist'
            },
            status=404
            )
        except Exception as e:
            print(e)
            return JsonResponse({
                'message': 'Something went wrong while getting outstanding balance for account. Make sure params are valid',
                'status': 'failure'
            }, status = 422)

    return HttpResponse('Sending HTTP response since it is not post request')

def manage_order(req):
    if req.method == 'PUT':
        reqBody = json.loads(req.body)
        user_id = reqBody.get('user_id')
        order_id = reqBody.get('order_id')
        action = reqBody.get('action')
        if user_id is not None and order_id is not None:
            user_id = int(user_id)
            order_id = int(order_id)
            # Need to add role based functionalities
            try:
                user_order = get_order_by_id(order_id)
                if action is not None:
                    if action == 'delete':
                        # Check if the request from user and vaildate updating his own orders
                        req_user_id = req.user.id
                        if req_user_id is not None and user_id == req_user_id and user_order.ordered_by_id == req_user_id:
                            # User based order update flow
                            user_order.status = 'done'
                            user_order.is_cancelled = True
                            user_order.actual_return_date = datetime.now()
                            user_order.save()
                            return JsonResponse({
                                'message': 'Successfully removed the order from the list',
                                'status': 'success'
                            }, status = 200)
                        else:
                            return JsonResponse({
                                'message': 'User cannot update someone elses order',
                                'status': 'failure'
                            }, status = 403)
                    elif action == 'approve':
                        pass
                    elif action == 'decline':
                        pass
                    elif action == 'accepted':
                        pass
                    else:
                        return JsonResponse({
                            'message': 'Action provided is invalid',
                            'status': 'failure'
                        }, status = 412)
                else:
                    return JsonResponse({
                        'message': 'action is mandatory to update order',
                        'status': 'failure'
                    }, status = 422)
            except Users.DoesNotExist:
                return JsonResponse({
                    'status': 'failure',
                    'message': 'User does not exist with' + str(user_id)
                },
                status=404
                )
            except Order.DoesNotExist:      
                return JsonResponse({
                    'status': 'failure',
                    'message': 'Order does not exist with' + str(order_id)
                },
                status=404
                )
        else:
            return JsonResponse({
                'message': 'User id and order id is mandatory to update order',
                'status': 'failure'
            }, status = 422)
    return HttpResponse('Sending HTTP response since it is not post request')    