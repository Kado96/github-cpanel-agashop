# Guide de Déploiement AgaShop (cPanel)

Ce guide explique comment synchroniser votre code local avec le serveur de production sur cPanel, notamment parce que l'outil Git automatique de cPanel et la commande `rsync` sont limités sur cet hébergement.

## Workflow de Synchronisation

### 1. Sur votre ordinateur (Local)
Dès que vos modifications sont prêtes et testées :
```bash
git add .
git commit -m "Description de vos changements"
git push origin main
```

### 2. Sur le serveur (cPanel)
Comme le déploiement automatique peut échouer, utilisez le **Terminal cPanel** :

1. **Entrer dans le répertoire du projet** :
   ```bash
   cd /home/agapb/github-cpanelsho-agashop
   ```

2. **Récupérer le code depuis GitHub** :
   ```bash
   git pull origin main
   ```

3. **Synchroniser les fichiers vers l'API** (Utilise notre script Python de secours car `rsync` est indisponible) :
   ```bash
   python3 sync_to_api.py
   ```

### 3. Finalisation
Après chaque synchronisation, vous devez impérativement redémarrer l'application pour que le code soit lu par le serveur :
1. Allez dans cPanel > **Setup Python App**.
2. Cliquez sur le bouton **RESTART** en face de l'application.

---

## Fichiers de Déploiement
- `.cpanel.yml` : Configuration standard (parfois ignorée par cPanel).
- `sync_to_api.py` : Script Python robuste pour copier les fichiers du dossier `backend/` vers `/home/agashopb/api/` en ignorant les fichiers inutiles (venv, git, db, etc.).


# 1. On initialise Git en toute sécurité
git init

# 2. On connecte votre serveur à GitHub
git remote add origin https://github.com/Kado96/github-cpanel-agashop.git

# 3. On télécharge la mise à jour de GitHub (en silence, sans rien modifier pour le moment)
git fetch origin main

# 4. On écrase l'ancien code par le nouveau (vos dossiers media, venv, et node_modules resteront intacts)
git reset --hard origin/main




**1. OBJECTIF ACTUEL**
Résoudre l'erreur d'authentification (`Password authentication is not supported`) en remplaçant votre mot de passe par un Jeton d'Accès Sécurisé (Token) exigé par GitHub.

**2. PLAN DÉCOUPÉ**
1. **Alerte Sécurité** : Ne tapez plus votre mot de passe `Quicksales@...` : depuis 2021, GitHub bloque les mots de passe classiques dans les terminaux par mesure de piratage. 
2. **Génération d'un Token** : Créer un mot de passe spécial (Token) directement sur votre compte GitHub.
3. **Mise à jour Git** : Relancer la commande de `fetch` et coller ce nouveau Token à la place du mot de passe.

**3. AGENTS SOLLICITÉS**
- 🔐 **AGENT SÉCURITÉ / DÉPLOIEMENT** : Qui garantit la bonne connexion au dépôt distant sans compromettre les accès.

**4. POINTS DE VALIDATION**
- **Avez-vous accès à votre compte GitHub sur votre navigateur ?** Si oui, suivez ces étapes obligatoires.

**5. RISQUES IDENTIFIÉS**
- ⚠️ N'utilisez plus jamais votre vrai mot de passe en ligne de commande. Si vous perdez le Token, vous pourrez en regénérer un autre facilement à l'étape suivante.

**6. PROCHAINE ACTION (EN ATTENTE DE VALIDATION)**
Voici les étapes obligatoires pour générer votre Token et finir le déploiement. 

**ÉTAPE 1 : SUR GITHUB (Navigateur internet)**
1. Connectez-vous sur GitHub, cliquez sur votre photo de profil en haut à droite, et allez dans **Settings** (Paramètres).
2. Dans le menu de gauche, tout en bas, cliquez sur **Developer settings**.
3. Déroulez **Personal access tokens** et cliquez sur **Tokens (classic)**.
4. Cliquez en haut à droite sur **Generate new token (classic)**.
5. Dans "Note", tapez `cPanel AgaShop`.
6. Dans "Expiration", mettez ce que vous voulez (ex: *No expiration*).
7. **TRÈS IMPORTANT** : Dans la liste des cases à cocher, trouvez et **cochez la case "repo"** (cela donne accès à tout le code privé).
8. Descendez tout en bas et cliquez sur **Generate token**.
9. **Copiez le code secret généré** (il commence souvent par `ghp_`). Attention, il ne sera affiché qu'une seule fois !

**ÉTAPE 2 : SUR CPANEL (Dans le terminal)**
Maintenant, retournez sur votre terminal noir et relancez simplement :
```bash
git fetch origin main
```
- À la question *Username*, retapez `kado96`.
- À la question *Password*, **COLLEZ LE TOKEN** caché que vous venez de copier, puis faites `Entrée` ! *(Attention : dans le terminal Linux, quand vous collez un mot de passe, rien ne s'affiche à l'écran, c'est normal, c'est une sécurité, collez-le et faites juste la touche Entrée).*

Une fois que cela est fait, si ça marche, terminez avec :
```bash
git reset --hard origin/main
```

Dites-moi si vous avez pu générer le Token !


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





Essayez cette variante de la commande (plus robuste) 

curl -u "kado96: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" -L -o /home/agashopb/api/api/shops/viewsets/SupplyViewSet.py https://raw.githubusercontent.com/Kado96/github-cpanel-agashop/main/backend/api/shops/viewsets/SupplyViewSet.py
