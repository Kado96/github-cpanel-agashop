import tarfile
import os

dist_path = r"E:\AgaShop\github-cpanel-agashop\frontend\dist"
output_filename = r"E:\AgaShop\github-cpanel-agashop\dist.tar.gz"

if os.path.exists(dist_path):
    print(f"Compression de {dist_path} en cours...")
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(dist_path, arcname="dist")
    print(f"✅ SUCCÈS ! Le fichier {output_filename} a été créé à la racine de votre projet.")
    print("👉 Allez sur cPanel et uploadez ce fichier dist.tar.gz (L'antivirus va le laisser passer !)")
else:
    print(f"❌ ERREUR : Le dossier {dist_path} n'existe pas. Avez-vous bien fait 'npm run build' ?")
