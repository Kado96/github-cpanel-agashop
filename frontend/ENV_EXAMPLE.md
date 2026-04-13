# Configuration des variables d'environnement

## Fichiers d'exemple

Créez un fichier `.env` à la racine du projet avec l'une des configurations suivantes :

### Pour le développement LOCAL (API sur localhost)

```env
# .env (pour développement local)
VITE_API_URL=http://localhost:8000/api
```

### Pour la PRODUCTION (API en ligne)

```env
# .env (pour production)
VITE_API_URL=https://api.agashop.bi/api
```

## Comment utiliser

1. **Développement local** :
   ```bash
   # Créez .env avec l'URL locale
   echo "VITE_API_URL=http://localhost:8000/api" > .env
   npm run dev
   ```

2. **Production/Test avec API en ligne** :
   ```bash
   # Créez .env avec l'URL de production
   echo "VITE_API_URL=https://api.agashop.bi/api" > .env
   npm run dev
   ```

3. **Application Android** :
   - L'application Android utilise **toujours** l'API en ligne
   - Le fichier `.env` n'est pas utilisé en mode natif
   - La configuration est dans `src/plugins/axios.js`

## Notes importantes

- Le fichier `.env` est ignoré par Git (dans `.gitignore`)
- En mode mobile (Capacitor), l'API en ligne est utilisée automatiquement
- Le fichier `.env` est utilisé uniquement pour le développement web

