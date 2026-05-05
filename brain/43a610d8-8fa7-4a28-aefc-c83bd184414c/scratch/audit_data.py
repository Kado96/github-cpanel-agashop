import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.shops.models import Product, Supply

def audit_products():
    print("--- Audit des produits et approvisionnements ---")
    products = Product.objects.all()
    anomalies = 0
    
    for p in products:
        # 1. Vérifier si la quantité est négative
        if p.quantity < 0:
            print(f"ALERTE : Produit ID {p.id} ({p.name}) a une quantité négative : {p.quantity}")
            anomalies += 1
            
        # 2. Vérifier la cohérence avec les Supplies
        supplies = Supply.objects.filter(product=p)
        total_supplied = sum(s.quantity for s in supplies)
        # Note : On ne peut pas comparer directement total_supplied et p.quantity 
        # car il y a aussi les ventes qui diminuent le stock.
        
        # 3. Vérifier les prix unitaires arrondis vs réels
        for s in supplies:
            if s.quantity > 0:
                real_unit_price = s.total_buy_price / s.quantity
                if abs(real_unit_price - round(real_unit_price)) > 0.01:
                    print(f"INFO : Achat ID {s.id} (Produit {p.id}) : Prix unitaire réel {real_unit_price:.2f} vs arrondi {round(real_unit_price)}")
                    # anomalies += 1 # C'est juste une info sur la perte de précision due au round()
    
    print(f"\nAudit terminé. {anomalies} anomalies critiques trouvées.")

if __name__ == "__main__":
    audit_products()
