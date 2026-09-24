from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.shops.models import FileMetadata, Product
from django.conf import settings
try:
    from jarvis_storage.core.storage_service import StorageService
    from jarvis_storage.providers.local import LocalStorageProvider
    from jarvis_storage.providers.google_drive import GoogleDriveProvider
    from jarvis_storage.providers.supabase_s3 import SupabaseS3Provider
except ImportError:
    StorageService = None

class MediaUploadView(APIView):
    def post(self, request, shop_id, product_id, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        uploaded_file = request.FILES['file']
        
        if StorageService is None:
             return Response({"error": "Storage SDK not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             
        # Initialize provider
        provider_name = getattr(settings, 'STORAGE_PROVIDER', 'LOCAL')
        if provider_name == 'SUPABASE_S3':
            endpoint_url = getattr(settings, 'SUPABASE_S3_ENDPOINT_URL', '')
            access_key_id = getattr(settings, 'SUPABASE_S3_ACCESS_KEY_ID', '')
            secret_access_key = getattr(settings, 'SUPABASE_S3_SECRET_ACCESS_KEY', '')
            bucket_name = getattr(settings, 'SUPABASE_S3_BUCKET_NAME', 'media')
            region_name = getattr(settings, 'SUPABASE_S3_REGION_NAME', 'eu-west-1')
            provider = SupabaseS3Provider(
                endpoint_url=endpoint_url,
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                bucket_name=bucket_name,
                region_name=region_name
            )
        elif provider_name == 'GOOGLE_DRIVE':
            credentials_path = getattr(settings, 'GOOGLE_APPLICATION_CREDENTIALS', '')
            shared_drive_id = getattr(settings, 'GOOGLE_DRIVE_SHARED_DRIVE_ID', None)
            provider = GoogleDriveProvider(credentials_json=credentials_path, shared_drive_id=shared_drive_id)
        else:
            base_path = getattr(settings, 'LOCAL_STORAGE_BASE_PATH', 'media/sdk_storage')
            provider = LocalStorageProvider(base_path=base_path)

            
        storage_service = StorageService(provider=provider)
        
        # Determine path and filename
        path = f"shops/{shop_id}/products/{product_id}"
        file_name = uploaded_file.name
        
        # Read file data
        file_data = uploaded_file.read()
        
        # Upload using SDK
        try:
            result = storage_service.upload_file(
                file_data=file_data,
                file_name=file_name,
                mime_type=uploaded_file.content_type,
                path=path,
                metadata={'shop_id': str(shop_id), 'product_id': str(product_id)}
            )
            
            # Create metadata in DB
            metadata = FileMetadata.objects.create(
                file_name=result.file_name,
                file_size=result.file_size,
                mime_type=result.mime_type,
                file_path=result.path,
                shop_id=shop_id,
                product_id=product_id,
                external_file_id=result.file_id,
                status='UPLOADED'
            )
            
            return Response({
                "id": metadata.id,
                "file_name": metadata.file_name,
                "preview_url": result.preview_url,
                "status": metadata.status
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
