import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les groupes de 4 espaces par une tabulation
    content = content.replace('    ', '\t')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file(r'e:\AgaShop\github-cpanel-agashop\backend\api\shops\viewsets\ProductViewSet.py')
fix_file(r'e:\AgaShop\github-cpanel-agashop\backend\api\shops\viewsets\SupplyViewSet.py')
print("Fichiers corrigés.")
