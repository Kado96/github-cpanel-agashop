# 🚀 Guide de Démarrage Rapide - AgaShop Mobile

Guide rapide pour lancer l'application mobile AgaShop.

---

## ⚡ Démarrage Rapide (5 minutes)

### 1. Installation des dépendances

```bash
cd agashop_mobile
npm install
```

### 2. Configuration de l'API

L'application est **déjà configurée** pour utiliser l'API en ligne (`https://api.agashop.bi/api`).

**Aucune configuration nécessaire** pour une application mobile ! 🎉

> **Note :** Pour le développement web local, vous pouvez créer un fichier `.env` avec `VITE_API_URL=http://localhost:8000/api`, mais ce n'est pas nécessaire pour l'application mobile.

### 3. Build de production

```bash
npm run build
```

### 4. Synchroniser avec Android

```bash
npm run cap:sync
```

### 5. Ouvrir Android Studio

```bash
npm run cap:open:android
```

### 6. Dans Android Studio

1. Attendez que le projet soit indexé (barre de progression en bas)
2. Connectez un appareil Android ou lancez un émulateur
3. Cliquez sur le bouton **Run** (▶️) pour installer et lancer l'application

---

## 📱 Tester l'Application

### Sur un appareil Android

1. **Activez le mode développeur** :
   - `Paramètres` → `À propos du téléphone`
   - Tapez 7 fois sur `Numéro de build`
   - `Paramètres` → `Options pour les développeurs` → Activez `Débogage USB`

2. **Connectez l'appareil** via USB

3. **Dans Android Studio**, cliquez sur **Run** (▶️)

### Sur un émulateur

1. Dans Android Studio, créez un émulateur :
   - `Tools` → `Device Manager` → `Create Device`
   - Choisissez un appareil (ex: Pixel 5)
   - Téléchargez une image système (ex: Android 13)
   - Cliquez sur **Finish**

2. Lancez l'émulateur

3. Dans Android Studio, cliquez sur **Run** (▶️)

---

## 🔨 Générer un APK pour installation manuelle

### APK Debug (pour tester)

1. Dans Android Studio : `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
2. Attendez la fin du build
3. Cliquez sur `locate` dans la notification
4. L'APK sera dans : `android/app/build/outputs/apk/debug/app-debug.apk`
5. Transférez l'APK sur votre appareil et installez-le

### APK Release (pour production)

Voir le guide complet : [GUIDE_ANDROID.md](./GUIDE_ANDROID.md)

---

## 📋 Commandes Utiles

```bash
# Build de production
npm run build

# Synchroniser avec Android
npm run cap:sync

# Ouvrir Android Studio
npm run cap:open:android

# Build complet (build + sync + open)
npm run cap:build:android

# Développement web (pour tester dans le navigateur)
npm run dev
```

---

## ✅ Vérifications

### L'application se connecte-t-elle à l'API ?

L'application est configurée pour utiliser automatiquement `https://api.agashop.bi/api` en mode mobile.

Pour vérifier :
1. Ouvrez l'application
2. Essayez de vous connecter
3. Si ça fonctionne, l'API est accessible ✅

### Problèmes courants

**L'application ne se connecte pas à l'API :**
- Vérifiez votre connexion Internet
- Vérifiez que l'API est accessible : https://api.agashop.bi
- Vérifiez les logs : Dans Android Studio, onglet `Logcat`

**L'application crash au démarrage :**
- Vérifiez les logs dans Android Studio (`Logcat`)
- Réessayez : `npm run build && npm run cap:sync`

**Android Studio ne trouve pas le SDK :**
- Ouvrez Android Studio
- `File` → `Settings` → `Appearance & Behavior` → `System Settings` → `Android SDK`
- Notez le chemin et créez `android/local.properties` :
  ```properties
  sdk.dir=C:\\Users\\VotreNom\\AppData\\Local\\Android\\Sdk
  ```

---

## 📚 Documentation Complète

Pour plus de détails, consultez :
- **[GUIDE_ANDROID.md](./GUIDE_ANDROID.md)** - Guide complet pour Android
- **[README.md](./README.md)** - Documentation générale du projet

---

## 🎯 Prochaines Étapes

1. ✅ Tester l'application sur un appareil Android
2. ✅ Vérifier toutes les fonctionnalités (login, register, etc.)
3. ✅ Générer un APK de release
4. ✅ Publier sur Google Play Store (voir GUIDE_ANDROID.md)

---

**Bon développement ! 🚀**

