from typing import Any, Dict, Optional
import os

from .core.config import StorageConfig
from .core.interface import BaseStorageProvider
from .providers.local import LocalStorageProvider
from .providers.google_drive import GoogleDriveProvider
from .processing.image import ImageProcessor


class StorageService:
    """Facade for the storage SDK, orchestrating provider and image processing."""

    def __init__(self, config: Optional[StorageConfig] = None):
        self.config = config or StorageConfig()
        self.provider = self._initialize_provider()
        self.image_processor = ImageProcessor(
            max_width=self.config.image_max_width,
            max_height=self.config.image_max_height,
            thumb_width=self.config.thumbnail_width,
            thumb_height=self.config.thumbnail_height,
            quality=self.config.image_quality
        )

    def _initialize_provider(self) -> BaseStorageProvider:
        if self.config.provider == "google_drive":
            if not self.config.google_drive_credentials_json:
                raise ValueError("google_drive_credentials_json is required for google_drive provider.")
            return GoogleDriveProvider(
                credentials_json=self.config.google_drive_credentials_json,
                shared_drive_id=self.config.google_drive_shared_drive_id
            )
        else:
            return LocalStorageProvider(base_path=self.config.local_storage_path)

    def upload_file(self, shop_id: str, file_data: bytes, destination_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Uploads a raw file."""
        return self.provider.upload(shop_id, file_data, destination_path, metadata)

    def upload_image(self, shop_id: str, image_data: bytes, base_destination_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Processes and uploads an image along with its thumbnail.
        
        Args:
            shop_id (str): The shop identifier for tenant isolation.
            image_data (bytes): The raw image bytes.
            base_destination_path (str): The destination path for the main image.
            metadata (Optional[Dict[str, Any]]): Metadata to attach.
            
        Returns:
            Dict[str, Any]: Information about the uploaded images.
        """
        compressed_bytes, thumbnail_bytes = self.image_processor.process_image(image_data)
        
        # Upload main image
        main_result = self.provider.upload(shop_id, compressed_bytes, base_destination_path, metadata)
        
        # Determine thumbnail path
        dir_name, file_name = os.path.split(base_destination_path)
        name, ext = os.path.splitext(file_name)
        thumb_path = os.path.join(dir_name, f"{name}_thumb{ext}").replace('\\', '/')
        
        # Upload thumbnail
        thumb_result = self.provider.upload(shop_id, thumbnail_bytes, thumb_path, metadata)
        
        return {
            "main": main_result,
            "thumbnail": thumb_result
        }

    def download_file(self, file_id: str) -> bytes:
        return self.provider.download(file_id)

    def delete_file(self, file_id: str) -> bool:
        return self.provider.delete(file_id)

    def get_file_url(self, file_id: str) -> str:
        return self.provider.get_url(file_id)

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        return self.provider.get_metadata(file_id)
