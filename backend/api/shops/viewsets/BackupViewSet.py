import os
import zipfile
import tempfile
from django.http import FileResponse, Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config

class TempFileResponse(FileResponse):
    """
    Classe personnalisée héritant de FileResponse qui supprime
    automatiquement le fichier ZIP temporaire après son envoi complet.
    """
    def __init__(self, temp_file_path, *args, **kwargs):
        self.temp_file_path = temp_file_path
        # Ouvrir le fichier en mode binaire lecture
        file_handle = open(temp_file_path, 'rb')
        super().__init__(file_handle, *args, **kwargs)
        
    def close(self):
        super().close()
        try:
            if os.path.exists(self.temp_file_path):
                os.remove(self.temp_file_path)
                print(f"Fichier temporaire supprime avec succes : {self.temp_file_path}")
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier temporaire {self.temp_file_path} : {str(e)}")

class BackupExportView(APIView):
    """
    Vue permettant d'exporter la base de données SQLite (db.sqlite3)
    et les fichiers médias compressés sous forme d'archive ZIP.
    Sécurisée par un token défini dans les variables d'environnement.
    """
    authentication_classes = []  # Pas d'authentification par session/JWT standard pour cette route
    permission_classes = []      # Géré manuellement via le token secret dans l'URL

    def get(self, request, *args, **kwargs):
        # 1. Vérification du token de sécurité
        client_token = request.GET.get('token')
        server_token = config('BACKUP_SYNC_TOKEN', default='')

        if not server_token:
            return Response(
                {"error": "Le jeton de synchronisation n'est pas configuré sur le serveur (BACKUP_SYNC_TOKEN)."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not client_token or client_token != server_token:
            return Response(
                {"error": "Accès refusé. Jeton de synchronisation invalide ou manquant."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. Définition des chemins d'accès aux fichiers à sauvegarder
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        media_dir = settings.MEDIA_ROOT

        if not os.path.exists(db_path):
            return Response(
                {"error": f"Base de données introuvable sur le serveur à l'adresse {db_path}."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. Création du fichier ZIP temporaire
        try:
            # Créer un fichier temporaire unique
            fd, temp_zip_path = tempfile.mkstemp(suffix='.zip')
            os.close(fd)  # Fermer le descripteur de fichier bas niveau ouvert par mkstemp

            print(f"Creation de l'archive ZIP temporaire : {temp_zip_path}")
            
            with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # A. Ajouter la base de données
                # On la place à la racine de l'archive zip
                zip_file.write(db_path, 'db.sqlite3')
                print("Base de donnees ajoutee a l'archive ZIP.")

                # B. Ajouter le dossier media s'il existe
                if os.path.exists(media_dir):
                    print(f"Ajout du dossier media ({media_dir}) a l'archive...")
                    for root, _, files in os.walk(media_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Créer un chemin relatif à l'intérieur du zip sous le dossier 'media/'
                            rel_path = os.path.join('media', os.path.relpath(file_path, media_dir))
                            zip_file.write(file_path, rel_path)
                    print("Dossier media ajoute a l'archive ZIP.")
                else:
                    print("Aucun dossier media detecte sur le serveur.")

            # 4. Renvoyer le fichier ZIP généré avec notre réponse temporaire autonettoyante
            response = TempFileResponse(
                temp_zip_path,
                as_attachment=True,
                filename='agashop_backup.zip'
            )
            response['Content-Type'] = 'application/zip'
            return response

        except Exception as e:
            # En cas d'erreur, s'assurer que le fichier temporaire est supprimé
            if 'temp_zip_path' in locals() and os.path.exists(temp_zip_path):
                try:
                    os.remove(temp_zip_path)
                except:
                    pass
            return Response(
                {"error": f"Une erreur est survenue lors de la création de la sauvegarde : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
