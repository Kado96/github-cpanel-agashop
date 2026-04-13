import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des boutiques
 * Correspond exactement à l'API backend: /api/shops/shops/
 */
export const shopsService = {
  /**
   * Récupérer la liste des boutiques
   * @returns {Promise} Liste des boutiques (paginée)
   */
  getShops(params = {}) {
    return axiosService.get('/shops/shops/', { params })
  },

  /**
   * Récupérer une boutique par ID
   * @param {number} shopId - ID de la boutique
   * @returns {Promise} Données de la boutique
   */
  getShop(shopId) {
    return axiosService.get(`/shops/shops/${shopId}/`)
  },

  /**
   * Créer une nouvelle boutique
   * @param {Object} shopData - Données de la boutique {name, province, commune, quarter, address}
   * @returns {Promise} Boutique créée
   */
  createShop(shopData) {
    return axiosService.post('/shops/shops/', shopData)
  },

  /**
   * Récupérer les statistiques d'une boutique
   * @param {number} shopId - ID de la boutique
   * @param {Object} params - Paramètres de filtrage (created_at__gte, created_at__lte)
   * @returns {Promise} Statistiques de la boutique {sales, b_sales, supply, b_supplies}
   */
  getShopStats(shopId, params = {}) {
    return axiosService.get(`/shops/shops/${shopId}/stats/`, { params })
  },

  /**
   * Définir la position GPS d'une boutique
   * @param {number} shopId - ID de la boutique
   * @param {number} longitude - Longitude
   * @param {number} latitude - Latitude
   * @returns {Promise} Réponse de l'API
   */
  setPosition(shopId, longitude, latitude) {
    return axiosService.post(`/shops/shops/${shopId}/set_position/`, { longitude, latitude })
  },

  /**
   * Mettre à jour une boutique
   * @param {number} shopId - ID de la boutique
   * @param {Object} shopData - Données de la boutique {name, province, commune, quarter, address, is_active}
   * @returns {Promise} Boutique mise à jour
   */
  updateShop(shopId, shopData) {
    return axiosService.patch(`/shops/shops/${shopId}/`, shopData)
  },

  /**
   * Supprimer une boutique
   * @param {number} shopId - ID de la boutique
   * @returns {Promise} Réponse de l'API
   */
  deleteShop(shopId) {
    return axiosService.delete(`/shops/shops/${shopId}/`)
  },

  /**
   * Demander un upgrade Premium
   * @param {number} shopId
   * @param {Object} data - { contact_info }
   */
  requestUpgrade(shopId, data) {
    return axiosService.post(`/shops/shops/${shopId}/request_upgrade/`, data)
  },

}
