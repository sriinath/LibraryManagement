import boto3
from utils.utils import read_file_from_path

s3_client = boto3.client('s3')
def upload_s3(bucket_name, file_name, file_path, **kwargs):
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


def get_object(bucket_name, key, **kwargs):
    version = kwargs.get('version', '')
    resp_kwargs = dict()
    if version:
        resp_kwargs.update(VersionId=version)

    try:
        resp = s3_client.get_object(
            Bucket=bucket_name,
            Key=key,
            **resp_kwargs
        )
        status = resp.get('ResponseMetadata', {}).get('HTTPStatusCode', None)
        if status == 200:
            return resp.get('Body', None)
        return None
    except Exception as retreive_err:
        print('Error while retreiving object from s3', retreive_err)
        return None
