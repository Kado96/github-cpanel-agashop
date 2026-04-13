import { axiosOtp, axiosService } from '../../plugins/axios'

/**
 * Service de gestion des comptes et OTP
 * Correspond exactement à l'API backend: /api/accounts/accounts/
 */
export const accountsService = {
  /**
   * Récupérer la liste de tous les comptes
   * @returns {Promise} Liste des comptes (paginée)
   */
  getAllAccounts() {
    return axiosService.get('/accounts/accounts/')
  },

  /**
   * Récupérer un compte par ID
   * @param {number} accountId - ID du compte
   * @returns {Promise} Données du compte
   */
  getAccount(accountId) {
    return axiosService.get(`/accounts/accounts/${accountId}/`)
  },

  /**
   * Mettre à jour un compte
   * @param {number} accountId - ID du compte
   * @param {Object} accountData - Données du compte {phone_number, is_active, role}
   * @returns {Promise} Compte mis à jour
   */
  updateAccount(accountId, accountData) {
    return axiosService.patch(`/accounts/accounts/${accountId}/`, accountData)
  },

  /**
   * Supprimer un compte
   * @param {number} accountId - ID du compte
   * @returns {Promise} Réponse de l'API
   */
  deleteAccount(accountId) {
    return axiosService.delete(`/accounts/accounts/${accountId}/`)
  },

  /**
   * Réinitialiser le mot de passe d'un compte (admin/agent)
   * @param {number} accountId - ID du compte dont on veut réinitialiser le mot de passe
   * @returns {Promise} Réponse de l'API avec le statut et l'état de l'envoi d'email
   */
  resetPasswordForAccount(accountId) {
    return axiosService.post(`/accounts/accounts/${accountId}/force-reset-password/`)
  },

  /**
   * Vérifier le code OTP
   * @param {string} otpCode - Code OTP à vérifier (5 chiffres)
   * @returns {Promise} Réponse avec tokens et données utilisateur
   */
  verifyOtp(otpCode) {
    return axiosOtp.post('/accounts/accounts/verify_otp/', { otp_code: otpCode })
  },

  /**
   * Renvoyer le code OTP
   * @returns {Promise} Réponse de l'API
   */
  resendOtp() {
    return axiosOtp.get('/accounts/accounts/resend_otp/')
  }
}
