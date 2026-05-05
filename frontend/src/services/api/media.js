import axios from 'axios'

/**
 * Service pour la gestion de la bibliothèque de médias (ProductMedia)
 */
export const mediaService = {
  /**
   * Récupère la liste des médias avec pagination et recherche optionnelle
   */
  getMedia(params = {}) {
    return axios.get('/shops/media/', { params })
  },

  /**
   * Récupère un média spécifique par son ID
   */
  getMediaById(id) {
    return axios.get(`/shops/media/${id}/`)
  },

  /**
   * Ajoute une nouvelle image à la bibliothèque
   * @param {FormData} formData - Doit contenir 'file' et optionnellement 'name'
   */
  uploadMedia(formData) {
    return axios.post('/shops/media/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  /**
   * Supprime un média de la bibliothèque
   */
  deleteMedia(id) {
    return axios.delete(`/shops/media/${id}/`)
  }
}
