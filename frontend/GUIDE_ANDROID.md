# 📱 Guide de Déploiement Android - AgaShop Mobile

Guide complet pour construire et déployer l'application AgaShop sur Android.

---

## 📋 Prérequis

### 1. Outils nécessaires

- **Node.js** (version 18 ou supérieure)
- **Java JDK** (version 17 ou supérieure)
- **Android Studio** (dernière version)
- **Android SDK** (via Android Studio)
- **Git** (optionnel, pour le contrôle de version)

### 2. Installation d'Android Studio

1. Téléchargez Android Studio depuis : https://developer.android.com/studio
2. Installez Android Studio avec les composants par défaut
3. Ouvrez Android Studio et installez :
   - Android SDK
   - Android SDK Platform-Tools
   - Android SDK Build-Tools
   - Android Emulator (optionnel, pour tester)

### 3. Configuration des variables d'environnement

#### Windows

1. Ouvrez les **Variables d'environnement système**
2. Ajoutez les variables suivantes :

```
ANDROID_HOME = C:\Users\VotreNom\AppData\Local\Android\Sdk
JAVA_HOME = C:\Program Files\Java\jdk-17
```

3. Ajoutez au **PATH** :
```
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\tools
%ANDROID_HOME%\tools\bin
%JAVA_HOME%\bin
```

#### Linux / macOS

Ajoutez dans votre `~/.bashrc` ou `~/.zshrc` :

```bash
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk  # Ajustez selon votre installation
```

Puis rechargez : `source ~/.bashrc` ou `source ~/.zshrc`

---

## 🚀 Configuration du Projet

### 1. Configuration de l'API

L'application est configurée pour utiliser l'API en ligne par défaut (`https://api.agashop.bi/api`).

**Optionnel :** Créez un fichier `.env` à la racine du projet si vous voulez changer l'URL :

```env
# Pour l'API en ligne (production)
VITE_API_URL=https://api.agashop.bi/api

# Pour l'API locale (développement uniquement)
# VITE_API_URL=http://localhost:8000/api
```

**Note :** Pour une application mobile, utilisez toujours l'API en ligne, car `localhost` ne fonctionnera pas sur un appareil physique.

### 2. Installation des dépendances

```bash
cd agashop_mobile
npm install
```

### 3. Vérification de Capacitor

Vérifiez que Capacitor est bien installé :

```bash
npx cap --version
```

---

## 🔨 Build de l'Application

### Étape 1 : Build de production

Construisez l'application web optimisée :

```bash
npm run build
```

Cette commande génère les fichiers dans le dossier `dist/`.

### Étape 2 : Synchronisation avec Capacitor

Synchronisez les fichiers web avec le projet Android :

```bash
npm run cap:sync
```

Ou directement :

```bash
npx cap sync
```

Cette commande :
- Copie les fichiers du dossier `dist/` vers le projet Android
- Met à jour les plugins Capacitor
- Synchronise la configuration

### Étape 3 : Ouvrir Android Studio

Ouvrez le projet Android dans Android Studio :

```bash
npm run cap:open:android
```

Ou directement :

```bash
npx cap open android
```

**Note :** La première fois, Android Studio peut prendre plusieurs minutes pour indexer le projet.

---

## 📦 Génération de l'APK (Application Package)

### Option 1 : Build via Android Studio (Recommandé)

1. **Ouvrez Android Studio** avec le projet (via `npx cap open android`)

2. **Attendez l'indexation** du projet (barre de progression en bas)

3. **Configurez le build** :
   - Menu : `Build` → `Generate Signed Bundle / APK`
   - Sélectionnez **APK** (pour tester) ou **Android App Bundle** (pour Play Store)

