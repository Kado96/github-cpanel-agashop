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
        dirs[:] = [d for d in dirs if d not in ignore_list]
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dest, rel_path)
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            
        for file in files:
            if file in ignore_list:
                continue
            
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            
            # Affichage discret mais informatif
            if "migrations" in src_file or "models.py" in src_file or "viewsets" in src_file:
                print(f"  -> Copie de : {rel_path}/{file}")

            shutil.copy2(src_file, dest_file)
            count += 1

    print(f"OK : Total de {count} fichiers synchronisés.")

    # Vérification critique de la migration 0023
    target_migration = os.path.join(dest, 'api', 'shops', 'migrations', '0023_productmedia_basicproduct_media.py')
    if os.path.exists(target_migration):
        print(f"✅ Migration 0023 détectée à destination.")
    else:
        print(f"⚠️ Migration 0023 MANQUANTE à destination ({target_migration}).")
        print("Tentative de génération automatique des migrations sur le serveur...")
        subprocess.run([venv_python, os.path.join(dest, 'manage.py'), 'makemigrations', 'shops'], cwd=dest)

    print("\n--- 2. Exécution des migrations (Base de données) ---")
    manage_py = os.path.join(dest, 'manage.py')
    try:
        subprocess.run([venv_python, manage_py, 'migrate', 'shops'], cwd=dest, check=True)
        print("OK : Migrations effectuées.")
    except subprocess.CalledProcessError:
        print("Erreur lors du migrate. On tente un makemigrations suivi d'un migrate...")
        subprocess.run([venv_python, manage_py, 'makemigrations', 'shops'], cwd=dest)
        subprocess.run([venv_python, manage_py, 'migrate', 'shops'], cwd=dest)

    print("\n--- 3. Nettoyage et fusion des doublons d'images ---")
    try:
        subprocess.run([venv_python, manage_py, 'cleanup_images'], cwd=dest, check=True)
        print("OK : Nettoyage terminé.")
    except subprocess.CalledProcessError as e:
        print(f"Le nettoyage a échoué (peut-être que la colonne media_id manque encore).")

    print("\n--- SYNCHRONISATION TERMINÉE ---")
    print(">>> N'oubliez pas de REDÉMARRER l'application Python dans cPanel (Setup Python App).")

if __name__ == "__main__":
    sync()
