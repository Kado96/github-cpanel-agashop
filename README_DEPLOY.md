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
