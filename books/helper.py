import json
import requests

from utils.utils import get_csv_contents, push_to_queue
from constants import MAXIMUM_ITEMS_PER_QUEUE

def add_product_to_queue(csv_path):
    csv_data = get_csv_contents(csv_path)
    failed_products = list()
    if csv_data is not None:
        csv_dict = json.loads(csv_data.to_json(orient='records'))
        for curr_index in range(0, len(csv_dict), MAXIMUM_ITEMS_PER_QUEUE):
            products = csv_dict[curr_index: curr_index + MAXIMUM_ITEMS_PER_QUEUE]
            req = push_to_queue(
                'digest_products',
                products
            )
            if not req.ok:
                failed_products += products
