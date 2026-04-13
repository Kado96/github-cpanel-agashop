import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des ventes
 * Correspond exactement à l'API backend: /api/shops/sales/
 */
export const salesService = {
  /**
   * Récupérer les ventes d'une boutique
   * @param {number} shopId - ID de la boutique
   * @param {Object} params - Paramètres de filtrage (created_at__gte, created_at__lte)
   * @returns {Promise} Liste des ventes (paginée)
   */
  getSales(shopId, params = {}) {
    return axiosService.get('/shops/sales/', {
      params: {
        shop: shopId,
        ...params
      }
    })
  }
}
