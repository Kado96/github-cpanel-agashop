# ⚡ Configuration rapide - AgaShop Mobile

Guide ultra-rapide pour configurer le projet en 2 minutes.

## 🚀 Démarrage rapide

### Option 1 : Développement local (API sur localhost)

```bash
# 1. Installer les dépendances
npm install

# 2. Configurer pour le développement local
npm run setup:local

# 3. Démarrer l'API Django (dans un autre terminal)
cd ../api/backend
..\virtualenv\api\Scripts\Activate.ps1  # Windows
python manage.py runserver

# 4. Démarrer l'application (dans le terminal principal)
cd agashop_mobile
npm run dev
```

✅ L'application sera sur `http://localhost:5173`  
✅ L'API sera sur `http://localhost:8000`

### Option 2 : Développement avec API en ligne

```bash
# 1. Installer les dépendances
npm install

# 2. Configurer pour l'API en ligne
npm run setup:prod

# 3. Démarrer l'application
npm run dev
```

✅ L'application sera sur `http://localhost:5173`  
✅ Utilise l'API en ligne : `https://api.agashop.bi/api`

### Option 3 : Build Android

```bash
# 1. Installer les dépendances
npm install

# 2. Build de production
npm run build

# 3. Synchroniser avec Android
npm run cap:sync

# 4. Ouvrir Android Studio
npm run cap:open:android
```

✅ L'application Android utilisera automatiquement l'API en ligne

---

## 📝 Commandes utiles

```bash
# Configuration
npm run setup:local      # Configurer pour développement local
npm run setup:prod       # Configurer pour API en ligne

# Développement
npm run dev              # Démarrer le serveur de développement
npm run build            # Build de production

# Android
npm run cap:build:android    # Build complet (build + sync + open)
npm run android:build        # Build et synchroniser uniquement
npm run cap:open:android     # Ouvrir Android Studio
```

---

## ⚠️ Notes importantes

1. **Fichier .env** : Créé automatiquement par `npm run setup:local` ou `npm run setup:prod`
2. **Mode Android** : L'application Android utilise toujours l'API en ligne (même si `.env` pointe vers localhost)
3. **Première installation** : Assurez-vous d'avoir Node.js 18+ et npm installés

---

## 🐛 Problèmes courants

**L'application ne démarre pas ?**
```bash
# Supprimer node_modules et réinstaller
rm -rf node_modules package-lock.json
npm install
```

**L'API locale ne répond pas ?**
```bash
# Vérifier que l'API Django tourne
# Dans le terminal de l'API, vous devriez voir :
# Starting development server at http://127.0.0.1:8000/
```

**Erreurs de build Android ?**
```bash
# Nettoyer et resynchroniser
cd android
./gradlew clean
cd ..
npm run cap:sync
```

---

**Besoin d'aide ?** Consultez `DEVELOPMENT.md` pour plus de détails.

