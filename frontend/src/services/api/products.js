import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des produits
 * Correspond exactement à l'API backend: /api/shops/products/
 */
export const productsService = {
  /**
   * Récupérer les produits d'une boutique
   * @param {number} shopId - ID de la boutique
   * @returns {Promise} Liste des produits
   */
  getProducts(shopId, params = {}) {
    return axiosService.get('/shops/products/', { params: { shop: shopId, ...params } })
  },

  /**
   * Créer un nouveau produit
   * @param {Object} productData - Données du produit {shop, product, quantity, sale_price, buy_price}
   * @returns {Promise} Produit créé
   */
  createProduct(productData) {
    return axiosService.post('/shops/products/', productData)
  },

  /**
   * Supprimer un produit d'une boutique
   * @param {number} productId - ID du produit
   * @returns {Promise} Réponse de l'API
   */
  deleteProduct(productId) {
    return axiosService.delete(`/shops/products/${productId}/`)
  },

  /**
   * Contrôler un produit (vente)
   * @param {number} productId - ID du produit
   * @param {number} quantity - Quantité restante après contrôle
   * @returns {Promise} Réponse de l'API
   */
  controlProduct(productId, quantity) {
    return axiosService.post(`/shops/products/${productId}/control/`, { quantity })
  },

  /**
   * Approvisionner un produit
   * @param {number} productId - ID du produit
   * @param {Object} supplyData - Données d'approvisionnement {quantity, total_buy_price}
   * @returns {Promise} Réponse de l'API
   */
  supplyProduct(productId, supplyData) {
    return axiosService.post(`/shops/products/${productId}/supply/`, supplyData)
  },

  /**
   * Récupérer le stock d'un produit (historique des approvisionnements)
   * @param {number} productId - ID du produit
   * @returns {Promise} Liste des approvisionnements
   */
  getProductStock(productId) {
    return axiosService.get(`/shops/products/${productId}/stock/`)
  },

  /**
   * Changer le prix de vente et d'achat d'un produit
   * @param {number} productId - ID du produit
   * @param {number} newPrice - Nouveau prix de vente
   * @param {number} newBuyPrice - Nouveau prix d'achat
   * @returns {Promise} Réponse de l'API
   */
  changeSalePrice(productId, newPrice, newBuyPrice) {
    return axiosService.post(`/shops/products/${productId}/change-sale-price/`, {
      new_price: newPrice,
      new_buy_price: newBuyPrice
    })
  },

  /**
   * Annuler le dernier contrôle d'un produit
   * @param {number} productId - ID du produit
   * @returns {Promise} Réponse de l'API
   */
  cancelControl(productId) {
    return axiosService.post(`/shops/products/${productId}/cancel-control/`)
  },

}
