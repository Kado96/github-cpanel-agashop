import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion de l'historique
 * Correspond exactement à l'API backend: /api/shops/history/
 * ViewSet: HistoryViewSet (Admin uniquement)
 */
export const historyService = {
  /**
   * Récupérer l'historique
   * @param {Object} params - Paramètres de filtrage (shop_name, shop_owner, action, sub_category, product_name, product_id, created_at__gte, created_at__lte, id__gt)
   * @returns {Promise} Liste de l'historique (paginée)
   */
  getHistory(params = {}) {
    return axiosService.get('/shops/history/', { params })
  },

  /**
   * Exporter l'historique (format CSV/Excel)
   * @param {Object} params - Paramètres de filtrage
   * @returns {Promise} Fichier exporté
   */
  exportHistory(params = {}) {
    return axiosService.get('/shops/history/export/', { params, responseType: 'blob' })
  }
}
