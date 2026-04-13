import { axiosService } from '../../plugins/axios'

/**
 * Service d'authentification
 * Correspond exactement à l'API backend: /api/login/, /api/register/, /api/refresh/
 */
export const authService = {
  /**
   * Connexion utilisateur
   * @param {string} username - Email de l'utilisateur
   * @param {string} password - Mot de passe
   * @returns {Promise} Réponse avec tokens et données utilisateur
   */
  login(username, password) {
    // Envoyer en JSON pour que le backend JWT reçoive bien username et password
    return axiosService.post('/login/', { username: (username || '').trim(), password: password || '' }, {
      headers: { 'Content-Type': 'application/json' }
    })
  },

  /**
   * Inscription d'un nouvel utilisateur
   * @param {Object} registerData - Données d'inscription {username, phone_number, password}
   * @returns {Promise} Réponse de l'API
   */
  register(registerData) {
    return axiosService.post('/register/', registerData)
  },

  /**
   * Rafraîchir le token d'accès
   * @param {string} refreshToken - Token de rafraîchissement
   * @returns {Promise} Nouveau token d'accès {access}
   */
  refreshToken(refreshToken) {
    return axiosService.post('/refresh/', { refresh: refreshToken })
  },

  /**
   * Réinitialiser le mot de passe
   * @param {string} email - Email de l'utilisateur
   * @returns {Promise} Réponse de l'API
   */
  resetPassword(email) {
    return axiosService.post('/accounts/accounts/reset-password/', { email })
  }
}
