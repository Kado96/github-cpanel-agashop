import os
import sys
import shutil
import zipfile
import urllib.request
import urllib.parse
from datetime import datetime

# Configuration des couleurs ANSI pour une superbe console premium
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(title):
    print(f"\n{Colors.HEADER}{Colors.BOLD}════════════════════════════════════════════════════════════════════{Colors.ENDC}")
    print(f" {Colors.CYAN}{Colors.BOLD}🔄 {title}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}════════════════════════════════════════════════════════════════════{Colors.ENDC}\n")

def print_status(icon, message, color=Colors.BLUE):
    print(f" {color}{icon} {message}{Colors.ENDC}")

def print_success(message):
    print(f" {Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    print(f" {Colors.WARNING}⚠️ {message}{Colors.ENDC}")

def print_error(message):
    print(f" {Colors.FAIL}❌ {message}{Colors.ENDC}")

def get_env_variable(env_file_path, key):
    """
    Lit un fichier .env simple pour récupérer une variable spécifique.
    """
    if not os.path.exists(env_file_path):
        return None
    
    with open(env_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == key:
                    # Enlever les guillemets éventuels
                    val = v.strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    return val
    return None

def main():
    print_header("AGASHOP - SYNCHRONISATION PROD ➔ LOCAL")
    
    # 1. Détermination des chemins locaux
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, 'backend')
    env_file = os.path.join(backend_dir, '.env')
    
    db_local_path = os.path.join(backend_dir, 'db.sqlite3')
    media_local_dir = os.path.join(backend_dir, 'media')
    
    # 2. Récupération du Token de Synchronisation
    token = get_env_variable(env_file, 'BACKUP_SYNC_TOKEN')
    
    if not token:
        print_warning(f"La variable 'BACKUP_SYNC_TOKEN' n'a pas été trouvée dans {env_file}.")
        token = input(f" {Colors.CYAN}👉 Veuillez saisir manuellement le jeton de synchronisation (Token) : {Colors.ENDC}").strip()
        if not token:
            print_error("Jeton manquant. Synchronisation annulée.")
            sys.exit(1)
    else:
        print_success("Jeton de synchronisation chargé depuis le fichier .env local.")
        
    # URL de production de l'API
    prod_base_url = "https://api.agashop.bi"
    backup_endpoint = f"{prod_base_url}/api/shops/backup/download/"
    
    # Construire l'URL finale sécurisée avec le token
    params = urllib.parse.urlencode({'token': token})
    download_url = f"{backup_endpoint}?{params}"
    
    temp_zip_file = os.path.join(root_dir, 'prod_backup_temp.zip')
    
    # 3. Lancement du téléchargement
    print_status("📥", f"Connexion sécurisée à {prod_base_url}...", Colors.CYAN)
    
    def progress_callback(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, int(downloaded * 100 / total_size))
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            # Afficher une jolie barre de chargement textuelle
            bar_length = 30
            filled_length = int(bar_length * percent // 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            sys.stdout.write(f"\r    [{bar}] {percent}% ({mb_downloaded:.2f} / {mb_total:.2f} MB)")
            sys.stdout.flush()
        else:
            mb_downloaded = downloaded / (1024 * 1024)
            sys.stdout.write(f"\r    Téléchargement : {mb_downloaded:.2f} MB...")
            sys.stdout.flush()

    try:
        urllib.request.urlretrieve(download_url, temp_zip_file, progress_callback)
        sys.stdout.write("\n")
        print_success("Téléchargement de l'archive de production terminé.")
        
    except urllib.error.HTTPError as e:
        sys.stdout.write("\n")
        if e.code == 403:
            print_error("Accès refusé ! Le jeton de synchronisation est invalide ou rejeté par le serveur.")
        elif e.code == 500:
            print_error("Erreur serveur ! Vérifiez que le paramètre BACKUP_SYNC_TOKEN est bien configuré dans le .env de production.")
        else:
            print_error(f"Erreur HTTP lors du téléchargement : {e.code} {e.reason}")
        
        # Nettoyage si besoin
        if os.path.exists(temp_zip_file):
            os.remove(temp_zip_file)
        sys.exit(1)
        
    except Exception as e:
        sys.stdout.write("\n")
        print_error(f"Impossible de se connecter au serveur de production : {str(e)}")
        if os.path.exists(temp_zip_file):
            os.remove(temp_zip_file)
        sys.exit(1)

    # 4. Sauvegarde locale préventive de la base de données
    print_status("💾", "Préparation de la base de données locale...", Colors.CYAN)
    if os.path.exists(db_local_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_db_path = f"{db_local_path}.bak_{timestamp}"
        try:
            shutil.copy2(db_local_path, backup_db_path)
            print_success(f"Sauvegarde de précaution créée : {os.path.basename(backup_db_path)}")
        except Exception as e:
            print_warning(f"Impossible de créer la sauvegarde préventive : {str(e)}")
            confirm = input(f" {Colors.WARNING}Voulez-vous continuer sans sauvegarde de sécurité ? (o/n) : {Colors.ENDC}").strip().lower()
            if confirm != 'o':
                print_error("Opération annulée par l'utilisateur.")
                if os.path.exists(temp_zip_file):
                    os.remove(temp_zip_file)
                sys.exit(1)

    # 5. Extraction du fichier ZIP
    print_status("📦", "Extraction des données de production...", Colors.CYAN)
    
    try:
        if not os.path.exists(media_local_dir):
            os.makedirs(media_local_dir)
            print_status("📁", f"Création du dossier média local : {media_local_dir}", Colors.BLUE)
            
        with zipfile.ZipFile(temp_zip_file, 'r') as zip_ref:
            # Liste des fichiers à extraire
            namelist = zip_ref.namelist()
            total_files = len(namelist)
            
            print_status("⚙️", f"Extraction de {total_files} fichiers...", Colors.CYAN)
            
            for index, file_in_zip in enumerate(namelist, 1):
                # Afficher le fichier en cours d'extraction
                percent = int(index * 100 / total_files)
                sys.stdout.write(f"\r    [{percent}%] Extraction : {file_in_zip[:50]}...")
                sys.stdout.flush()
                
                # Définir la cible de l'extraction
                if file_in_zip == 'db.sqlite3':
                    # Extraire db.sqlite3 directement dans backend/
                    # Pour éviter les verrous de fichiers ouverts sous Windows, on tente une suppression préalable si possible
                    try:
                        if os.path.exists(db_local_path):
                            os.remove(db_local_path)
                    except Exception as err:
                        # Si le fichier est verrouillé, on prévient l'utilisateur
                        sys.stdout.write("\n")
                        print_error(f"La base locale db.sqlite3 est verrouillée : {str(err)}")
                        print_warning("Veuillez arrêter votre serveur de développement local Django s'il est actif !")
                        confirm = input(f" {Colors.CYAN}Avez-vous arrêté le serveur local ? Appuyez sur ENTRÉE pour réessayer ou 'q' pour quitter : {Colors.ENDC}").strip().lower()
                        if confirm == 'q':
                            raise Exception("Synchronisation interrompue en raison du fichier verrouillé.")
                        if os.path.exists(db_local_path):
                            os.remove(db_local_path)
                            
                    # Extraction finale de la base de données
                    zip_ref.extract(file_in_zip, backend_dir)
                    
                elif file_in_zip.startswith('media/'):
                    # Les fichiers médias sont extraits dans backend/media/
                    # Le chemin de destination est calculé pour correspondre à backend/media/
                    # zipfile extrait en gardant le dossier 'media/' s'il est extrait vers backend_dir
                    zip_ref.extract(file_in_zip, backend_dir)

            sys.stdout.write("\n")
            print_success("Extraction terminée avec succès.")

    except Exception as e:
        print_error(f"Erreur lors de la décompression : {str(e)}")
        if os.path.exists(temp_zip_file):
            os.remove(temp_zip_file)
        sys.exit(1)

    # 6. Nettoyage
    print_status("🧹", "Nettoyage des fichiers temporaires...", Colors.CYAN)
    if os.path.exists(temp_zip_file):
        os.remove(temp_zip_file)
        print_success("Fichier temporaire archivé supprimé.")

    # Message final de réussite
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TOUTES LES DONNÉES ONT ÉTÉ SYNCHRONISÉES AVEC SUCCÈS !{Colors.ENDC}")
    print(f" {Colors.BLUE}🔹 Base de données de production importée en local : {Colors.BOLD}backend/db.sqlite3{Colors.ENDC}")
    print(f" {Colors.BLUE}🔹 Fichiers médias synchronisés en local : {Colors.BOLD}backend/media/{Colors.ENDC}")
    print(f" {Colors.CYAN}💡 Vous pouvez dès à présent démarrer votre serveur local : {Colors.BOLD}python manage.py runserver{Colors.ENDC}\n")

if __name__ == '__main__':
    main()
