# 🧹 Guide de Diagnostic et Nettoyage d'Espace Disque cPanel (AgaShop)

Ce guide s'adresse aux administrateurs rencontrant l'erreur **`Disk quota exceeded` (Errno 122)** ou **`user block limit reached`** sur un hébergement cPanel (souvent limité à 1 Go ou 2 Go). Il détaille la méthodologie pour identifier le gaspillage d'espace, supprimer les fichiers inutiles en toute sécurité, et libérer les quotas.

---

## 🔎 Étape 1 : Diagnostiquer l'occupation de l'espace disque

> [!WARNING]
> La commande standard `df -h` affiche l'espace du disque dur global du serveur physique. Elle **ne montre pas** le quota individuel de votre compte cPanel. Pour auditer votre quota utilisateur, utilisez les commandes ci-dessous.

Exécutez ces commandes dans le **Terminal cPanel** :

### 1. Connaître la taille de vos dossiers principaux
Affiche le volume de chaque répertoire à la racine de votre compte `/home/votredossier/`, trié du plus lourd au plus léger :
```bash
du -h --max-depth=1 /home/$(whoami) | sort -hr
```
*Exemple de diagnostic typique :*
- `/home/user/api` : Très lourd (ex: 700 Mo)
- `/home/user/.git` : Très lourd (ex: 120 Mo) -> **Alerte : Dépôt Git à la racine**
- `/home/user/github-cpanel-agashop` : Moyen (ex: 100 Mo) -> **Alerte : Clone dupliqué**

### 2. Lister les fichiers volumineux à la racine
Affiche tous les fichiers directement à la racine, triés par taille :
```bash
ls -lhS /home/$(whoami)
```
*(Permet de repérer des sauvegardes `.zip` ou `.tar.gz` oubliées).*

### 3. Inspecter en détail le dossier de l'API active
Pour savoir exactement ce qui pèse lourd dans votre application active :
```bash
du -h --max-depth=2 /home/$(whoami)/api | sort -hr
```
*(Permet de détecter des environnements virtuels imbriqués, des images en doublon ou des journaux d'erreurs `error_log` géants).*

---

## ⚠️ Les 4 pièges classiques qui saturent le quota cPanel

### 1. Le dossier Git invisible à la racine (`.git`) — ~120 Mo
* **Cause** : Exécution accidentelle de `git init` directement à la racine `/home/user/`.
* **Impact** : Git commence à suivre tout votre compte cPanel, créant des métadonnées volumineuses et inutiles.
* **Solution** : Supprimer le dossier `/home/user/.git`.

### 2. Le dépôt Git doublon (`github-cpanel-agashop` ou similaire) — ~100 Mo
* **Cause** : Clonage du projet dans un sous-dossier, alors que le dossier actif `api` possède déjà sa propre configuration Git et reçoit déjà le code.
* **Impact** : Deux copies complètes du projet coexistent sur le serveur.
* **Solution** : Supprimer le dossier de clonage secondaire si le dossier `api` gère déjà la liaison Git.

### 3. Les environnements virtuels imbriqués (`venv` ou `backend/venv`) — ~100 Mo à ~200 Mo
* **Cause** : Envoi accidentel des dossiers d'environnement virtuel local vers le serveur.
* **Impact** : cPanel utilise son propre dossier d'environnement virtuel géré par l'outil "Setup Python App" (situé dans `/home/user/virtualenv/`). Les dossiers `venv` internes à votre projet sont donc totalement inutilisés et consomment de l'espace.
* **Solution** : Supprimer les dossiers `venv` situés dans `api/venv` ou `api/backend/venv`.

### 4. La corbeille cachée de cPanel (`.trash`) — Variable (parfois plusieurs Go)
* **Cause** : Suppression de fichiers depuis le Gestionnaire de Fichiers cPanel sans cocher la case "Supprimer définitivement".
* **Impact** : Les fichiers supprimés sont déplacés dans un dossier caché `/home/user/.trash/` et continuent de consommer votre quota d'espace.
* **Solution** : Vider la corbeille.

---

## 🛠️ Script de Nettoyage Sécurisé

Copiez et collez ces commandes dans le **Terminal cPanel** de l'environnement saturé pour libérer instantanément jusqu'à **450 Mo** :

```bash
# 1. Supprimer le dépôt git erroné à la racine du compte cPanel
rm -rf /home/$(whoami)/.git

# 2. Supprimer le clone git doublon et inutile
rm -rf /home/$(whoami)/github-cpanel-agashop

# 3. Entrer dans le dossier de l'application active
cd /home/$(whoami)/api

# 4. Supprimer les environnements virtuels locaux et inutilisés dans l'application
rm -rf backend/venv
rm -rf venv

# 5. Vider définitivement la corbeille cachée de cPanel
rm -rf /home/$(whoami)/.trash/*
```

---

## 🚀 Étape 3 : Relancer le déploiement après nettoyage

Une fois l'espace libéré, vous pouvez mettre à jour votre code sans blocage :

```bash
# Force l'alignement des fichiers locaux sur la version propre de GitHub
cd /home/$(whoami)/api
git reset --hard origin/main

# Lance le script de synchronisation du backend et les migrations
python3 deploy_updates.py
```

> [!IMPORTANT]
> N'oubliez pas d'aller sur votre interface **cPanel > Setup Python App** et de cliquer sur **RESTART** face à votre application pour appliquer le nouveau code.