4. **Créez un Keystore** (si vous n'en avez pas) :
   - Cliquez sur `Create new...`
   - Remplissez les informations :
     - **Key store path** : Choisissez un emplacement sécurisé
     - **Password** : Créez un mot de passe fort
     - **Key alias** : `agashop-key`
     - **Key password** : Créez un mot de passe fort
     - **Validity** : 25 ans (recommandé)
     - **Certificate** : Remplissez vos informations
   - **⚠️ IMPORTANT :** Sauvegardez le keystore et les mots de passe en lieu sûr !

5. **Sélectionnez le keystore** et entrez les mots de passe

6. **Choisissez le type de build** :
   - **debug** : Pour tester (plus rapide, non sécurisé)
   - **release** : Pour production (signé, optimisé)

7. **Cliquez sur `Finish`**

8. **Localisation de l'APK** :
   - L'APK sera généré dans : `android/app/release/app-release.apk`
   - Android Studio affichera un message avec le chemin exact

### Option 2 : Build via ligne de commande

#### Build Debug (pour tester)

```bash
cd android
./gradlew assembleDebug
```

L'APK sera dans : `android/app/build/outputs/apk/debug/app-debug.apk`

#### Build Release (pour production)

1. **Configurez le keystore** dans `android/app/build.gradle` :

```gradle
android {
    ...
    signingConfigs {
        release {
            storeFile file('path/to/your/keystore.jks')
            storePassword 'your-store-password'
            keyAlias 'agashop-key'
            keyPassword 'your-key-password'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            ...
        }
    }
}
```

2. **Build l'APK** :

```bash
cd android
./gradlew assembleRelease
```

L'APK sera dans : `android/app/build/outputs/apk/release/app-release.apk`

**⚠️ Sécurité :** Ne commitez jamais le fichier `build.gradle` avec les mots de passe en clair. Utilisez des variables d'environnement ou un fichier `keystore.properties` (ajouté au `.gitignore`).

---

## 📲 Installation sur un Appareil Android

### Option 1 : Via USB (Appareil physique)

1. **Activez le mode développeur** sur votre appareil Android :
   - Allez dans `Paramètres` → `À propos du téléphone`
   - Tapez 7 fois sur `Numéro de build`
   - Retournez dans `Paramètres` → `Options pour les développeurs`
   - Activez `Débogage USB`

2. **Connectez l'appareil** via USB à votre ordinateur

3. **Autorisez le débogage** sur l'appareil (popup de confirmation)

4. **Vérifiez la connexion** :
   ```bash
   adb devices
   ```
   Vous devriez voir votre appareil listé.

5. **Installez l'APK** :
   ```bash
   adb install android/app/build/outputs/apk/debug/app-debug.apk
   ```

   Ou glissez-déposez l'APK directement sur l'appareil et installez-le manuellement.

### Option 2 : Via Android Studio

1. Connectez l'appareil via USB
2. Dans Android Studio, cliquez sur le bouton **Run** (▶️)
3. Sélectionnez votre appareil
4. L'application sera installée et lancée automatiquement

### Option 3 : Via Email / Cloud Storage

1. Uploadez l'APK sur Google Drive, Dropbox, etc.
2. Téléchargez l'APK sur votre appareil Android
3. Ouvrez le fichier APK
4. Autorisez l'installation depuis des sources inconnues si nécessaire
5. Installez l'application

---

## 🏪 Publication sur Google Play Store

### Étape 1 : Créer un compte développeur

1. Allez sur : https://play.google.com/console
2. Créez un compte développeur (frais unique de 25$)
3. Complétez votre profil développeur

### Étape 2 : Créer une nouvelle application

1. Dans la console Play, cliquez sur **Créer une application**
2. Remplissez les informations :
   - **Nom de l'application** : AgaShop
   - **Langue par défaut** : Français
   - **Type d'application** : Application
   - **Gratuite ou payante** : Gratuite

### Étape 3 : Préparer les ressources

Vous aurez besoin de :

- **Icône de l'application** : 512x512 px (PNG, 32 bits)
- **Capture d'écran** : Au moins 2 (recommandé : 4-8)
  - Téléphone : 1080 x 1920 px minimum
- **Graphique de présentation** : 1024 x 500 px (optionnel)
- **Description** : Description de l'application (jusqu'à 4000 caractères)
- **Politique de confidentialité** : URL vers votre politique

### Étape 4 : Générer un Android App Bundle (AAB)

Au lieu d'un APK, Google Play Store nécessite un **AAB** (Android App Bundle) :

1. Dans Android Studio :
   - Menu : `Build` → `Generate Signed Bundle / APK`
   - Sélectionnez **Android App Bundle**
   - Suivez les mêmes étapes que pour l'APK

2. Le fichier `.aab` sera généré dans : `android/app/release/app-release.aab`

### Étape 5 : Uploader l'application

1. Dans la console Play, allez dans **Production** (ou **Test interne** pour tester)

2. Cliquez sur **Créer une nouvelle version**

3. **Uploadez le fichier AAB** :
   - Glissez-déposez le fichier `.aab`
   - Ou cliquez sur **Télécharger** et sélectionnez le fichier

4. **Remplissez les notes de version** :
   - Décrivez les nouveautés de cette version
   - Exemple : "Première version de l'application AgaShop avec authentification et gestion des boutiques"

5. **Remplissez les autres sections** :
   - **Contenu de l'application** : Icône, captures d'écran, description
   - **Prix et distribution** : Pays, prix (gratuit)
   - **Évaluation du contenu** : Répondez aux questions
   - **Politique de confidentialité** : URL de votre politique

### Étape 6 : Soumettre pour révision

1. Vérifiez toutes les sections (icône verte ✅)
2. Cliquez sur **Envoyer pour révision**
3. Google examinera votre application (généralement 1-3 jours)
4. Une fois approuvée, l'application sera disponible sur le Play Store

