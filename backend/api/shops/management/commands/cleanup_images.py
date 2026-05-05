import hashlib
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from api.shops.models import BasicProduct, ProductMedia
from django.conf import settings

class Command(BaseCommand):
    help = 'Migre les images des produits vers la bibliothèque de médias en éliminant les doublons'

    def handle(self, *args, **options):
        products = BasicProduct.objects.filter(media__isnull=True).exclude(image='')
        self.stdout.write(f"Analyse de {products.count()} produits avec images legacy...")

        # Map pour stocker {hash_md5: product_media_instance}
        media_map = {}
        # Map pour stocker {nom_normalise: product_media_instance} pour les similarités
        name_map = {}
        
        # Pré-charger les médias existants
        for pm in ProductMedia.objects.all():
            if pm.file and os.path.exists(pm.file.path):
                f_hash = self.get_file_hash(pm.file.path)
                media_map[f_hash] = pm
                if pm.name:
                    name_map[pm.name.lower().strip()] = pm

        count_migrated = 0
        count_shared = 0

        for product in products:
            if not product.image or not os.path.exists(product.image.path):
                continue

            file_path = product.image.path
            file_hash = self.get_file_hash(file_path)
            prod_name = product.name.lower().strip() if product.name else ""

            # 1. Recherche par Hash (Identique binaire)
            if file_hash in media_map:
                product.media = media_map[file_hash]
                product.save(update_fields=['media'])
                count_shared += 1
                self.stdout.write(f"Mutualisation par hash: {product.name}")
                continue

            # 2. Recherche par Nom (Appellation identique)
            if prod_name in name_map:
                # Si le nom est identique, on vérifie si la taille du fichier est proche (similarité)
                existing_media = name_map[prod_name]
                if existing_media.file and os.path.exists(existing_media.file.path):
                    existing_size = os.path.getsize(existing_media.file.path)
                    current_size = os.path.getsize(file_path)
                    
                    # Si la différence de taille est < 5%, on considère que c'est la même image "semblable"
                    if abs(existing_size - current_size) / max(existing_size, 1) < 0.05:
                        product.media = existing_media
                        product.save(update_fields=['media'])
                        count_shared += 1
                        self.stdout.write(f"Mutualisation par appellation semblable: {product.name}")
                        continue

            # 3. Nouveau média (Unique)
            with open(file_path, 'rb') as f:
                new_media = ProductMedia(name=product.name)
                filename = os.path.basename(file_path)
                new_media.file.save(filename, File(f), save=True)
                
                media_map[file_hash] = new_media
                if prod_name:
                    name_map[prod_name] = new_media
                product.media = new_media
                product.save(update_fields=['media'])
                count_migrated += 1
                self.stdout.write(self.style.SUCCESS(f"Nouveau média créé: {product.name}"))

        self.stdout.write(self.style.SUCCESS(
            f"Migration terminée: {count_migrated} nouvelles images, {count_shared} doublons mutualisés."
        ))

    def get_file_hash(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
