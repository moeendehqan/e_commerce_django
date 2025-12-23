import os
from storages.backends.s3boto3 import S3Boto3Storage

class MinioStorage(S3Boto3Storage):
    """
    Custom storage for MinIO.
    Usage in models:
    from utiles.storage import MinioStorage
    
    class MyModel(models.Model):
        image = models.ImageField(storage=MinioStorage(), ...)
    """
    def __init__(self, *args, **kwargs):
        self.access_key = os.getenv('MINIO_ACCESS_KEY', 'ZLFRbZgCfaFyEnDO3PrF')
        self.secret_key = os.getenv('MINIO_SECRET_KEY', 'JB43qVgVfAk1eFbFoHsslqpSrzvXhWcrPY1qtIqS')
        self.bucket_name = os.getenv('MINIO_BUCKET_NAME', 'woocammers')
        self.endpoint_url = os.getenv('MINIO_ENDPOINT', 'https://minio.shikala.com/')
        self.region_name = os.getenv('MINIO_REGION', 'us-east-1')
        self.use_ssl = os.getenv('MINIO_USE_SSL', 'true').lower() == 'true'
        
        # S3Boto3Storage init configuration
        kwargs['access_key'] = self.access_key
        kwargs['secret_key'] = self.secret_key
        kwargs['bucket_name'] = self.bucket_name
        kwargs['endpoint_url'] = self.endpoint_url
        kwargs['region_name'] = self.region_name
        kwargs['use_ssl'] = self.use_ssl
        kwargs['verify'] = self.use_ssl # Verify SSL only if using SSL
        
        # MinIO-specific settings
        kwargs['custom_domain'] = os.getenv('MINIO_CUSTOM_DOMAIN', None)
        kwargs['file_overwrite'] = False
        kwargs['signature_version'] = 's3v4'
        kwargs['addressing_style'] = 'path'
        
        super().__init__(*args, **kwargs)