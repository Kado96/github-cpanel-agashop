import { axiosService } from '../../plugins/axios'

/**
 * Service de gestion des provinces
 * Correspond exactement à l'API backend: /api/shops/provinces/
 * ViewSet: ProvincesViewSet
 */
export const provincesService = {
  /**
   * Récupérer la liste des provinces avec leurs communes
   * @returns {Promise} Liste des provinces avec communes
   */
  getProvinces() {
    return axiosService.get('/shops/provinces/')
  }
}
