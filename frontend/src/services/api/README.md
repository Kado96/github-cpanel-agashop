# Services API - Structure Django REST Framework

Cette structure de services correspond **exactement** à l'organisation du backend Django REST Framework.

## 📁 Organisation des Services

### Authentification (`/api/`)
- **authService** (`auth.js`)
  - `login()` → `POST /api/login/` (CustomTokenObtainPairView)
  - `register()` → `POST /api/register/` (RegisterViewSet)
  - `refreshToken()` → `POST /api/refresh/` (TokenRefreshView)
  - `resetPassword()` → `POST /api/accounts/accounts/reset-password/` (AccountViewSet action)

### Accounts App (`/api/accounts/`)
- **usersService** (`users.js`)
  - `updateUser()` → `PATCH /api/accounts/users/{id}/` (UserViewSet)
  
- **accountsService** (`accounts.js`)
  - `verifyOtp()` → `POST /api/accounts/accounts/verify_otp/` (AccountViewSet action)
  - `resendOtp()` → `GET /api/accounts/accounts/resend_otp/` (AccountViewSet action)

### Shops App (`/api/shops/`)
- **shopsService** (`shops.js`) - ShopViewSet
  - `getShops()` → `GET /api/shops/shops/`
  - `getShop(id)` → `GET /api/shops/shops/{id}/`
  - `createShop()` → `POST /api/shops/shops/`
  - `getShopStats(id, params)` → `GET /api/shops/shops/{id}/stats/` (action custom)
  - `setPosition(id, lon, lat)` → `POST /api/shops/shops/{id}/set_position/` (action custom)

- **productsService** (`products.js`) - ProductViewSet
  - `getProducts(shopId)` → `GET /api/shops/products/?shop={shopId}`
  - `createProduct()` → `POST /api/shops/products/`
  - `controlProduct(id, quantity)` → `POST /api/shops/products/{id}/control/` (action custom)
  - `supplyProduct(id, data)` → `POST /api/shops/products/{id}/supply/` (action custom)
  - `getProductStock(id)` → `GET /api/shops/products/{id}/stock/` (action custom)
  - `changeSalePrice(id, price, buyPrice)` → `POST /api/shops/products/{id}/change-sale-price/` (action custom)

- **basicProductsService** (`basicProducts.js`) - BasicProductViewSet
  - `getBasicProducts(params)` → `GET /api/shops/basic-products/`
  - `getBasicProduct(id)` → `GET /api/shops/basic-products/{id}/`

- **salesService** (`sales.js`) - SalesViewSet
  - `getSales(shopId, params)` → `GET /api/shops/sales/?shop={shopId}`

- **suppliesService** (`supplies.js`) - SupplyViewSet
  - `getSupplies(shopId, params)` → `GET /api/shops/supplies/?shop={shopId}`

- **categoriesService** (`categories.js`) - CategoryViewSet
  - `getCategories(params)` → `GET /api/shops/categories/`
  - `getCategory(id)` → `GET /api/shops/categories/{id}/`

- **subCategoriesService** (`subCategories.js`) - SubCategoryViewSet
  - `getSubCategories(params)` → `GET /api/shops/sub-categories/`
  - `getSubCategory(id)` → `GET /api/shops/sub-categories/{id}/`

- **provincesService** (`provinces.js`) - ProvincesViewSet
  - `getProvinces()` → `GET /api/shops/provinces/`

- **controlFrequencyService** (`controlFrequency.js`) - ControlFrequencyViewSet
  - `getControlFrequency(shopId)` → `GET /api/shops/control-frequency/?shop={shopId}`
  - `createControlFrequency()` → `POST /api/shops/control-frequency/`
  - `updateControlFrequency(id, data)` → `PUT /api/shops/control-frequency/{id}/`

- **historyService** (`history.js`) - HistoryViewSet (Admin uniquement)
  - `getHistory(params)` → `GET /api/shops/history/`
  - `exportHistory(params)` → `GET /api/shops/history/export/`

## 🔗 Correspondance Backend

| Service Frontend | ViewSet Backend | Endpoint Base |
|-----------------|-----------------|---------------|
| authService | CustomTokenObtainPairView, RegisterViewSet | `/api/login/`, `/api/register/`, `/api/refresh/` |
| usersService | UserViewSet | `/api/accounts/users/` |
| accountsService | AccountViewSet | `/api/accounts/accounts/` |
| shopsService | ShopViewSet | `/api/shops/shops/` |
| productsService | ProductViewSet | `/api/shops/products/` |
| basicProductsService | BasicProductViewSet | `/api/shops/basic-products/` |
| salesService | SalesViewSet | `/api/shops/sales/` |
| suppliesService | SupplyViewSet | `/api/shops/supplies/` |
| categoriesService | CategoryViewSet | `/api/shops/categories/` |
| subCategoriesService | SubCategoryViewSet | `/api/shops/sub-categories/` |
| provincesService | ProvincesViewSet | `/api/shops/provinces/` |
| controlFrequencyService | ControlFrequencyViewSet | `/api/shops/control-frequency/` |
| historyService | HistoryViewSet | `/api/shops/history/` |

## 📝 Notes

- Tous les endpoints utilisent le `baseURL` configuré dans `plugins/axios.js` (`http://localhost:8000/api` en local)
- Les actions custom des ViewSets sont documentées dans chaque service
- La pagination est gérée automatiquement par Django REST Framework
- Les filtres correspondent aux `filterset_fields` définis dans les ViewSets
