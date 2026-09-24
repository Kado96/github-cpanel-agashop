from django.db import models
from django.utils.translation import gettext_lazy as _

class AbstractFileMetadata(models.Model):
    """Abstract Django model mixin for storing file metadata."""
    provider_file_id = models.CharField(_("Provider File ID"), max_length=255, db_index=True)
    file_name = models.CharField(_("File Name"), max_length=255)
    mime_type = models.CharField(_("MIME Type"), max_length=100, blank=True, null=True)
    size_bytes = models.PositiveBigIntegerField(_("Size in Bytes"), blank=True, null=True)
    url = models.URLField(_("File URL"), max_length=1024, blank=True, null=True)
    thumbnail_url = models.URLField(_("Thumbnail URL"), max_length=1024, blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.file_name
