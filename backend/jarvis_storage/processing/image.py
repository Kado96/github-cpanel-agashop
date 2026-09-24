import io
from typing import Tuple
from PIL import Image

class ImageProcessor:
    """Handles image processing: validation, compression, and thumbnail generation."""

    def __init__(self, max_width: int = 1920, max_height: int = 1080, 
                 thumb_width: int = 300, thumb_height: int = 300, quality: int = 85):
        self.max_size = (max_width, max_height)
        self.thumb_size = (thumb_width, thumb_height)
        self.quality = quality

    def process_image(self, file_data: bytes) -> Tuple[bytes, bytes]:
        """
        Process the image by compressing it and generating a thumbnail.
        
        Args:
            file_data (bytes): The raw bytes of the original image.
            
        Returns:
            Tuple[bytes, bytes]: A tuple containing (compressed_bytes, thumbnail_bytes).
            
        Raises:
            ValueError: If the file data cannot be identified as an image.
        """
        try:
            with Image.open(io.BytesIO(file_data)) as img:
                # Convert to RGB if necessary (e.g. RGBA or P)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Create compressed main image
                main_img = img.copy()
                main_img.thumbnail(self.max_size, Image.Resampling.LANCZOS)
                
                quality = self.quality
                while True:
                    main_buffer = io.BytesIO()
                    main_img.save(main_buffer, format="JPEG", quality=quality, optimize=True)
                    compressed_bytes = main_buffer.getvalue()
                    if len(compressed_bytes) <= 1024 * 1024 or quality <= 40:
                        break
                    quality -= 5
                
                # Create thumbnail
                thumb_img = img.copy()
                # Use crop/resize or simple thumbnail; thumbnail preserves aspect ratio
                thumb_img.thumbnail(self.thumb_size, Image.Resampling.LANCZOS)
                
                thumb_quality = self.quality
                while True:
                    thumb_buffer = io.BytesIO()
                    thumb_img.save(thumb_buffer, format="JPEG", quality=thumb_quality, optimize=True)
                    thumbnail_bytes = thumb_buffer.getvalue()
                    if len(thumbnail_bytes) <= 150 * 1024 or thumb_quality <= 40:
                        break
                    thumb_quality -= 5
                
                return compressed_bytes, thumbnail_bytes
        except Exception as e:
            raise ValueError(f"Invalid image data: {str(e)}")
