from typing import Optional
from pydantic import BaseModel, Field


class StorageConfig(BaseModel):
    """Configuration for the storage SDK."""
    provider: str = Field(default="local", description="The storage provider to use (e.g., 'local', 'google_drive').")
    
    # Google Drive specific
    google_drive_credentials_json: Optional[str] = Field(default=None, description="Path to the Google Service Account credentials JSON file.")
    google_drive_shared_drive_id: Optional[str] = Field(default=None, description="The ID of the Shared Drive, if applicable.")
    
    # Local specific
    local_storage_path: Optional[str] = Field(default="./local_storage", description="The base path for local storage.")
    
    # Image processing specific
    image_max_width: int = Field(default=1920, description="Maximum width for compressed images.")
    image_max_height: int = Field(default=1080, description="Maximum height for compressed images.")
    thumbnail_width: int = Field(default=300, description="Width for generated thumbnails.")
    thumbnail_height: int = Field(default=300, description="Height for generated thumbnails.")
    image_quality: int = Field(default=85, description="JPEG quality for compressed images.")
