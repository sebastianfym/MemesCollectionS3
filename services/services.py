import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import NoCredentialsError
from config.config import settings


def create_bucket_if_not_exists(bucket_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL,
    )
    try:
        s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        raise f"Failed to create bucket {bucket_name}: {e}"


def upload_file_to_s3(file, bucket_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.S3_ACCESS_KEY,
                      aws_secret_access_key=settings.S3_SECRET_KEY,
                      endpoint_url=settings.S3_ENDPOINT_URL,
                      config=Config(signature_version='s3v4'))
    create_bucket_if_not_exists(bucket_name)
    try:
        object_name = f"{uuid.uuid4()}.jpg"
        s3.upload_fileobj(file, bucket_name, object_name)
        return {"url": f"{settings.S3_ENDPOINT_URL}/{bucket_name}/{object_name}"}
    except NoCredentialsError:
        return {"error": "Credentials not available"}
