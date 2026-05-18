# 🔄 Guide de Synchronisation : Production ➔ Local (AgaShop)

Ce guide explique comment utiliser le nouveau système de synchronisation automatique et sécurisé pour rapatrier les données réelles de production (base de données SQLite `db.sqlite3` et l'ensemble des fichiers médias de boutiques/produits) vers votre environnement de développement local.

---

## 🛠️ Étape 1 : Configuration du Jeton de Sécurité (Token)

Pour des raisons de sécurité évidentes, la synchronisation est protégée par un jeton secret unique défini sur le serveur et sur votre machine locale.

### 1. Sur le serveur de Production (cPanel) :
1. Connectez-vous à votre **cPanel**.
2. Allez dans le **Gestionnaire de fichiers** (ou via SSH) et ouvrez le fichier `.env` situé dans votre dossier API (`/home/agashopb/api/.env`).
3. Ajoutez la ligne suivante avec un token personnalisé très robuste (sans espaces, sans caractères spéciaux complexes) :
   ```env
   BACKUP_SYNC_TOKEN=VotreSuperCléSecrèteUniqueAgaShop2026!
   ```
4. Enregistrez le fichier.
5. Allez dans **Setup Python App** sur cPanel et cliquez sur **RESTART** pour que Django charge cette nouvelle configuration.

### 2. Sur votre PC Local (Windows) :
1. Ouvrez votre fichier `.env` local situé dans le dossier `backend/.env`.
2. Ajoutez le même token exact :
   ```env
   BACKUP_SYNC_TOKEN=VotreSuperCléSecrèteUniqueAgaShop2026!
   ```
3. Enregistrez le fichier.

---

## 🚀 Étape 2 : Lancer la Synchronisation en un clic

Une fois les jetons configurés, vous pouvez rapatrier toutes les données en ouvrant votre terminal et en lançant le script à la racine du projet :

```powershell
# Assurez-vous d'être à la racine du projet (e:\AgaShop\github-cpanel-agashop)
python sync_prod_to_local.py
```

### 📋 Ce que fait le script automatiquement :
1. **Sécurise les accès** : Charge votre token local et contacte l'API de production de manière sécurisée.
2. **Télécharge l'archive** : Télécharge par blocs (avec une jolie barre de progression en direct) le fichier ZIP de sauvegarde généré par le serveur.
3. **Crée un backup local** : Fait une copie de sauvegarde de votre ancienne base de données sous le nom `db.sqlite3.bak_YYYYMMDD_HHMMSS` (ainsi, aucun risque de perdre vos tests locaux !).
4. **Installe la DB de Prod** : Remplace votre `db.sqlite3` locale par celle de production.
5. **Synchronise les Médias** : Extrait et fusionne toutes les photos des boutiques et produits réels dans votre dossier local `backend/media/`.
6. **Nettoie le disque** : Supprime les fichiers ZIP temporaires pour laisser votre espace propre.

---

## ⚠️ Résolution des problèmes fréquents

### 🔒 Erreur : "La base locale db.sqlite3 est verrouillée"
* **Cause** : Votre serveur local de développement Django (`manage.py runserver`) ou un outil de base de données (comme DB Browser for SQLite) est en cours d'exécution et verrouille le fichier `db.sqlite3`.
* **Solution** :
  1. Arrêtez votre serveur Django local dans votre terminal (faites `Ctrl + C`).
  2. Fermez tout logiciel de base de données ouvert sur ce fichier.
  3. Appuyez sur `ENTRÉE` dans le script de synchronisation pour retenter l'opération.

### 🚫 Erreur : "Accès refusé ! Le jeton de synchronisation est invalide..."
* **Cause** : Le token spécifié dans le fichier `backend/.env` de votre PC ne correspond pas exactement à celui configuré dans le `.env` de production sur le serveur cPanel, ou le serveur n'a pas été redémarré.
* **Solution** :
  1. Vérifiez que la clé `BACKUP_SYNC_TOKEN` est strictement identique des deux côtés (majuscules/minuscules comprises).
  2. N'oubliez pas de cliquer sur **RESTART** dans l'outil **Setup Python App** de votre cPanel pour appliquer le changement.
