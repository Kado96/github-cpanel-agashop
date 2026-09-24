from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseStorageProvider(ABC):
    """Abstract interface for storage providers."""

    @abstractmethod
    def upload(self, shop_id: str, file_data: bytes, destination_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Upload a file to the storage.
        
        Args:
            shop_id (str): The shop identifier for tenant isolation.
            file_data (bytes): The raw bytes of the file.
            destination_path (str): The desired path/filename in the storage.
            metadata (Optional[Dict[str, Any]]): Additional metadata to store with the file.
            
        Returns:
            Dict[str, Any]: Information about the uploaded file, including its ID and URL.
        """
        pass

    @abstractmethod
    def download(self, file_id: str) -> bytes:
        """
        Download a file from the storage.
        
        Args:
            file_id (str): The identifier of the file to download.
            
        Returns:
            bytes: The raw bytes of the downloaded file.
        """
        pass

    @abstractmethod
    def delete(self, file_id: str) -> bool:
        """
        Delete a file from the storage.
        
        Args:
            file_id (str): The identifier of the file to delete.
            
        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def get_url(self, file_id: str) -> str:
        """
        Get the public or signed URL for a file.
        
        Args:
            file_id (str): The identifier of the file.
            
        Returns:
            str: The URL to access the file.
        """
        pass

    @abstractmethod
    def get_metadata(self, file_id: str) -> Dict[str, Any]:
        """
        Get metadata for a file.
        
        Args:
            file_id (str): The identifier of the file.
            
        Returns:
            Dict[str, Any]: The metadata of the file.
        """
        pass
