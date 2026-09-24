import os
import uuid
from typing import Any, Dict, Optional
from ..core.interface import BaseStorageProvider
from ..core.exceptions import FileNotFoundStorageError

class LocalStorageProvider(BaseStorageProvider):
    """Local file system implementation for development and testing."""

    def __init__(self, base_path: str = "./local_storage"):
        self.base_path = os.path.abspath(base_path)
        os.makedirs(self.base_path, exist_ok=True)

    def _get_full_path(self, destination_path: str) -> str:
        # Prevent directory traversal
        full_path = os.path.abspath(os.path.join(self.base_path, destination_path))
        if os.path.commonpath([os.path.abspath(self.base_path), os.path.abspath(full_path)]) != os.path.abspath(self.base_path):
            raise ValueError("Invalid destination path.")
        return full_path

    def upload(self, shop_id: str, file_data: bytes, destination_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        import re
        if not re.match(r'^[\w\-]+$', shop_id):
            raise ValueError(f"Invalid shop_id format: {shop_id}")
            
        destination_path = f"shops/{shop_id}/{destination_path.lstrip('/')}"
        full_path = self._get_full_path(destination_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "wb") as f:
            f.write(file_data)
            
        file_id = destination_path # Using path as ID for simplicity
        
        return {
            "id": file_id,
            "url": f"file://{full_path}",
            "path": destination_path,
            "size": len(file_data)
        }

    def download(self, file_id: str) -> bytes:
        full_path = self._get_full_path(file_id)
        if not os.path.exists(full_path):
            raise FileNotFoundStorageError(f"File {file_id} not found.")
            
        with open(full_path, "rb") as f:
            return f.read()

    def delete(self, file_id: str) -> bool:
        full_path = self._get_full_path(file_id)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

    def get_url(self, file_id: str) -> str:
        full_path = self._get_full_path(file_id)
        return f"file://{full_path}"

    def get_metadata(self, file_id: str) -> Dict[str, Any]:
        full_path = self._get_full_path(file_id)
        if not os.path.exists(full_path):
            raise FileNotFoundStorageError(f"File {file_id} not found.")
            
        stat = os.stat(full_path)
        return {
            "id": file_id,
            "size": stat.st_size,
            "created_at": stat.st_ctime,
            "updated_at": stat.st_mtime
        }
