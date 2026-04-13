import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion de la fréquence de contrôle
 * Correspond exactement à l'API backend: /api/shops/control-frequency/
 */
export const controlFrequencyService = {
  /**
   * Récupérer la fréquence de contrôle d'une boutique
   * @param {number} shopId - ID de la boutique
   * @returns {Promise} Fréquence de contrôle
   */
  getControlFrequency(shopId) {
    return axiosService.get('/shops/control-frequency/', { params: { shop: shopId } })
  },

  /**
   * Créer une fréquence de contrôle
   * @param {Object} frequencyData - Données de fréquence {shop, days, hours}
   * @returns {Promise} Fréquence créée
   */
  createControlFrequency(frequencyData) {
    return axiosService.post('/shops/control-frequency/', frequencyData)
  },

  /**
   * Mettre à jour une fréquence de contrôle
   * @param {number} frequencyId - ID de la fréquence
   * @param {Object} frequencyData - Données de fréquence {days, hours}
   * @returns {Promise} Fréquence mise à jour
   */
  updateControlFrequency(frequencyId, frequencyData) {
    return axiosService.put(`/shops/control-frequency/${frequencyId}/`, frequencyData)
  }
}
