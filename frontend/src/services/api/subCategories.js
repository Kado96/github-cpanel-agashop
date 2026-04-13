import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des sous-catégories
 * Correspond exactement à l'API backend: /api/shops/sub-categories/
 * ViewSet: SubCategoryViewSet
 */
export const subCategoriesService = {
  /**
   * Récupérer la liste des sous-catégories
   * @param {Object} params - Paramètres de filtrage (category, updated_at__gte, updated_at__lte, id__gt)
   * @returns {Promise} Liste des sous-catégories (paginée)
   */
  getSubCategories(params = {}) {
    return axiosService.get('/shops/sub-categories/', { params })
  },

  /**
   * Récupérer une sous-catégorie par ID
   * @param {number} subCategoryId - ID de la sous-catégorie
   * @returns {Promise} Données de la sous-catégorie
   */
  getSubCategory(subCategoryId) {
    return axiosService.get(`/shops/sub-categories/${subCategoryId}/`)
  },

  /**
   * Créer une nouvelle sous-catégorie
   * @param {Object} data - { name, category }
   * @returns {Promise} Sous-catégorie créée
   */
  createSubCategory(data) {
    return axiosService.post('/shops/sub-categories/', data)
  }
}
