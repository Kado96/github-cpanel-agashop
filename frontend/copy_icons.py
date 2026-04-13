import os
import shutil

base_path = r"e:\AgaShop\Frontend\agashop_mobile"
icons_dir = os.path.join(base_path, "public", "icons")
if not os.path.exists(icons_dir):
    os.makedirs(icons_dir)

source = os.path.join(base_path, r"android\app\src\main\res\mipmap-xxxhdpi\ic_agashop.webp")
shutil.copy2(source, os.path.join(base_path, "public", "favicon.webp"))

sizes = ["icon-48.webp", "icon-72.webp", "icon-96.webp", "icon-128.webp", "icon-192.webp", "icon-256.webp", "icon-512.webp"]
for size in sizes:
    shutil.copy2(source, os.path.join(icons_dir, size))

print("Files copied successfully")
