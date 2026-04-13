# 🛠️ Guide de développement - AgaShop Mobile

Guide rapide pour développer l'application en local et la préparer pour la production.

## 📋 Table des matières

- [Configuration initiale](#-configuration-initiale)
- [Développement local](#-développement-local)
- [Développement avec API en ligne](#-développement-avec-api-en-ligne)
- [Build pour Android](#-build-pour-android)
- [Workflow recommandé](#-workflow-recommandé)

---

## ⚙️ Configuration initiale

### 1. Installer les dépendances

```bash
cd agashop_mobile
npm install
```

### 2. Configurer l'environnement

Créez un fichier `.env` à la racine du projet :

**Pour développement local** (API sur localhost:8000) :
```bash
echo "VITE_API_URL=http://localhost:8000/api" > .env
```

**Pour production/test** (API en ligne) :
```bash
echo "VITE_API_URL=https://api.agashop.bi/api" > .env
```

---

## 🏠 Développement local

### Prérequis

1. **API Django locale** doit être en cours d'exécution :
   ```bash
   cd ../api/backend
   ..\virtualenv\api\Scripts\Activate.ps1  # Windows
   # ou
   source ../virtualenv/api/bin/activate   # Linux/Mac
   python manage.py runserver
   ```

2. **Configuration .env** :
   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

### Démarrer le serveur de développement

```bash
npm run dev
```

L'application sera accessible sur : `http://localhost:5173`

### Avantages du développement local

- ✅ Modifications instantanées (Hot Module Replacement)
- ✅ Débogage facile avec les DevTools
- ✅ Pas besoin de connexion Internet
- ✅ Tests rapides des nouvelles fonctionnalités

---

## 🌐 Développement avec API en ligne

### Configuration

1. **Configuration .env** :
   ```env
   VITE_API_URL=https://api.agashop.bi/api
   ```

2. **Démarrer le serveur** :
   ```bash
   npm run dev
   ```

### Avantages

- ✅ Test avec les vraies données de production
- ✅ Vérification de la compatibilité avec l'API en ligne
- ✅ Pas besoin de lancer l'API locale

### Inconvénients

- ⚠️ Nécessite une connexion Internet
- ⚠️ Utilise les données réelles (attention aux modifications)

---

## 📱 Build pour Android

### Prérequis

1. **Android Studio** installé
2. **Android SDK** configuré
3. **Java JDK** installé

### Étapes

1. **Build de production** :
   ```bash
   npm run build
   ```
   ...install
   npx react-native run-android

2. **Synchroniser avec Capacitor** :
   ```bash
   npm run cap:sync
   ```

3. **Ouvrir dans Android Studio** :
   ```bash
   npm run cap:open:android
   ```

4. **Dans Android Studio** :
   - Attendre la synchronisation Gradle
   - Sélectionner un appareil/émulateur
   - Cliquer sur "Run" (▶)

### Commandes rapides

```bash
# Build complet (build + sync + open)
npm run cap:build:android

# Build et sync uniquement
npm run android:build

# Lancer sur appareil
npm run android:run
```

### ⚠️ Important : API en ligne en mode Android

**L'application Android utilise TOUJOURS l'API en ligne**, même si vous avez configuré `.env` avec l'URL locale.

C'est normal et souhaitable car :
- Les appareils Android ne peuvent pas accéder à `localhost` de votre machine
- L'API doit être accessible depuis Internet
- La configuration est dans `src/plugins/axios.js` (ligne 17-19)

---

## 🔄 Workflow recommandé

### Scénario 1 : Développement de nouvelles fonctionnalités

```bash
# 1. Configurer pour local
echo "VITE_API_URL=http://localhost:8000/api" > .env

# 2. Démarrer l'API locale
cd ../api/backend
python manage.py runserver

# 3. Dans un autre terminal, démarrer l'app
cd agashop_mobile
npm run dev

# 4. Développer et tester localement
# 5. Quand prêt, tester avec l'API en ligne
echo "VITE_API_URL=https://api.agashop.bi/api" > .env
npm run dev
```

### Scénario 2 : Test avant déploiement

```bash
# 1. Configurer pour production
echo "VITE_API_URL=https://api.agashop.bi/api" > .env

# 2. Build de production
npm run build

# 3. Tester le build localement
npm run preview

# 4. Si OK, build Android
npm run cap:build:android
```

### Scénario 3 : Build Android pour distribution

```bash
# 1. S'assurer que .env pointe vers l'API en ligne (optionnel, pas utilisé en natif)
echo "VITE_API_URL=https://api.agashop.bi/api" > .env

# 2. Build de production
npm run build

# 3. Synchroniser avec Android
npm run cap:sync

# 4. Ouvrir Android Studio
npm run cap:open:android

# 5. Dans Android Studio : Build → Generate Signed Bundle / APK
```

---

## 🐛 Débogage

### Problèmes courants

1. **L'application ne se connecte pas à l'API locale**
   - Vérifiez que l'API Django tourne sur `http://localhost:8000`
   - Vérifiez le fichier `.env`
   - Vérifiez la console du navigateur (F12)

2. **Erreurs CORS**
   - En développement local, vérifiez `CORS_ORIGIN_ALLOW_ALL = True` dans Django
   - En mode natif Android, les erreurs CORS ne devraient pas apparaître

3. **L'application Android ne se connecte pas**
   - Vérifiez la connexion Internet
   - Vérifiez que l'API en ligne est accessible : `https://api.agashop.bi/api`
   - Vérifiez les logs dans Android Studio (Logcat)

4. **Les modifications ne s'affichent pas**
   - Videz le cache : `Ctrl+Shift+R` (Chrome)
   - Redémarrez le serveur de développement
   - Vérifiez que vous avez bien sauvegardé les fichiers

---

## 📝 Checklist avant commit

- [ ] Code testé en local avec API locale
- [ ] Code testé avec API en ligne
- [ ] Pas d'erreurs dans la console
- [ ] Build de production fonctionne (`npm run build`)
- [ ] Fichier `.env` n'est pas commité (dans `.gitignore`)

---

## 🔗 Liens utiles

- **API en ligne** : `https://api.agashop.bi/api`
- **API locale** : `http://localhost:8000/api`
- **Documentation API** : Voir `../api/README.md`
- **Guide Android** : Voir `GUIDE_ANDROID.md`

---

**Dernière mise à jour** : Janvier 2025

