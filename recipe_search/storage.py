"""
Allows the multiple configuration of different types of storage in a single S3 bucket
"""
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class StaticStorage(S3StaticStorage):
    """Static files storage configuration"""
    bucket_name = 'viteunerecette-statics'


class MediaStorage(S3Boto3Storage):
    """User file storage configuration"""
    bucket_name = 'viteunerecette-assets'
    file_overwrite = False
