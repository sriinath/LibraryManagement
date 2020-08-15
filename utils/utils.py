import os
import pandas as pd
import requests

from constants import QUEUE_HEADERS, QUEUE_URL

def read_file_from_path(file_path, mode='buffer'):
    """
    read the contents from the provided path and return the contents as buffer
    """
    if file_path is not None:
        read_mode = 'rb' if mode == 'buffer' else 'r'
        try:
            with open(file_path, read_mode) as data_stream:
                buffer = None
                while True:
                    data = data_stream.read(1024)
                    if not data:
                        break
                    if buffer is None:
                        buffer = data
                    else:
                        buffer += data
                return buffer
        except Exception as file_err:
            print('Failure in opening and processing file in path', file_path)
            print('File path error', file_err)
            return None
    else:
        print('File path is necessary to read data')
        return None

def is_valid_protocol(url):
    return url.startswith(('http://', 'https://'))

def create_write_path(folder_path, file_name):
    cur_dir = os.getcwd()
    batch_file_path = cur_dir + folder_path
    if not os.path.exists(batch_file_path):
        os.mkdir(batch_file_path)
    return batch_file_path + file_name

def get_csv_contents(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as csv_err:
        print('Failure in reading csv data', csv_err)
        return None

def push_to_queue(topic, data):
    return requests.post(
        QUEUE_URL,
        headers=QUEUE_HEADERS,
        json=dict(
            topic=topic,
            data=data
        )
    )