---

## 🔧 Scripts Utiles

Ajoutés dans `package.json` :

```bash
# Build et synchroniser avec Android
npm run android:build

# Ouvrir Android Studio
npm run cap:open:android

# Synchroniser les fichiers
npm run cap:sync

# Build complet et ouvrir Android Studio
npm run cap:build:android
```

---

## 🐛 Dépannage

### Erreur : "ANDROID_HOME is not set"

**Solution :** Configurez les variables d'environnement (voir section Prérequis)

### Erreur : "SDK location not found"

**Solution :** 
1. Ouvrez Android Studio
2. `File` → `Settings` → `Appearance & Behavior` → `System Settings` → `Android SDK`
3. Notez le chemin du SDK
4. Créez un fichier `local.properties` dans `android/` :
   ```properties
   sdk.dir=C:\\Users\\VotreNom\\AppData\\Local\\Android\\Sdk
   ```
   (Ajustez le chemin selon votre installation)

### Erreur : "Gradle sync failed"

**Solution :**
1. Dans Android Studio : `File` → `Invalidate Caches / Restart`
2. Ou supprimez le dossier `.gradle` dans `android/` et resynchronisez

### L'application ne se connecte pas à l'API

**Vérifications :**
1. Vérifiez que l'API est accessible : `https://api.agashop.bi`
2. Vérifiez les permissions Internet dans `android/app/src/main/AndroidManifest.xml` :
   ```xml
   <uses-permission android:name="android.permission.INTERNET" />
   <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
   ```
3. Vérifiez les logs : `adb logcat | grep -i "agashop"`

### L'application crash au démarrage

**Solution :**
1. Vérifiez les logs : `adb logcat`
2. Assurez-vous que le build est à jour : `npm run build && npx cap sync`
3. Vérifiez que tous les plugins Capacitor sont installés

### Problème de permissions

Si l'application nécessite des permissions (caméra, localisation, etc.) :

1. Ajoutez dans `android/app/src/main/AndroidManifest.xml` :
   ```xml
   <uses-permission android:name="android.permission.CAMERA" />
   <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
   ```

2. Synchronisez : `npx cap sync`

---

## 📝 Checklist de Déploiement

Avant de publier sur le Play Store :

- [ ] Application testée sur plusieurs appareils Android
- [ ] Tous les bugs critiques corrigés
- [ ] Icône et captures d'écran préparées
- [ ] Description de l'application rédigée
- [ ] Politique de confidentialité créée et hébergée
- [ ] Keystore sauvegardé en lieu sûr
- [ ] Version de l'application mise à jour dans `package.json`
- [ ] Build de production testé
- [ ] AAB généré et testé
- [ ] Toutes les sections de la console Play remplies
- [ ] Application soumise pour révision

---

## 🔐 Sécurité

### Protection du Keystore

**⚠️ IMPORTANT :** Le keystore est nécessaire pour toutes les mises à jour futures de l'application. Perdre le keystore signifie ne plus pouvoir mettre à jour l'application sur le Play Store.

**Recommandations :**
1. Sauvegardez le keystore dans plusieurs endroits sécurisés
2. Utilisez un gestionnaire de mots de passe pour stocker les mots de passe
3. Ne commitez jamais le keystore dans Git
4. Documentez l'emplacement du keystore (hors du code)

### Variables d'environnement

Pour les builds de production, utilisez des variables d'environnement ou un fichier `keystore.properties` (ajouté au `.gitignore`) :

```properties
# keystore.properties (NE PAS COMMITER)
storePassword=votre-mot-de-passe-store
keyPassword=votre-mot-de-passe-key
keyAlias=agashop-key
storeFile=../path/to/keystore.jks
```

Puis dans `build.gradle` :

```gradle
def keystorePropertiesFile = rootProject.file("keystore.properties")
def keystoreProperties = new Properties()
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
        }
    }
}
```

---

## 📞 Support

Pour toute question ou problème :

1. Consultez la documentation Capacitor : https://capacitorjs.com/docs
2. Consultez la documentation Ionic : https://ionicframework.com/docs
3. Vérifiez les logs : `adb logcat`
4. Vérifiez la console du navigateur (si testé en mode web)

---

## 🎉 Félicitations !

Votre application AgaShop est maintenant prête à être déployée sur Android ! 🚀

**Résumé des commandes principales :**

```bash
# 1. Build de production
npm run build

# 2. Synchroniser avec Android
npm run cap:sync

# 3. Ouvrir Android Studio
npm run cap:open:android

# 4. Dans Android Studio : Build → Generate Signed Bundle / APK
```

---

**Dernière mise à jour :** Janvier 2025

