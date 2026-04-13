# 📱 AgaShop Mobile - Application Ionic Vue

Application mobile cross-platform (Android/iOS) pour la gestion complète des boutiques AgaShop. Développée avec **Ionic Vue** et **Capacitor**, consommant l'API REST Django en ligne.

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Fonctionnalités](#-fonctionnalités)
- [Configuration](#-configuration)
- [Installation et démarrage](#-installation-et-démarrage)
- [Créer une application Android qui utilise l'API en ligne](#-créer-une-application-android-qui-utilise-lapi-en-ligne)
- [Routes et pages](#-routes-et-pages)
- [Services API](#-services-api)
- [Déploiement](#-déploiement)
- [Ce qui reste à faire](#-ce-qui-reste-à-faire)
- [Dépannage](#-dépannage)

---

## 🎯 Vue d'ensemble

AgaShop Mobile est une application de gestion de boutiques permettant de :
- ✅ Gérer les produits et le stock
- ✅ Enregistrer les ventes et approvisionnements
- ✅ Contrôler le stock avec fréquence personnalisable
- ✅ Consulter les statistiques détaillées
- ✅ Gérer les modes de paiement
- ✅ Administrer les produits de base (catalogue)
- ✅ Gérer les utilisateurs et boutiques (admin/agent)

**Technologies utilisées :**
- **Ionic Vue** : Framework UI mobile
- **Vue 3** : Framework JavaScript
- **Vuex** : Gestion d'état
- **Axios** : Client HTTP
- **Capacitor** : Bridge natif pour Android/iOS
- **Vite** : Build tool moderne

**API Backend :**
- **URL Production** : `https://api.agashop.bi/api`
- **Authentification** : JWT (JSON Web Tokens)
- **Format** : REST API

---

## ✨ Fonctionnalités

### 🔐 Authentification

1. **Connexion (Login)**
   - Authentification par email et mot de passe
   - Sauvegarde automatique des tokens JWT dans localStorage
   - Gestion automatique du refresh token
   - Redirection intelligente (OTP si compte non validé, accueil sinon)
   - Support des rôles : Utilisateur, Agent, Admin

2. **Inscription (Register)**
   - Création de compte avec email, téléphone et mot de passe
   - Formatage automatique du numéro burundais (+257)
   - Validation du format de numéro
   - Envoi automatique du code OTP par email
   - Redirection vers la page de connexion après inscription

3. **Vérification OTP**
   - Validation du code OTP reçu par email
   - Possibilité de renvoyer le code
   - Création automatique de la boutique après validation
   - Activation du compte

4. **Récupération de mot de passe**
   - Réinitialisation par email
   - Génération automatique d'un nouveau mot de passe
   - Invalidation des anciennes sessions (blacklist tokens)

### 🏪 Gestion des boutiques

- **Tableau de bord** : Vue d'ensemble avec accès rapide aux fonctionnalités
- **Menu contextuel** : Affichage dynamique selon le rôle utilisateur
- **Gestion multi-boutiques** : Support pour plusieurs boutiques par utilisateur
- **Géolocalisation** : Enregistrement de la position GPS (prévu)

### 📦 Gestion des produits

1. **Liste des produits**
   - Affichage de tous les produits de la boutique
   - Filtrage et recherche
   - Informations : nom, prix, stock, catégorie

2. **Ajout/Modification de produits**
   - Création de produits à partir du catalogue de base
   - Définition des prix d'achat et de vente
   - Gestion des unités de mesure (entrée/sortie)
   - Upload d'images (si disponible)

3. **Catalogue de produits de base** (Admin/Agent)
   - Gestion du catalogue centralisé
   - Création, modification, suppression
   - Association avec catégories et sous-catégories
   - Import depuis Excel (prévu)

### 📊 Contrôle du stock

- **Contrôle de stock** : Enregistrement de la quantité restante
- **Calcul automatique** : Vente = Stock initial - Stock restant
- **Fréquence personnalisable** : Configuration par boutique (jours, heures, minutes)
- **Historique** : Traçabilité complète des contrôles
- **Validation** : Vérification que la quantité restante est cohérente

### 💰 Ventes

- **Enregistrement automatique** : Création lors du contrôle de stock
- **Liste des ventes** : Historique complet avec filtres
- **Calcul du montant** : Prix × Quantité vendue
- **Statistiques** : Bénéfices et totaux par période

### 🛒 Approvisionnements

- **Enregistrement des achats** : Quantité et prix total
- **Mise à jour automatique** : Stock et prix d'achat
- **Historique** : Liste complète des approvisionnements
- **Calcul des bénéfices** : Comparaison prix achat/vente

### 📈 Statistiques

1. **Statistiques gratuites** (`/stats/free`)
   - Vue d'ensemble des ventes et approvisionnements
   - Totaux de base

2. **Statistiques premium** (`/stats`)
   - Bénéfices détaillés
   - Statistiques par période (filtres date)
   - Graphiques et visualisations (prévu)
   - Export des données (prévu)

### 💳 Modes de paiement

- **Gestion des modes de paiement** : Création et configuration
- **Association aux ventes** : Enregistrement du mode de paiement utilisé

### 👥 Administration (Admin/Agent uniquement)

1. **Gestion des utilisateurs** (`/admin/users`)
   - Liste des utilisateurs
   - Création, modification, suppression
   - Filtrage par agent (agents voient leurs utilisateurs)

2. **Gestion des boutiques** (`/admin/shops`)
   - Liste de toutes les boutiques
   - Création, modification, suppression
   - Gestion des permissions

3. **Gestion du catalogue** (`/admin/basic-products`)
   - CRUD complet sur les produits de base
   - Gestion des catégories et sous-catégories
   - Import/Export (prévu)

4. **Paramètres** (`/admin/settings`)
   - Configuration globale de l'application

### 🔔 Notifications (Prévu)

- Notifications push pour événements importants
- Alertes de stock faible
- Notifications d'abonnement

---

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
# Pour utiliser l'API en ligne (production) - RECOMMANDÉ
VITE_API_URL=https://api.agashop.bi/api

# Pour utiliser l'API en local (développement uniquement)
# VITE_API_URL=http://localhost:8000/api
```

**Note importante :**
- En mode **mobile** (Android/iOS), l'application utilise **toujours** l'API en ligne (`https://api.agashop.bi/api`)
- Le fichier `.env` est utilisé uniquement pour le développement web
- L'API en ligne est la configuration par défaut si aucune variable n'est définie

### Configuration Capacitor

Le fichier `capacitor.config.ts` contient :
- **App ID** : `bi.sales.agashop`
- **App Name** : `AgaShop`
- **Web Dir** : `dist`

---

## 🚀 Installation et démarrage

### Prérequis

- **Node.js** 18+ et npm
- **Android Studio** (pour Android)
- **Xcode** (pour iOS, macOS uniquement)
- **Git** (optionnel)

### Installation

```bash
# 1. Installer les dépendances
npm install

# 2. Créer le fichier .env (optionnel pour développement)
echo "VITE_API_URL=https://api.agashop.bi/api" > .env
```

### Développement web

```bash
# Démarrer le serveur de développement
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

### Build de production

```bash
# Générer les fichiers de production
npm run build
```

Les fichiers seront générés dans le dossier `dist/`

---

## 📱 Créer une application Android qui utilise l'API en ligne

### Guide étape par étape

#### Étape 1 : Préparer l'environnement

1. **Installer Android Studio**
   - Téléchargez depuis [developer.android.com](https://developer.android.com/studio)
   - Installez Android SDK, Android SDK Platform-Tools, et Android Emulator

2. **Vérifier la configuration**
   ```bash
   # Vérifier que Java est installé
   java -version
   
   # Vérifier que Android SDK est configuré
   echo $ANDROID_HOME
   ```

#### Étape 2 : Configurer l'API en ligne

L'application est **déjà configurée** pour utiliser l'API en ligne par défaut.

**Vérification :**
- Ouvrez `src/plugins/axios.js` ou `src/composables/mixins.js`
- L'URL de base doit être : `https://api.agashop.bi/api`
- Si vous modifiez, assurez-vous que l'URL pointe vers l'API en production

#### Étape 3 : Build de production

```bash
# 1. Build de l'application
npm run build

# 2. Synchroniser avec Capacitor
npm run cap:sync
```

Cette commande :
- Compile l'application Vue
- Copie les fichiers dans `dist/`
- Synchronise avec le projet Android

#### Étape 4 : Ouvrir dans Android Studio

```bash
# Ouvrir Android Studio
npm run cap:open:android
```

Ou manuellement :
1. Ouvrez Android Studio
2. File → Open
3. Sélectionnez le dossier `android/` dans le projet

#### Étape 5 : Configurer le projet Android

1. **Vérifier le build.gradle**
   - Le fichier `android/app/build.gradle` doit contenir les bonnes configurations
   - Version minimale SDK : 22 (Android 5.1)
   - Version cible SDK : 33+ (Android 13+)

2. **Configurer les permissions** (déjà fait)
   - Internet : Pour accéder à l'API
   - Network State : Pour vérifier la connexion

3. **Vérifier l'App ID**
   - Dans `capacitor.config.ts` : `appId: 'bi.sales.agashop'`
   - Dans `android/app/build.gradle` : `applicationId "bi.sales.agashop"`

#### Étape 6 : Tester sur émulateur ou appareil

1. **Créer un émulateur** (si nécessaire)
   - Tools → Device Manager → Create Device
   - Choisir un appareil (ex: Pixel 5)
   - Choisir une version Android (API 33+)

2. **Connecter un appareil physique** (optionnel)
   - Activer le mode développeur
   - Activer le débogage USB
   - Connecter via USB

3. **Lancer l'application**
   - Cliquez sur le bouton "Run" (▶) dans Android Studio
   - Ou utilisez : `npm run android:run`

#### Étape 7 : Générer l'APK

1. **APK de débogage** (pour tests)
   ```bash
   # Dans Android Studio
   Build → Build Bundle(s) / APK(s) → Build APK(s)
   ```
   L'APK sera dans : `android/app/build/outputs/apk/debug/app-debug.apk`

2. **APK de release** (pour distribution)
   ```bash
   # 1. Générer une clé de signature (première fois)
   keytool -genkey -v -keystore agashop-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias agashop
   
   # 2. Configurer la signature dans build.gradle
   # Ajouter dans android/app/build.gradle :
   android {
       signingConfigs {
           release {
               storeFile file('../agashop-release-key.jks')
               storePassword 'votre_mot_de_passe'
               keyAlias 'agashop'
               keyPassword 'votre_mot_de_passe'
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
           }
       }
   }
   
   # 3. Build de release
   # Dans Android Studio : Build → Generate Signed Bundle / APK → APK
   ```

#### Étape 8 : Vérifier la connexion à l'API

1. **Lancer l'application**
2. **Tester la connexion**
   - Se connecter avec un compte existant
   - Vérifier que les données se chargent depuis l'API
   - Vérifier la console pour les erreurs

2. **Vérifier les logs**
   ```bash
   # Dans Android Studio
   Logcat → Filtrer par "AgaShop" ou "Capacitor"
   ```

### Commandes rapides

```bash
# Build complet (build + sync + open)
npm run cap:build:android

# Build et synchroniser uniquement
npm run android:build

# Synchroniser uniquement
npm run cap:sync

# Ouvrir Android Studio
npm run cap:open:android

# Lancer sur appareil/émulateur
npm run android:run
```

### Configuration de l'API dans le code

L'URL de l'API est définie dans plusieurs endroits :

1. **Service Axios** (`src/plugins/axios.js`)
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'https://api.agashop.bi/api'
   ```

2. **Mixins** (`src/composables/mixins.js`)
   ```javascript
   const API_URL = import.meta.env.VITE_API_URL || 'https://api.agashop.bi/api'
   ```

**Important :** En mode mobile, `import.meta.env.VITE_API_URL` sera `undefined`, donc l'API en ligne sera utilisée automatiquement.

### Résolution des problèmes courants

1. **L'application ne se connecte pas à l'API**
   - Vérifiez la connexion Internet
   - Vérifiez que l'API est accessible : `https://api.agashop.bi/api`
   - Vérifiez les logs dans Logcat
   - Vérifiez les permissions Internet dans `AndroidManifest.xml`

2. **Erreurs CORS**
   - Les erreurs CORS ne devraient pas apparaître en mode natif
   - Si elles apparaissent, vérifiez la configuration CORS côté API

3. **Tokens expirés**
   - Le refresh token est géré automatiquement
   - Vérifiez que le localStorage fonctionne (Capacitor Storage)

---

## 🗺️ Routes et pages

### Routes publiques (non authentifiées)

| Route | Page | Description |
|-------|------|-------------|
| `/login` | `LoginPage.vue` | Page de connexion |
| `/register` | `RegisterPage.vue` | Page d'inscription |
| `/forgot-password` | `ForgotPasswordPage.vue` | Récupération de mot de passe |
| `/forgot-password/success` | `ForgotPasswordSuccessPage.vue` | Confirmation d'envoi |
| `/otp` | `OTPPage.vue` | Vérification du code OTP |

### Routes protégées (authentifiées)

| Route | Page | Description | Rôle |
|-------|------|-------------|------|
| `/` | `ShopHome.vue` | Tableau de bord | Tous |
| `/shop` | `ShopHome.vue` | Gestion de la boutique | Tous |
| `/products` | `ShopProducts.vue` | Liste des produits | Tous |
| `/controls` | `ControlProducts.vue` | Contrôle du stock | Tous |
| `/sales` | `SalesProducts.vue` | Liste des ventes | Tous |
| `/supplies` | `SupplyProducts.vue` | Liste des approvisionnements | Tous |
| `/supplies/actions` | `SupplyProductActions.vue` | Actions sur approvisionnements | Tous |
| `/stats` | `ShopStats.vue` | Statistiques premium | Tous |
| `/stats/free` | `FreeStats.vue` | Statistiques gratuites | Tous |
| `/payment-methods` | `PaymentMethods.vue` | Modes de paiement | Tous |

### Routes admin/agent (authentifiées + permissions)

| Route | Page | Description | Rôle |
|-------|------|-------------|------|
| `/admin` | `AdminHome.vue` | Tableau de bord admin | Admin |
| `/agent` | `AgentHome.vue` | Tableau de bord agent | Agent |
| `/admin/users` | `AdminUsers.vue` | Gestion des utilisateurs | Admin uniquement |
| `/admin/shops` | `AdminShops.vue` | Gestion des boutiques | Admin/Agent |
| `/admin/basic-products` | `ManageBasicProducts.vue` | Gestion du catalogue | Admin/Agent |
| `/admin/settings` | `AdminSettings.vue` | Paramètres | Admin/Agent |

### Protection des routes

- **Middleware d'authentification** : Vérifie la présence du token JWT
- **Vérification des rôles** : Redirection si l'utilisateur n'a pas les permissions
- **Redirection automatique** : Vers `/login` si non authentifié

---

## 🔌 Services API

L'application utilise des services centralisés pour communiquer avec l'API :

### Services disponibles

- **`authService`** : Authentification (login, register, refresh, logout)
- **`accountsService`** : Gestion des comptes (OTP, reset password)
- **`usersService`** : Gestion des utilisateurs
- **`shopsService`** : Gestion des boutiques
- **`productsService`** : Gestion des produits
- **`basicProductsService`** : Gestion du catalogue
- **`salesService`** : Gestion des ventes
- **`suppliesService`** : Gestion des approvisionnements
- **`categoriesService`** : Gestion des catégories
- **`subCategoriesService`** : Gestion des sous-catégories
- **`provincesService`** : Liste des provinces
- **`controlFrequencyService`** : Fréquence de contrôle
- **`historyService`** : Historique (admin)

### Exemple d'utilisation

```javascript
import { authService, shopsService } from '@/services/api'

// Connexion
const response = await authService.login(email, password)

// Récupérer les boutiques
const shops = await shopsService.getAll()
```

### Gestion automatique des tokens

- **Ajout automatique** : Le token est ajouté à chaque requête
- **Refresh automatique** : Renouvellement si le token expire
- **Gestion des erreurs** : Redirection vers login si 401

---

## 📦 Déploiement

### Application Web

Les fichiers dans `dist/` peuvent être déployés sur :
- Serveur web statique (Nginx, Apache)
- CDN (Cloudflare, AWS CloudFront)
- Services d'hébergement (Netlify, Vercel)

### Application Android

1. **Générer l'APK de release** (voir section précédente)
2. **Tester l'APK** sur plusieurs appareils
3. **Publier sur Google Play Store** :
   - Créer un compte développeur
   - Créer une nouvelle application
   - Uploader l'APK/AAB
   - Remplir les métadonnées
   - Soumettre pour révision

### Application iOS

1. **Ouvrir dans Xcode** : `npm run cap:open:ios`
2. **Configurer les certificats** : Apple Developer Account
3. **Build et archiver** : Product → Archive
4. **Publier sur App Store** : Via Xcode ou App Store Connect

---

## 📝 Ce qui reste à faire

### 🔴 Priorité haute

1. **Gestion des dépenses**
   - [ ] Créer la page Dépenses
   - [ ] Intégrer avec l'API (endpoints à créer)
   - [ ] Ajouter dans les statistiques
   - [ ] Formulaire de saisie

2. **Gestion des commissions** (Agent/Admin)
   - [ ] Page de visualisation des commissions
   - [ ] Intégration avec l'API
   - [ ] Calcul et affichage

3. **Système d'abonnements**
   - [ ] Page d'abonnement
   - [ ] Affichage du plan actuel
   - [ ] Intégration avec système de paiement
   - [ ] Vérification des fonctionnalités premium

4. **Notifications push**
   - [ ] Configuration Capacitor Push Notifications
   - [ ] Intégration avec le backend
   - [ ] Gestion des notifications locales

### 🟡 Priorité moyenne

5. **Amélioration des statistiques**
   - [ ] Graphiques et visualisations (Chart.js, etc.)
   - [ ] Export PDF/Excel
   - [ ] Filtres avancés
   - [ ] Prévisions financières

6. **Gestion des images**
   - [ ] Upload d'images pour produits
   - [ ] Utilisation de la caméra (Capacitor Camera)
   - [ ] Compression et optimisation

7. **Recherche avancée**
   - [ ] Recherche full-text dans les produits
   - [ ] Filtres multiples
   - [ ] Tri et pagination améliorés

8. **Mode hors ligne** (PWA)
   - [ ] Service Worker
   - [ ] Cache des données
   - [ ] Synchronisation automatique

### 🟢 Priorité basse

9. **Amélioration UX/UI**
   - [ ] Animations et transitions
   - [ ] Thème sombre
   - [ ] Personnalisation

10. **Tests**
    - [ ] Tests unitaires (Vitest)
    - [ ] Tests E2E (Cypress)
    - [ ] Tests sur appareils réels

11. **Documentation**
    - [ ] Guide utilisateur
    - [ ] Vidéos tutoriels
    - [ ] FAQ

12. **Performance**
    - [ ] Optimisation des images
    - [ ] Lazy loading
    - [ ] Code splitting

---

## 🔍 Dépannage

### L'application ne se connecte pas à l'API

**Symptômes :** Erreurs réseau, timeout, 404

**Solutions :**
1. Vérifiez que le fichier `.env` existe et contient la bonne URL
2. Vérifiez la console du navigateur (F12) pour les erreurs
3. Vérifiez que l'API est accessible : `https://api.agashop.bi/api`
4. Vérifiez les erreurs CORS (ne devrait pas arriver en natif)
5. Vérifiez la connexion Internet
6. Vérifiez les logs dans Android Studio (Logcat)

### Le token expire trop vite

**Symptômes :** Déconnexion fréquente, erreurs 401

**Solutions :**
1. Les tokens expirent après 3 jours (access) et 6 jours (refresh)
2. Le refresh automatique devrait gérer cela
3. Vérifiez les logs pour voir si le refresh fonctionne
4. Vérifiez que le localStorage fonctionne correctement

### Problèmes de localStorage

**Symptômes :** Données perdues au redémarrage, déconnexion

**Solutions :**
1. Videz le cache du navigateur
2. Vérifiez que localStorage n'est pas désactivé
3. En mode mobile, utilisez Capacitor Preferences au lieu de localStorage

### L'application ne se compile pas

**Symptômes :** Erreurs de build, dépendances manquantes

**Solutions :**
1. Supprimez `node_modules` et `package-lock.json`
2. Réinstallez : `npm install`
3. Vérifiez la version de Node.js : `node -v` (18+)
4. Vérifiez les erreurs dans la console

### Problèmes Android

**Symptômes :** Erreurs Gradle, APK ne se génère pas

**Solutions :**
1. Vérifiez que Android Studio est à jour
2. Vérifiez que le SDK Android est installé
3. Nettoyez le projet : `cd android && ./gradlew clean`
4. Rebuild : `npm run cap:sync` puis rebuild dans Android Studio

### Les images ne s'affichent pas

**Symptômes :** Images manquantes, erreurs 404

**Solutions :**
1. Vérifiez que les URLs d'images sont correctes
2. Vérifiez que l'API renvoie les bonnes URLs
3. Vérifiez les permissions Internet dans AndroidManifest.xml
4. Vérifiez CORS côté API pour les images

---

## 📚 Guides Disponibles

- **[GENERER_APK.md](./GENERER_APK.md)** - ⚡ Guide simple : Générer un APK
- **[QUICK_START.md](./QUICK_START.md)** - Démarrage rapide pour Android (5 minutes)
- **[GUIDE_ANDROID.md](./GUIDE_ANDROID.md)** - Guide complet Android (build, APK, Play Store)
- **[README.md](./README.md)** - Documentation générale (ce fichier)

---

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation dans les guides
2. Vérifiez les logs dans la console/Logcat
3. Vérifiez que l'API est accessible
4. Contactez l'équipe de développement

---

## ✅ Fonctionnalités implémentées

- ✅ Authentification complète (login, register, OTP, reset password)
- ✅ Gestion des produits (CRUD)
- ✅ Contrôle du stock
- ✅ Ventes et approvisionnements
- ✅ Statistiques de base
- ✅ Gestion des modes de paiement
- ✅ Administration (utilisateurs, boutiques, catalogue)
- ✅ Gestion des rôles (utilisateur, agent, admin)
- ✅ Refresh token automatique
- ✅ Protection des routes
- ✅ Support Android/iOS via Capacitor

---

**Dernière mise à jour** : Janvier 2025  
**Version** : 0.0.1  
**API Backend** : `https://api.agashop.bi/api`

