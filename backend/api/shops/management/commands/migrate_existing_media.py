import os
import mimetypes
from django.core.management.base import BaseCommand
from django.conf import settings
from jarvis_storage.service import StorageService
from jarvis_storage.core.config import StorageConfig
from api.shops.models import FileMetadata

class Command(BaseCommand):
    help = "Migre les images existantes du backend vers le service de stockage jarvis_storage et crée les entrées FileMetadata."

    def add_arguments(self, parser):
        parser.add_argument(
            '--shop-id',
            type=str,
            default='B000001',
            help="L'identifiant de la boutique cible (défaut: B000001)."
        )
        parser.add_argument(
            '--images-dir',
            type=str,
            default=None,
            help="Chemin personnalisé vers le dossier d'images (défaut: backend/media/images)."
        )

    def handle(self, *args, **options):
        shop_id = options['shop_id']
        images_dir = options['images_dir']

        if not images_dir:
            images_dir = os.path.join(settings.BASE_DIR, 'media', 'images')

        self.stdout.write(self.style.NOTICE(f"Démarrage de la migration pour la boutique [{shop_id}]..."))
        self.stdout.write(f"Dossier source : {images_dir}")

        if not os.path.exists(images_dir):
            self.stdout.write(self.style.ERROR(f"Le dossier spécifié n'existe pas : {images_dir}"))
            return

        # Initialisation du service de stockage SDK
        provider_name = getattr(settings, 'STORAGE_PROVIDER', 'local').lower()
        if provider_name in ['google_drive', 'gdrive']:
            config = StorageConfig(
                provider="google_drive",
                google_drive_credentials_json=getattr(settings, 'GOOGLE_APPLICATION_CREDENTIALS', None),
                google_drive_shared_drive_id=getattr(settings, 'GOOGLE_DRIVE_SHARED_DRIVE_ID', None)
            )
        else:
            local_path = getattr(settings, 'LOCAL_STORAGE_BASE_PATH', os.path.join(settings.BASE_DIR, 'media', 'sdk_storage'))
            config = StorageConfig(
                provider="local",
                local_storage_path=local_path
            )

        storage_service = StorageService(config=config)

        # Liste des fichiers dans le dossier images
        all_entries = os.listdir(images_dir)
        image_files = [f for f in all_entries if os.path.isfile(os.path.join(images_dir, f))]

        total_files = len(image_files)
        self.stdout.write(f"Total des fichiers trouvés : {total_files}")

        migrated_count = 0
        error_count = 0
        total_original_bytes = 0
        total_compressed_bytes = 0

        for idx, filename in enumerate(image_files, start=1):
            file_path = os.path.join(images_dir, filename)
            try:
                with open(file_path, 'rb') as f:
                    file_bytes = f.read()

                original_size = len(file_bytes)
                total_original_bytes += original_size

                # Détermination du MIME type
                mime_type, _ = mimetypes.guess_type(filename)
                if not mime_type:
                    mime_type = 'image/jpeg' if filename.lower().endswith(('.jpg', '.jpeg')) else 'image/png'

                # Appel upload_image via le StorageService SDK
                # signature: upload_image(shop_id, image_data, base_destination_path, metadata)
                result = storage_service.upload_image(
                    shop_id=shop_id,
                    image_data=file_bytes,
                    base_destination_path=filename,
                    metadata={'original_filename': filename, 'source': 'migration_existing_media'}
                )

                main_res = result.get('main', {})
                thumb_res = result.get('thumbnail', {})

                main_file_id = main_res.get('id', filename)
                main_url = main_res.get('url', '')
                main_size = main_res.get('size', original_size)
                thumbnail_file_id = thumb_res.get('id', '')
                thumbnail_url = thumb_res.get('url', '')

                total_compressed_bytes += main_size

                # Enregistrement de FileMetadata
                FileMetadata.objects.create(
                    provider_file_id=main_file_id,
                    file_name=filename,
                    mime_type=mime_type,
                    size_bytes=main_size,
                    url=main_url,
                    thumbnail_url=thumbnail_url,
                    shop_id=shop_id,
                    external_file_id=main_file_id,
                    thumbnail_file_id=thumbnail_file_id,
                    status='UPLOADED'
                )

                migrated_count += 1
                if idx % 50 == 0 or idx == total_files:
                    self.stdout.write(f"Progression : {idx}/{total_files} images traitées...")

            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.WARNING(f"Erreur lors du traitement de '{filename}': {str(e)}"))

        # Récapitulatif
        saved_bytes = max(0, total_original_bytes - total_compressed_bytes)
        compression_ratio = ((saved_bytes / total_original_bytes) * 100) if total_original_bytes > 0 else 0

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("RÉCAPITULATIF DE LA MIGRATION"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"Images trouvées        : {total_files}")
        self.stdout.write(f"Images migrées avec succès : {migrated_count}")
        self.stdout.write(f"Erreurs rencontrées   : {error_count}")
        self.stdout.write(f"Taille d'origine totale : {total_original_bytes / (1024 * 1024):.2f} Mo")
        self.stdout.write(f"Taille compressée totale: {total_compressed_bytes / (1024 * 1024):.2f} Mo")
        self.stdout.write(f"Espace économisé       : {saved_bytes / (1024 * 1024):.2f} Mo ({compression_ratio:.1f}%)")
        self.stdout.write("=" * 50 + "\n")
