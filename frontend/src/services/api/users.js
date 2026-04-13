import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des utilisateurs
 * Correspond exactement à l'API backend: /api/accounts/users/
 */
export const usersService = {
  /**
   * Récupérer la liste de tous les utilisateurs
   * @returns {Promise} Liste des utilisateurs (paginée)
   */
  getAllUsers() {
    return axiosService.get('/accounts/users/')
  },

  /**
   * Récupérer un utilisateur par ID
   * @param {number} userId - ID de l'utilisateur
   * @returns {Promise} Données de l'utilisateur
   */
  getUser(userId) {
    return axiosService.get(`/accounts/users/${userId}/`)
  },

  /**
   * Mettre à jour un utilisateur
   * @param {number} userId - ID de l'utilisateur
   * @param {Object} userData - Données utilisateur {first_name, last_name, email, is_staff, is_superuser}
   * @returns {Promise} Utilisateur mis à jour
   */
  updateUser(userId, userData) {
    // Convertir phone_number en phone_number_write pour l'API
    const payload = { ...userData };
    if (payload.phone_number !== undefined) {
      payload.phone_number_write = payload.phone_number;
      delete payload.phone_number;
    }
    return axiosService.patch(`/accounts/users/${userId}/`, payload)
  },

  /**
   * Créer un nouvel utilisateur
   * @param {Object} userData - Données utilisateur {username, email, password, first_name, last_name, role, is_staff, is_superuser}
   * @returns {Promise} Utilisateur créé
   */
  createUser(userData) {
    return axiosService.post('/accounts/users/', {
      username: userData.username,
      email: userData.email,
      password: userData.password,
      phone_number_write: userData.phone_number,
      first_name: userData.first_name,
      last_name: userData.last_name,
      role: userData.role || 'user', // 'user', 'agent', 'admin'
      is_staff: userData.is_staff,
      is_superuser: userData.is_superuser
    });
  },

  /**
   * Supprimer un utilisateur
   * @param {number} userId - ID de l'utilisateur
   * @returns {Promise} Réponse de l'API
   */
  deleteUser(userId) {
    return axiosService.delete(`/accounts/users/${userId}/`)
  }
}
