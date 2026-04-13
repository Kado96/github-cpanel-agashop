"""
Script pour générer les icônes et splash screens Android
à partir du icon.png (1024x1024) et splash.png de la racine du projet.
"""
import os
from PIL import Image

# Chemins
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANDROID_RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "android", "app", "src", "main", "res")

ICON_SRC = os.path.join(ROOT, "icon.png")
SPLASH_SRC = os.path.join(ROOT, "splash.png")

# Tailles des icônes Android par densité (mipmap)
ICON_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

# Tailles foreground pour adaptive icons (108dp * densité)
FOREGROUND_SIZES = {
    "mipmap-mdpi": 108,
    "mipmap-hdpi": 162,
    "mipmap-xhdpi": 216,
    "mipmap-xxhdpi": 324,
    "mipmap-xxxhdpi": 432,
}

# Splash screen sizes (drawable)
SPLASH_SIZES = {
    "drawable": (480, 800),
    "drawable-hdpi": (480, 800),
    "drawable-mdpi": (320, 480),
    "drawable-xhdpi": (720, 1280),
    "drawable-xxhdpi": (960, 1600),
    "drawable-xxxhdpi": (1280, 1920),
    "drawable-land-hdpi": (800, 480),
    "drawable-land-mdpi": (480, 320),
    "drawable-land-xhdpi": (1280, 720),
    "drawable-land-xxhdpi": (1600, 960),
    "drawable-land-xxxhdpi": (1920, 1280),
}

def resize_icon(src_path, dest_path, size):
    """Redimensionne une icône en gardant le ratio carré."""
    img = Image.open(src_path)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(dest_path, "PNG")

def resize_splash(src_path, dest_path, width, height):
    """Redimensionne le splash screen en gardant le ratio et en remplissant."""
    img = Image.open(src_path)
    src_w, src_h = img.size
    
    # Calculer le ratio pour couvrir toute la zone
    ratio = max(width / src_w, height / src_h)
    new_w = int(src_w * ratio)
    new_h = int(src_h * ratio)
    
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Centrer et recadrer
    left = (new_w - width) // 2
    top = (new_h - height) // 2
    img = img.crop((left, top, left + width, top + height))
    
    img.save(dest_path, "PNG")

def main():
    print("=" * 50)
    print("Generation des assets Android AgaShop")
    print("=" * 50)
    
    # 1. Générer les icônes (ic_agashop.png) dans chaque mipmap
    print("\n[ICONS] Generation des icones...")
    for folder, size in ICON_SIZES.items():
        dest_dir = os.path.join(ANDROID_RES, folder)
        os.makedirs(dest_dir, exist_ok=True)
        
        # Icône standard
        dest = os.path.join(dest_dir, "ic_agashop.png")
        resize_icon(ICON_SRC, dest, size)
        print(f"  OK {folder}/ic_agashop.png ({size}x{size})")
        
        # Icône ronde
        dest_round = os.path.join(dest_dir, "ic_agashop_round.png")
        resize_icon(ICON_SRC, dest_round, size)
        print(f"  OK {folder}/ic_agashop_round.png ({size}x{size})")
    
    # 2. Générer les foreground pour adaptive icons
    print("\n[FOREGROUND] Generation des adaptive icons...")
    for folder, size in FOREGROUND_SIZES.items():
        dest_dir = os.path.join(ANDROID_RES, folder)
        os.makedirs(dest_dir, exist_ok=True)
        
        dest = os.path.join(dest_dir, "ic_agashop_foreground.png")
        resize_icon(ICON_SRC, dest, size)
        print(f"  OK {folder}/ic_agashop_foreground.png ({size}x{size})")
        
        # Splash foreground aussi
        dest_splash = os.path.join(dest_dir, "splash_foreground.png")
        resize_icon(ICON_SRC, dest_splash, size)
        print(f"  OK {folder}/splash_foreground.png ({size}x{size})")
    
    # 3. Générer les splash screens
    print("\n[SPLASH] Generation des splash screens...")
    for folder, (w, h) in SPLASH_SIZES.items():
        dest_dir = os.path.join(ANDROID_RES, folder)
        os.makedirs(dest_dir, exist_ok=True)
        
        dest = os.path.join(dest_dir, "splash.png")
        resize_splash(SPLASH_SRC, dest, w, h)
        print(f"  OK {folder}/splash.png ({w}x{h})")
    
    print("\n" + "=" * 50)
    print("DONE - Tous les assets Android ont ete generes !")
    print("=" * 50)

if __name__ == "__main__":
    main()
