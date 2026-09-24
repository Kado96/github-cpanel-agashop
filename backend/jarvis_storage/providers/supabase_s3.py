import re
import os
from typing import Any, Dict, Optional
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from ..core.interface import BaseStorageProvider
from ..core.exceptions import AuthenticationStorageError, FileNotFoundStorageError, StorageError

class SupabaseS3Provider(BaseStorageProvider):
    """
    Supabase Storage Provider via S3 Protocol using boto3.
    """

    def __init__(
        self,
        endpoint_url: str,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str = "media",
        region_name: str = "eu-west-1"
    ):
        if not endpoint_url or not access_key_id or not secret_access_key:
            raise AuthenticationStorageError("Supabase S3 credentials missing (endpoint_url, access_key_id, secret_access_key).")

        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url.rstrip('/')
        
        try:
            self.s3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name,
                config=Config(signature_version='s3v4')
            )
        except Exception as e:
            raise AuthenticationStorageError(f"Failed to initialize Supabase S3 client: {str(e)}")

    def upload(self, shop_id: str, file_data: bytes, destination_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not re.match(r'^[\w\-]+$', shop_id):
            raise ValueError(f"Invalid shop_id format: {shop_id}")

        clean_path = destination_path.lstrip('/')
        file_key = f"shops/{shop_id}/{clean_path}"
        filename = os.path.basename(file_key)

        extra_args = {}
        if metadata and 'mime_type' in metadata:
            extra_args['ContentType'] = metadata['mime_type']

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_data,
                **extra_args
            )
            
            # Construire l'URL publique Supabase Storage
            # Exemple: https://plihtjkucujoeewlzptb.supabase.co/storage/v1/object/public/media/shops/...
            project_ref = self.endpoint_url.split('.')[0].replace('https://', '')
            public_url = f"https://{project_ref}.supabase.co/storage/v1/object/public/{self.bucket_name}/{file_key}"

            return {
                "id": file_key,
                "url": public_url,
                "path": file_key,
                "size": len(file_data)
            }
        except Exception as error:
            raise StorageError(f"Failed to upload to Supabase Storage: {error}")

    def download(self, file_id: str) -> bytes:
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_id)
            return response['Body'].read()
        except ClientError as error:
            if error.response['Error']['Code'] in ('404', 'NoSuchKey'):
                raise FileNotFoundStorageError(f"File {file_id} not found on Supabase Storage.")
            raise StorageError(f"Failed to download from Supabase Storage: {error}")

    def delete(self, file_id: str) -> bool:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_id)
            return True
        except Exception as error:
            raise StorageError(f"Failed to delete file from Supabase Storage: {error}")

    def get_url(self, file_id: str) -> str:
        project_ref = self.endpoint_url.split('.')[0].replace('https://', '')
        return f"https://{project_ref}.supabase.co/storage/v1/object/public/{self.bucket_name}/{file_id}"

    def get_metadata(self, file_id: str) -> Dict[str, Any]:
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=file_id)
            return {
                "content_type": response.get('ContentType'),
                "content_length": response.get('ContentLength'),
                "last_modified": response.get('LastModified'),
                "etag": response.get('ETag')
            }
        except ClientError as error:
            if error.response['Error']['Code'] in ('404', 'NoSuchKey'):
                raise FileNotFoundStorageError(f"File {file_id} not found.")
            raise StorageError(f"Failed to get metadata: {error}")
