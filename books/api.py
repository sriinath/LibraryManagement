import os
import json
import requests
from datetime import datetime
import time
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q, Count, When, Case, Value, BooleanField, F, FilteredRelation, IntegerField
from django.contrib.auth.decorators import permission_required
from django.db.utils import IntegrityError
from django.views.decorators.http import require_http_methods

from CustomException import CustomException, exception_handler
from utils.S3_utils import upload_s3, get_object
from utils.utils import is_valid_protocol, create_write_path
from .models import Books, get_item
from .helper import add_product_to_queue
from constants import BUCKET_NAME


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
@permission_required('books.add_books', raise_exception=True)
def create_books(req):
    params = req.POST
    title = params.get('title')
    desc = params.get('description')
    author = params.get('author')
    stock = params.get('stock')
    price = params.get('price')
    try:
        book = Books(
            title=title,
            description=desc,
            author=author,
            stock=stock,
            price=price
        )
        book.save()
        return JsonResponse({
            'message': 'Successfully added the book to list',
            'status': 'success'
        }, status = 201)
    except IntegrityError:
        return JsonResponse({
            'message': 'Please make sure you passed all the required fields',
            'status': 'failure'
        }, status = 412)
    except Exception as e:
        print(e)
        return JsonResponse({
            'message': 'Something went wrong while processing your reqeuest',
            'status': 'failure'
        }, status = 500)


@require_http_methods(["POST"])
@permission_required('books.change_books', raise_exception=True)
def update_books(req):
    if(req.method == 'PUT'):
        reqBody = json.loads(req.body)
        book_id = reqBody.get('id')
        stock = reqBody.get('stock')
        price = reqBody.get('price')
        try:
            book = get_item(item_id=book_id)
            if book is not None:
                book.stock = stock
                book.price = price
                book.save()
            else:
                return JsonResponse({
                    'message': 'There is no book with the id provided',
                    'status': 'failure'
                }, status = 422)
        except IntegrityError:
            return JsonResponse({
                'message': 'Please make sure you passed all the required fields',
                'status': 'failure'
            }, status = 412)
        except Exception as e:
            print(e)
            return JsonResponse({
                'message': 'Something went wrong while processing your reqeuest',
                'status': 'failure'
            }, status = 422)


@require_http_methods(["POST"])
@exception_handler
def upload_product_data(request):
    csv_file = request.FILES.get('product_data')
    if not csv_file:
        raise CustomException(400, 'File data is not available to process')
    
    file_name = csv_file.name
    file_type = os.path.splitext(file_name)[1] if file_name else None
    if not file_type or file_type.lower() != '.csv':
        raise CustomException(400, 'Uploaded file is not a valid file type')
    
    temp_file_path = create_write_path('/batches/') + file_name
    with open(temp_file_path, 'wb+') as destination_file:
        for chunk in csv_file.chunks():
            destination_file.write(chunk)
    
    upload_data = upload_s3(BUCKET_NAME, file_name, temp_file_path)
    os.remove(temp_file_path)
    if upload_data == 200:
        return JsonResponse({
            'status': 'success'
        }, status = 200)

    return JsonResponse({
        'message': 'Something went wrong while uploading your file to process',
        'status': 'failure'
    }, status = 422)


@require_http_methods(["POST"])
@exception_handler
def process_product_data(request):
    message_type = request.headers.get('x-amz-sns-message-type')
    payload = json.loads(request.body)

    if message_type in ('SubscriptionConfirmation', 'UnsubscribeConfirmation'):
        subscriber_url = payload.get('SubscribeURL')
        print('subscriber url is: ', subscriber_url)
        return HttpResponse(status=200)
    elif message_type == 'Notification':
        s3_body = payload.get('Message', '')
        if s3_body:
            parsed_message = json.loads(s3_body)
            records = parsed_message.get('Records', [])
            for data in records:
                s3_key = data.get('s3', {}).get('object', {}).get('key', '').replace('+', ' ')
                if s3_key:
                    s3_object = get_object(BUCKET_NAME, s3_key)
                    temp_file_name = '{}_{}'.format(int(time.time()), s3_key)
                    temp_file_path = create_write_path('/process_batches/') + temp_file_name

                    with open(temp_file_path, 'wb+') as destination_file:
                        for chunk in s3_object.iter_chunks():
                            destination_file.write(chunk)

                    add_product_to_queue(temp_file_path)
                    os.remove(temp_file_path)

        return JsonResponse({
            'status': 'success'
        })
    else:
        return CustomException(400, 'Unknown message type')
