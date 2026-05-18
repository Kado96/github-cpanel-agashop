import urllib.request
import urllib.error
import json

url = 'https://api.agashop.bi/api/shops/backup/download/?token=AgaShopSync2026_x8F2kL9qP3vW5zY7'

print("🔍 Interrogation de l'API de production...")
try:
    response = urllib.request.urlopen(url)
    print("✅ Succès ! Le téléchargement fonctionne. Code 200.")
except urllib.error.HTTPError as e:
    print(f"❌ Erreur HTTP {e.code}")
    try:
        error_body = e.read().decode('utf-8')
        try:
            parsed = json.loads(error_body)
            print("Détail de l'erreur JSON :")
            print(json.dumps(parsed, indent=4, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Détail de l'erreur brut :")
            print(error_body)
    except Exception as read_err:
        print("Impossible de lire le corps de l'erreur :", read_err)
except Exception as e:
    print("Erreur réseau inattendue :", e)
