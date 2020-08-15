import boto3
from utils.utils import read_file_from_path

def upload_s3(bucket_name, file_name, file_path, **kwargs):
    s3_client = boto3.client('s3')
    try:
        file_data = read_file_from_path(file_path)
        if not file_data:
            print(file_path)
            raise Exception('There is no file data in provided file path')

        upload_result = s3_client.put_object(
            Bucket=bucket_name,
            Body=file_data,
            Key=file_name,
            Metadata=kwargs.get('meta_data', {})
        )
        if ('ResponseMetadata' in upload_result and
                'HTTPStatusCode' in upload_result['ResponseMetadata']):
            return upload_result['ResponseMetadata']['HTTPStatusCode']
        return None
    except Exception as upload_err:
        print('Error while uploading file to s3', upload_err)
        return None
