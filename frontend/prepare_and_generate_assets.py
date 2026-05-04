import os
from PIL import Image

def fix_image(filepath, target_width, target_height):
    if not os.path.exists(filepath):
        print(f"⚠️ Ignoré : Le fichier {filepath} n'existe pas.")
        return False
        
    try:
        img = Image.open(filepath)
        w, h = img.size
        print(f"🔍 Vérification de {os.path.basename(filepath)} (Actuel: {w}x{h}, Cible: {target_width}x{target_height})")
        
        if w != target_width or h != target_height:
            print(f"📐 Redimensionnement de {os.path.basename(filepath)}...")
            
            # Calcul du ratio pour couvrir toute la zone sans déformer
            ratio = max(target_width / w, target_height / h)
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            
            img = img.resize((new_w, new_h), Image.LANCZOS)
            
            # Recadrage au centre (Crop)
            left = (new_w - target_width) // 2
            top = (new_h - target_height) // 2
            img = img.crop((left, top, left + target_width, top + target_height))
            
            # Sauvegarde de l'image corrigée
            img.save(filepath, format="PNG")
            print(f"✅ {os.path.basename(filepath)} redimensionné avec succès !")
        else:
            print(f"✅ {os.path.basename(filepath)} est déjà aux bonnes dimensions.")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("🛠️  CORRECTION ET GÉNÉRATION DES ASSETS ANDROID")
    print("=" * 60)
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    
    # Fichiers à vérifier
    icon_path = os.path.join(base_dir, "icon-only.png")
    icon_bg_path = os.path.join(base_dir, "icon-background.png")
    icon_fg_path = os.path.join(base_dir, "icon-foreground.png")
    splash_path = os.path.join(base_dir, "splash.png")
    splash_dark_path = os.path.join(base_dir, "splash-dark.png")
    
    # 1. Correction des icônes (1024x1024)
    print("\n--- 1. Vérification des icônes ---")
    fix_image(icon_path, 1024, 1024)
    fix_image(icon_bg_path, 1024, 1024)
    fix_image(icon_fg_path, 1024, 1024)
    
    # 2. Correction des splash screens (2732x2732)
    print("\n--- 2. Vérification des splash screens ---")
    fix_image(splash_path, 2732, 2732)
    fix_image(splash_dark_path, 2732, 2732)
    
    # 3. Lancement de la génération Capacitor
    print("\n--- 3. Génération des assets Capacitor ---")
    os.system("npx @capacitor/assets generate --assetPath resources")
    
    # 4. Synchronisation Android
    print("\n--- 4. Synchronisation Android ---")
    os.system("npx cap sync android")
    
    print("\n" + "=" * 60)
    print("🚀 Terminé ! Teste avec : npx cap open android")
    print("=" * 60)

if __name__ == "__main__":
    main()
