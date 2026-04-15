import os
import shutil

def sync():
    src = os.path.join(os.getcwd(), 'backend')
    dest = '/home/agashopb/api'
    
    # Liste des dossiers/fichiers à ignorer
    ignore_list = [
        '.git', 'venv', 'db.sqlite3', 'media', '__pycache__', 
        '.env', '.vscode', '.cursor', 'pyrightconfig.json', '.gitignore'
    ]
    
    print(f"--- Démarrage de la synchronisation de {src} vers {dest} ---")
    
    if not os.path.exists(src):
        print(f"Erreur : Le dossier source {src} n'existe pas.")
        return

    count = 0
    for root, dirs, files in os.walk(src):
        # Filtrer les dossiers ignorés
        dirs[:] = [d for d in dirs if d not in ignore_list]
        
        # Créer le chemin relatif
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dest, rel_path)
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            
        for file in files:
            if file in ignore_list:
                continue
            
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            
            # Copie du fichier
            shutil.copy2(src_file, dest_file)
            count += 1

    print(f"--- Synchronisation terminée : {count} fichiers copiés ---")
    print("Veuillez maintenant redémarrer votre application Python dans cPanel.")

if __name__ == "__main__":
    sync()
