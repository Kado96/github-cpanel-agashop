import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des approvisionnements
 * Correspond exactement à l'API backend: /api/shops/supplies/
 */
export const suppliesService = {
  /**
   * Récupérer les approvisionnements d'une boutique
   * @param {number} shopId - ID de la boutique
   * @param {Object} params - Paramètres de filtrage (created_at__gte, created_at__lte)
   * @returns {Promise} Liste des approvisionnements (paginée)
   */
  getSupplies(shopId, params = {}) {
    return axiosService.get('/shops/supplies/', {
      params: {
        shop: shopId,
        ...params
      }
    })
  },

  /**
   * Mettre à jour un approvisionnement (quantité, prix d'achat total)
   * @param {number} supplyId - ID de l'approvisionnement
   * @param {Object} data - { quantity, total_buy_price }
   * @returns {Promise} Approvisionnement mis à jour (updated_at géré par le backend)
   */
  updateSupply(supplyId, data) {
    return axiosService.patch(`/shops/supplies/${supplyId}/`, data)
  },

  /**
   * Supprimer un approvisionnement
   * @param {number} supplyId - ID de l'approvisionnement
   * @returns {Promise}
   */
  deleteSupply(supplyId) {
    return axiosService.delete(`/shops/supplies/${supplyId}/`)
  }
}
