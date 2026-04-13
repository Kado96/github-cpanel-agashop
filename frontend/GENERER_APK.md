# 📱 Comment Générer un APK - Guide Simple

## 📁 Structure de vos dossiers

```
Frontend/
├── agashop_mobile/    ← ⭐ APPLICATION MOBILE (vous travaillez ici)
│   ├── src/           ← Code source de l'application
│   ├── android/       ← Projet Android (créé automatiquement)
│   └── ...
└── api/               ← ❌ BACKEND/API (déjà en ligne, pas besoin)
```

**Réponse à votre question :** Vous ouvrez **`agashop_mobile/android/`** dans Android Studio.

> **Note :** Le dossier `android/` sera créé automatiquement lors de `npm run cap:sync`. Vous n'avez pas besoin de le créer manuellement.

---

## ❓ Question : Dois-je modifier l'API sur cPanel ?

**Réponse : NON ! ❌**

L'application mobile est **déjà configurée** pour utiliser l'API en ligne (`https://api.agashop.bi/api`). 

**Vous n'avez rien à modifier sur cPanel !** ✅

---

## ✅ Ce que vous devez vérifier

### 1. L'API est-elle accessible ?

Testez simplement si l'API répond :

```bash
# Dans votre navigateur ou terminal
curl https://api.agashop.bi/api/
```

Ou ouvrez dans votre navigateur : `https://api.agashop.bi`

**Si l'API répond, c'est bon !** ✅

### 2. L'API est-elle déjà en ligne ?

Si votre API est déjà déployée sur cPanel et accessible à `https://api.agashop.bi`, **c'est parfait !** 

L'application mobile utilisera automatiquement cette URL.

---

## 🚀 Générer l'APK (Sans modifier l'API)

### 📁 Structure de vos dossiers

```
Frontend/
├── agashop_mobile/    ← ⭐ VOUS TRAVAILLEZ ICI (application mobile)
└── api/               ← ❌ PAS BESOIN (backend déjà en ligne)
```

**Vous ouvrez uniquement :** `agashop_mobile/` dans Android Studio

### Étape 1 : Build de l'application

```bash
cd agashop_mobile
npm run build
```

Cette commande compile votre application avec l'URL de l'API déjà configurée (`https://api.agashop.bi/api`).

### Étape 2 : Ajouter la plateforme Android (Première fois uniquement)

**⚠️ IMPORTANT :** Si vous voyez l'erreur `android platform has not been added yet`, vous devez d'abord ajouter la plateforme Android :

```bash
npm run cap:add:android
```

Ou directement :
```bash
npx cap add android
```

Cette commande crée le dossier `android/` dans votre projet.

> **Note :** Cette étape n'est nécessaire **qu'une seule fois**. Une fois le dossier `android/` créé, vous pouvez passer directement à l'étape 3.

### Étape 3 : Synchroniser avec Android

```bash
npm run cap:sync
```

Cette commande copie les fichiers du build vers le projet Android.

### Étape 4 : Ouvrir Android Studio

```bash
npm run cap:open:android
```

**⚠️ Important :** Cette commande va :
1. Créer automatiquement le dossier `android/` dans `agashop_mobile/` (si pas déjà créé)
2. Ouvrir Android Studio avec le projet `agashop_mobile/android/`

**Vous ouvrez :** `agashop_mobile/android/` (pas le dossier `api` !)

> **Note :** Le dossier `api` est votre backend (déjà en ligne). Vous n'avez pas besoin de l'ouvrir dans Android Studio.

### Étape 5 : Générer l'APK dans Android Studio

1. Dans Android Studio, attendez que le projet soit indexé (barre de progression en bas)
2. Menu : `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
3. Attendez la fin du build
4. Cliquez sur `locate` dans la notification
5. L'APK sera dans : `agashop_mobile/android/app/build/outputs/apk/debug/app-debug.apk`

**C'est tout !** 🎉

---

## 🔍 Vérification : L'APK utilise-t-il la bonne API ?

### Comment vérifier ?

1. **Installez l'APK** sur un appareil Android
2. **Ouvrez l'application**
3. **Essayez de vous connecter**
4. **Si la connexion fonctionne** → L'API est bien utilisée ✅

### Si ça ne fonctionne pas

Vérifiez que :
- ✅ L'API est accessible : `https://api.agashop.bi`
- ✅ L'appareil a une connexion Internet
- ✅ L'API accepte les requêtes depuis les applications mobiles (CORS configuré)

---

## 📝 Configuration actuelle de l'application

L'application est configurée dans `src/plugins/axios.js` :

```javascript
// En mode mobile (Capacitor), toujours utiliser l'API en ligne
if (Capacitor.isNativePlatform()) {
  return "https://api.agashop.bi/api"
}
```

**Donc :**
- ✅ En mode mobile → Utilise automatiquement `https://api.agashop.bi/api`
- ✅ Aucune modification nécessaire
- ✅ Aucun fichier `.env` nécessaire pour l'APK

---

## 🎯 Résumé

| Action | Nécessaire ? |
|--------|--------------|
| Modifier l'API sur cPanel | ❌ **NON** |
| Vérifier que l'API est accessible | ✅ **OUI** (juste tester) |
| Build de l'application | ✅ **OUI** |
| Générer l'APK | ✅ **OUI** |

---

## 🚨 Cas particuliers

### Si vous voulez changer l'URL de l'API

**Seulement si** vous avez une autre URL d'API :

1. Modifiez `src/plugins/axios.js` ligne 18 :
   ```javascript
   return "https://votre-nouvelle-api.com/api"
   ```

2. Rebuild :
   ```bash
   npm run build
   npm run cap:sync
   ```

**Mais normalement, ce n'est pas nécessaire !** L'API est déjà configurée.

---

## ✅ Checklist avant de générer l'APK

- [ ] L'API est accessible : `https://api.agashop.bi` ✅
- [ ] L'application fonctionne en mode web (test : `npm run dev`)
- [ ] Les dépendances sont installées : `npm install`
- [ ] Android Studio est installé
- [ ] **La plateforme Android est ajoutée** : `npm run cap:add:android` (première fois uniquement)
- [ ] Le projet est synchronisé : `npm run cap:sync`

**C'est tout !** Vous pouvez générer l'APK maintenant. 🚀

---

## 📞 Besoin d'aide ?

Si vous avez des problèmes :

1. Vérifiez que l'API répond : `https://api.agashop.bi`
2. Vérifiez les logs dans Android Studio (`Logcat`)
3. Consultez [GUIDE_ANDROID.md](./GUIDE_ANDROID.md) pour plus de détails

---

**En résumé : L'API est déjà configurée, vous n'avez qu'à générer l'APK !** 🎉

