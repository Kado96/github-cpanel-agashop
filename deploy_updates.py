import os
import shutil
import subprocess

def sync():
    """
    Script de déploiement automatique pour AgaShop (cPanel)
    1. Synchronise les fichiers du dossier backend vers le dossier de l'API active
    2. Exécute les migrations Django
    3. Exécute le script de nettoyage des images (dédoublonnage)
    """
    # Chemins basés sur la structure cPanel (à ajuster si nécessaire)
    src = os.path.join(os.getcwd(), 'backend')
    dest = '/home/agashopb/api'
    venv_python = '/home/agashopb/virtualenv/api/3.11/bin/python'
    
    # Liste des dossiers/fichiers à ignorer lors de la copie
    ignore_list = [
        '.git', 'venv', 'db.sqlite3', 'media', '__pycache__', 
        '.env', '.vscode', '.cursor', 'pyrightconfig.json', '.gitignore'
    ]
    
    print(f"\n--- 1. Synchronisation de {src} vers {dest} ---")
    
    if not os.path.exists(src):
        print(f"Erreur : Le dossier source {src} n'existe pas.")
        return

    count = 0
    for root, dirs, files in os.walk(src):
        # Filtrer les dossiers ignorés
        dirs[:] = [d for d in dirs if d not in ignore_list]
        
        # Créer le chemin relatif pour la destination
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dest, rel_path)
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            
        for file in files:
            if file in ignore_list:
                continue
            
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            
            # Copie du fichier avec préservation des métadonnées
            shutil.copy2(src_file, dest_file)
            count += 1

    print(f"OK : {count} fichiers copiés avec succès.")

    # Vérification de l'existence du manage.py à destination
    manage_py = os.path.join(dest, 'manage.py')
    if not os.path.exists(manage_py):
        print(f"Erreur : manage.py introuvable à l'adresse {manage_py}")
        return

    print("\n--- 2. Exécution des migrations (Base de données) ---")
    try:
        subprocess.run([venv_python, manage_py, 'migrate', 'shops'], cwd=dest, check=True)
        print("OK : Migrations effectuées.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors des migrations : {e}")

    print("\n--- 3. Nettoyage et fusion des doublons d'images ---")
    try:
        subprocess.run([venv_python, manage_py, 'cleanup_images'], cwd=dest, check=True)
        print("OK : Nettoyage terminé.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du nettoyage : {e}")

    print("\n--- SYNCHRONISATION TERMINÉE ---")
    print(">>> N'oubliez pas de REDÉMARRER l'application Python dans cPanel (Setup Python App).")

if __name__ == "__main__":
    sync()
