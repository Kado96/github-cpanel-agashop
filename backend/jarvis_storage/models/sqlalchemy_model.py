from sqlalchemy import Column, String, Integer, BigInteger, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class FileMetadata(Base):
    """SQLAlchemy model for storing file metadata."""
    __tablename__ = 'file_metadata'

    id = Column(String(255), primary_key=True)
    provider_file_id = Column(String(255), index=True, nullable=False)
    file_name = Column(String(255), nullable=False)
    mime_type = Column(String(100))
    size_bytes = Column(BigInteger)
    url = Column(String(1024))
    thumbnail_url = Column(String(1024))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<FileMetadata(id='{self.id}', file_name='{self.file_name}')>"
