# 📱 Guide Ultime : Déploiement d'AgaShop sur Android

Ce guide explique pas-à-pas comment générer l'application Android (fichier `.apk` ou `.aab`) à partir de votre projet Vue.js / Ionic / Capacitor.

---

## 🛠️ Étape 1 : Prérequis (À installer sur votre PC)
Pour compiler une application Android, votre ordinateur a besoin des outils de développement mobiles :
1. **[Android Studio](https://developer.android.com/studio)** : Téléchargez-le et installez-le. C'est le moteur de compilation.
2. Ouvrez Android Studio une première fois pour qu'il installe automatiquement le **Android SDK** par défaut.
3. Vérifiez que votre `.env` dans le dossier `frontend` pointe bien vers la production :
   ```env
   VITE_API_URL=https://api.agashop.bi/api
   ```
   *(Vous pouvez utiliser la commande `npm run setup:prod` pour le créer automatiquement).*

---

## ⚙️ Étape 2 : Préparation du code (Compilation Capacitor)
Ouvrez un terminal dans VS Code, placez-vous dans le dossier **`frontend/`** et suivez ces commandes :

1. **Générer les fichiers web (`dist/`)**
   ```bash
   npm run build
   ```
2. **Ajouter/Mettre à jour la plateforme Android**
   *(Si le dossier `android/` n'existe pas encore)*
   ```bash
   npx cap add android
   ```
3. **Synchroniser le code Web vers Android**
   *(Copie vos fichiers Vue.js fraîchement compilés dans le dossier Android)*
   ```bash
   npx cap sync android
   ```

*(Note : Votre `package.json` possède déjà des raccourcis. Vous pouvez simplement taper `npm run android:build`)*

---

## 🚀 Étape 3 : Compilation Finale dans Android Studio
Une fois la synchronisation terminée, il faut ouvrir le projet dans Android Studio pour générer l'APK.

1. **Lancer Android Studio depuis votre terminal**
   Toujours dans le dossier `frontend/`, tapez :
   ```bash
   npx cap open android
   ```
   *Android Studio va s'ouvrir automatiquement avec votre projet. Patientez (ça peut prendre quelques minutes) le temps que l'indexation et "Gradle Sync" se terminent (barre de chargement en bas).*

2. **Tester sur votre propre téléphone (Optionnel mais recommandé)**
   - Branchez votre téléphone Android en USB.
   - Activez le **"Débogage USB"** dans les options de développement de votre téléphone.
   - Votre téléphone apparaîtra en haut dans Android Studio. Cliquez sur le bouton ▶️ **Play (Run)** pour installer l'application dessus !

3. **Générer le Fichier `.APK` (Pour partager hors Play Store)**
   Dans Android Studio, allez dans la barre de menu en haut :
   - `Build` > `Build Bundle(s) / APK(s)` > `Build APK(s)`
   - Une petite notification apparaîtra en bas à droite une fois fini avec un lien **"locate"**. Cliquez dessus, voilà votre fichier `.apk` prêt à être envoyé par WhatsApp ou hébergé sur votre site !

4. **Générer le Fichier `.AAB` (Pour le Google Play Store)**
   - `Build` > `Generate Signed Bundle / APK...`
   - Choisissez **Android App Bundle**.
   - Créez un profil de signature (Keystore) avec un mot de passe sécurisé.
   - Suivez les étapes, et hébergez le `.aab` généré sur le **Google Play Console**.

---

## 🎨 Annexe : Changer le nom et l'icône de l'app
*  **Nom de l'App** : Ouvrez `android/app/src/main/res/values/strings.xml` et changez la valeur de `app_name`.
*  **Icône et Splash Screen** : Capacitor possède un outil automatique. Placez votre belle icône 1024x1024 (`icon.png`) et un écran de démarrage (`splash.png`) dans votre dossier racine et lancez :
   ```bash
   npm run cordova-res android --skip-config --copy
   # Ou avec le nouvel outil Capacitor Assets :
   npx @capacitor/assets generate --android
   ```
