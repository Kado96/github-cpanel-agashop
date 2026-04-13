import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des catégories
 * Correspond exactement à l'API backend: /api/shops/categories/
 * ViewSet: CategoryViewSet
 */
export const categoriesService = {
  /**
   * Récupérer la liste des catégories
   * @param {Object} params - Paramètres de filtrage (name__contains, id__gt)
   * @returns {Promise} Liste des catégories (paginée)
   */
  getCategories(params = {}) {
    return axiosService.get('/shops/categories/', { params })
  },

  /**
   * Récupérer une catégorie par ID
   * @param {number} categoryId - ID de la catégorie
   * @returns {Promise} Données de la catégorie
   */
  getCategory(categoryId) {
    return axiosService.get(`/shops/categories/${categoryId}/`)
  },

  /**
   * Créer une nouvelle catégorie
   * @param {Object} data - { name }
   * @returns {Promise} Catégorie créée
   */
  createCategory(data) {
    return axiosService.post('/shops/categories/', data)
  }
}
