import sqlite3
import os
import unicodedata
import re

def normalize(s):
    if not s: return ""
    # Remove accents
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    # Replace non-alphanumeric with underscores
    s = re.sub(r'[^a-z0-9]', '_', s)
    # Remove double underscores
    s = re.sub(r'_+', '_', s)
    return s.strip('_')

def run():
    db_path = 'db.sqlite3'
    media_path = 'media/images'
    
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found")
        return
    if not os.path.exists(media_path):
        print(f"Error: {media_path} not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Get all products
    try:
        cursor.execute("SELECT id, name, image FROM shops_basicproduct")
        products = cursor.fetchall()
    except Exception as e:
        print(f"Error querying table: {e}")
        conn.close()
        return

    # 2. Map all files to normalized names
    files = os.listdir(media_path)
    file_map = {}
    for f in files:
        # We skip directories if any
        if os.path.isdir(os.path.join(media_path, f)): continue
        
        name_part = os.path.splitext(f)[0]
        norm = normalize(name_part)
        
        # Priority: Exact match without random suffixes or shorter names
        if norm not in file_map or len(f) < len(file_map[norm]):
            file_map[norm] = f

    print(f"Found {len(products)} products and {len(files)} image files.")
    
    updates = []
    
    for p_id, name, current_img in products:
        norm_name = normalize(name)
        
        # Check if current image path is valid
        is_valid = False
        if current_img:
            if os.path.exists(os.path.join('media', current_img)):
                is_valid = True
            elif os.path.exists(os.path.join(media_path, current_img)): # maybe it's missing the images/ prefix
                is_valid = True
                new_path = f"images/{current_img}"
                updates.append((new_path, p_id))
                continue

        if not is_valid:
            # Try to match by name
            best_match = file_map.get(norm_name)
            if best_match:
                new_path = f"images/{best_match}"
                if new_path != current_img:
                    updates.append((new_path, p_id))

    # 3. Perform updates
    if updates:
        print(f"Applying {len(updates)} updates...")
        try:
            cursor.executemany("UPDATE shops_basicproduct SET image = ? WHERE id = ?", updates)
            conn.commit()
            print("Successfully updated image links.")
        except Exception as e:
            print(f"Error updating database: {e}")
            conn.rollback()
    else:
        print("No updates needed.")

    conn.close()

if __name__ == "__main__":
    run()
