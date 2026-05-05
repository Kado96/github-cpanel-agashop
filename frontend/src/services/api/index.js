/**
 * Services API centralisés
 * 
 * Structure organisée selon la structure Django REST Framework du backend
 * 
 * Organisation backend:
 * - /api/login/, /api/register/, /api/refresh/ (authentification)
 * - /api/accounts/users/ (UserViewSet)
 * - /api/accounts/accounts/ (AccountViewSet avec actions custom)
 * - /api/shops/shops/ (ShopViewSet avec actions custom: stats, set_position)
 * - /api/shops/products/ (ProductViewSet avec actions custom: control, supply, stock, change-sale-price)
 * - /api/shops/basic-products/ (BasicProductViewSet)
 * - /api/shops/sales/ (SalesViewSet)
 * - /api/shops/supplies/ (SupplyViewSet)
 * - /api/shops/categories/ (CategoryViewSet)
 * - /api/shops/sub-categories/ (SubCategoryViewSet)
 * - /api/shops/provinces/ (ProvincesViewSet)
 * - /api/shops/control-frequency/ (ControlFrequencyViewSet)
 * - /api/shops/history/ (HistoryViewSet - admin uniquement)
 */

// Authentification (endpoints directs)
export { authService } from './auth'

// Accounts app (/api/accounts/)
export { accountsService } from './accounts'
export { usersService } from './users'

// Shops app (/api/shops/)
export { shopsService } from './shops'
export { productsService } from './products'
export { basicProductsService } from './basicProducts'
export { salesService } from './sales'
export { suppliesService } from './supplies'
export { categoriesService } from './categories'
export { subCategoriesService } from './subCategories'
export { provincesService } from './provinces'
export { controlFrequencyService } from './controlFrequency'
export { historyService } from './history'
export { expensesService } from './expenses'
export { mediaService } from './media'
