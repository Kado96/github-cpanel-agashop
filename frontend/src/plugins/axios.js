import axios from 'axios'
import store from '../store'
import { Capacitor } from '@capacitor/core'
import { alertController } from '@ionic/vue'

// Configuration de l'URL de l'API
// Pour utiliser l'API en ligne, utilisez: "https://api.agashop.bi/api"
// Pour utiliser l'API en local, utilisez: "http://localhost:8000/api"
const DEFAULT_LOCAL_API = "http://localhost:8000/api"
const API_BASE_URL = import.meta.env.VITE_API_URL || DEFAULT_LOCAL_API
const API_ONLINE_URL = import.meta.env.VITE_API_URL || DEFAULT_LOCAL_API

function url() {
  // En mode mobile (Capacitor), utiliser la variable VITE_API_URL ou le fallback local
  if (Capacitor.isNativePlatform()) {
    return API_ONLINE_URL
  }

  // Si une variable d'environnement est définie et qu'on n'est pas en mode natif, l'utiliser
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }

  // En mode web, détecter automatiquement (local vs production)
  if (typeof window !== 'undefined' && window.location) {
    let base_host = window.location.host.split(":")[0]
    let locals = ["localhost", "127.0.0.1"]

    if (locals.includes(base_host)) {
      return DEFAULT_LOCAL_API
    }
  }

  // Fallback de sécurité
  return API_BASE_URL
}

// Créer l'instance avec une URL par défaut (sera mise à jour par l'interceptor)
export const axiosService = axios.create({
  baseURL: url(),
  params: {}
})

// Interceptor pour forcer l'URL en mode natif à chaque requête
axiosService.interceptors.request.use((config) => {
  // Forcer l'utilisation de l'API en ligne en mode natif
  if (Capacitor.isNativePlatform()) {
    config.baseURL = API_ONLINE_URL
  }

  // Si on refresh la page, le store peut être vide -> relire depuis localStorage
  const safeParse = (val) => {
    try {
      if (!val || val === 'undefined' || val === 'null') return null
      return JSON.parse(val)
    } catch {
      return null
    }
  }

  const storedUser = safeParse(localStorage.getItem('user'))
  if (!store.state.user && storedUser) {
    store.state.user = storedUser
  }

  const access = store.state.user?.access
  if (access) {
    config.headers.Authorization = `Bearer ${access}`
  } else {
    // Éviter d'envoyer "Authorization: " vide (peut provoquer 401)
    delete config.headers.Authorization
    delete config.headers.authorization
  }
  return config
})

// Interceptor de réponse pour gérer le Paywall (403 Subscription Expired)
axiosService.interceptors.response.use(
  response => {
    // 🔥 Astuce.md: Robustesse contre la pagination DRF
    // Si la réponse contient .results (format paginé), on tente d'extraire les données utiles
    // tout en gardant une compatibilité ascendante.
    if (response.data && response.data.results && Array.isArray(response.data.results)) {
       // Silent handling
    }
    return response;
  },
  async error => {
    if (error.response && error.response.status === 403) {
      const data = error.response.data;
      // Vérifier si c'est notre erreur spécifique d'expiration
      if (data && data.detail && data.detail.code === 'SUBSCRIPTION_EXPIRED') {

        // Afficher une alerte bloquante (Paywall)
        const alert = await alertController.create({
          header: '⛔ Abonnement Expiré',
          subHeader: 'Accès Bloqué',
          message: 'Votre période d\'essai ou votre abonnement est terminé.\n\n' +
            'Pour continuer à utiliser AgaShop et accéder à vos données, veuillez régulariser votre situation.\n\n' +
            'Contactez le support :\n' +
            '• Tél : +257 61 00 00 00\n' +
            '• Email : info@agashop.bi',
          backdropDismiss: false, // Empêcher de fermer en cliquant à côté
          buttons: [
            {
              text: 'Se déconnecter',
              handler: () => {
                // Force logout
                localStorage.removeItem('user');
                localStorage.removeItem('current_shop');
                window.location.href = '/login';
              }
            },
            {
              text: 'J\'ai compris',
              role: 'cancel' // Laisse l'utilisateur sur la page mais l'action a échoué
            }
          ]
        });
        await alert.present();
      }
    }
    return Promise.reject(error);
  }
);

export const axiosOtp = axios.create({
  baseURL: url()
})

axiosOtp.interceptors.request.use((config) => {
  // Forcer l'utilisation de l'API en ligne en mode natif
  if (Capacitor.isNativePlatform()) {
    config.baseURL = API_ONLINE_URL
  }

  const safeParse = (val) => {
    try {
      if (!val || val === 'undefined' || val === 'null') return null
      return JSON.parse(val)
    } catch {
      return null
    }
  }

  const storedOtpUser = safeParse(localStorage.getItem('otp_user'))
  if (!store.state.otp_user && storedOtpUser) {
    store.state.otp_user = storedOtpUser
  }

  const otp = store.state.otp_user?.otp
  if (otp) {
    config.headers.Authorization = `Bearer ${otp}`
  } else {
    delete config.headers.Authorization
    delete config.headers.authorization
  }
  return config
})