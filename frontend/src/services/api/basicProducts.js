import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des produits de base
 * Correspond exactement à l'API backend: /api/shops/basic-products/
 * ViewSet: BasicProductViewSet
 */
export const basicProductsService = {
  /**
   * Récupérer la liste des produits de base
   * @param {Object} params - Paramètres de filtrage (sub_category)
   * @returns {Promise} Liste des produits de base (paginée)
   */
  getBasicProducts(params = {}) {
    return axiosService.get('/shops/basic-products/', { params })
  },

  /**
   * Récupérer un produit de base par ID
   * @param {number} productId - ID du produit de base
   * @returns {Promise} Données du produit de base
   */
  getBasicProduct(productId) {
    return axiosService.get(`/shops/basic-products/${productId}/`)
  },

  /**
   * Créer un nouveau produit de base
   * @param {FormData|Object} productData - Données du produit (peut inclure image en FormData)
   * @returns {Promise} Produit créé
   */
  createBasicProduct(productData) {
    // Si c'est un FormData (avec image), on l'envoie tel quel
    if (productData instanceof FormData) {
      return axiosService.post('/shops/basic-products/', productData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    // Sinon, on envoie en JSON
    return axiosService.post('/shops/basic-products/', productData)
  },

  /**
   * Modifier un produit de base
   * @param {number} productId - ID du produit de base
   * @param {FormData|Object} productData - Données mises à jour
   * @returns {Promise} Produit modifié
   */
  updateBasicProduct(productId, productData) {
    if (productData instanceof FormData) {
      return axiosService.patch(`/shops/basic-products/${productId}/`, productData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }
    return axiosService.patch(`/shops/basic-products/${productId}/`, productData)
  },

  /**
   * Supprimer un produit de base
   * @param {number} productId - ID du produit de base
   * @returns {Promise} Réponse de l'API
   */
  deleteBasicProduct(productId) {
    return axiosService.delete(`/shops/basic-products/${productId}/`)
  }
}
