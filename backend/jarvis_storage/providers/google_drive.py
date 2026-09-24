import io
import os
from typing import Any, Dict, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
from ..core.interface import BaseStorageProvider
from ..core.exceptions import AuthenticationStorageError, FileNotFoundStorageError, StorageError

class GoogleDriveProvider(BaseStorageProvider):
    """Google Drive storage provider using service account credentials."""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    def __init__(self, credentials_json: str, shared_drive_id: Optional[str] = None):
        if not os.path.exists(credentials_json):
            raise AuthenticationStorageError(f"Credentials file not found: {credentials_json}")
            
        try:
            self.creds = service_account.Credentials.from_service_account_file(
                credentials_json, scopes=self.SCOPES)
            self.service = build('drive', 'v3', credentials=self.creds)
        except Exception as e:
            raise AuthenticationStorageError(f"Failed to authenticate with Google Drive: {str(e)}")
            
        self.shared_drive_id = shared_drive_id
        self._folder_cache = {}

    def _get_or_create_folder(self, folder_path: str) -> str:
        """Resolves a folder path to a Google Drive folder ID, creating it if necessary."""
        if folder_path in ("", ".", "/"):
            return self.shared_drive_id or 'root'
            
        if folder_path in self._folder_cache:
            return self._folder_cache[folder_path]
            
        parts = [p for p in folder_path.split('/') if p]
        current_parent = self.shared_drive_id or 'root'
        
        for part in parts:
            query = f"name='{part}' and mimeType='application/vnd.google-apps.folder' and '{current_parent}' in parents and trashed=false"
            
            kwargs = {'q': query, 'spaces': 'drive', 'fields': 'files(id, name)'}
            if self.shared_drive_id:
                kwargs['corpora'] = 'drive'
                kwargs['driveId'] = self.shared_drive_id
                kwargs['includeItemsFromAllDrives'] = True
                kwargs['supportsAllDrives'] = True
                
            results = self.service.files().list(**kwargs).execute()
            items = results.get('files', [])
            
            if items:
                current_parent = items[0]['id']
            else:
                # Create folder
                folder_metadata = {
                    'name': part,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [current_parent]
                }
                create_kwargs = {'body': folder_metadata, 'fields': 'id'}
                if self.shared_drive_id:
                    create_kwargs['supportsAllDrives'] = True
                    
                folder = self.service.files().create(**create_kwargs).execute()
                current_parent = folder.get('id')
                
        self._folder_cache[folder_path] = current_parent
        return current_parent

    def upload(self, shop_id: str, file_data: bytes, destination_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        import re
        if not re.match(r'^[\w\-]+$', shop_id):
            raise ValueError(f"Invalid shop_id format: {shop_id}")
            
        destination_path = f"shops/{shop_id}/{destination_path.lstrip('/')}"
        folder_path = os.path.dirname(destination_path).replace('\\', '/')
        filename = os.path.basename(destination_path)
        
        try:
            folder_id = self._get_or_create_folder(folder_path)
            
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            if metadata:
                file_metadata['properties'] = metadata
                
            media = MediaIoBaseUpload(io.BytesIO(file_data), mimetype='application/octet-stream', resumable=True)
            
            create_kwargs = {
                'body': file_metadata,
                'media_body': media,
                'fields': 'id, webViewLink, webContentLink, name, size'
            }
            if self.shared_drive_id:
                create_kwargs['supportsAllDrives'] = True
                
            file = self.service.files().create(**create_kwargs).execute()
            
            return {
                "id": file.get('id'),
                "url": file.get('webViewLink'),
                "download_url": file.get('webContentLink'),
                "path": destination_path,
                "size": file.get('size')
            }
        except HttpError as error:
            raise StorageError(f"Failed to upload to Google Drive: {error}")

    def download(self, file_id: str) -> bytes:
        try:
            request_kwargs = {'fileId': file_id}
            if self.shared_drive_id:
                request_kwargs['supportsAllDrives'] = True
                
            request = self.service.files().get_media(**request_kwargs)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            return fh.getvalue()
        except HttpError as error:
            if error.resp.status == 404:
                raise FileNotFoundStorageError(f"File {file_id} not found.")
            raise StorageError(f"Failed to download from Google Drive: {error}")

    def delete(self, file_id: str) -> bool:
        try:
            kwargs = {'fileId': file_id}
            if self.shared_drive_id:
                kwargs['supportsAllDrives'] = True
            self.service.files().delete(**kwargs).execute()
            return True
        except HttpError as error:
            if error.resp.status == 404:
                return False
            raise StorageError(f"Failed to delete file from Google Drive: {error}")

    def get_url(self, file_id: str) -> str:
        try:
            kwargs = {'fileId': file_id, 'fields': 'webViewLink'}
            if self.shared_drive_id:
                kwargs['supportsAllDrives'] = True
            file = self.service.files().get(**kwargs).execute()
            return file.get('webViewLink', '')
        except HttpError as error:
            if error.resp.status == 404:
                raise FileNotFoundStorageError(f"File {file_id} not found.")
            raise StorageError(f"Failed to get URL: {error}")

    def get_metadata(self, file_id: str) -> Dict[str, Any]:
        try:
            kwargs = {'fileId': file_id, 'fields': '*'}
            if self.shared_drive_id:
                kwargs['supportsAllDrives'] = True
            file = self.service.files().get(**kwargs).execute()
            return file
        except HttpError as error:
            if error.resp.status == 404:
                raise FileNotFoundStorageError(f"File {file_id} not found.")
            raise StorageError(f"Failed to get metadata: {error}")
