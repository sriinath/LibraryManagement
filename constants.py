import os

MAXIMUM_ITEMS_PER_QUEUE = 200
QUEUE_URL = os.environ.get('QUEUE_URL')
QUEUE_API_KEY = os.environ.get('QUEUE_API_KEY')
QUEUE_HEADERS = {
    'Authorization': QUEUE_API_KEY
}

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'library-management-data')
