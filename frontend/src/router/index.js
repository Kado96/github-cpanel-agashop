import { createRouter, createWebHistory } from '@ionic/vue-router';
import HomePage from '../views/HomePage.vue'
import LoginPage from '../views/auth/LoginPage.vue';
import AuthLayout from '../views/auth/AuthLayout.vue';
import RegisterPage from '../views/auth/RegisterPage.vue';
import OTPPage from '../views/auth/OTPPage.vue';
import ForgotPasswordPage from '../views/auth/ForgotPasswordPage.vue';
import ForgotPasswordSuccessPage from '../views/auth/ForgotPasswordSuccessPage.vue';
import store from '../store'

const routes = [
  { path: '/login', name: "login", component: LoginPage, meta: { requiresAuth: false } },
  { path: '/register', name: "register", component: RegisterPage, meta: { requiresAuth: false } },
  { path: '/otp', name: "otp-verification", component: OTPPage, meta: { requiresAuth: false } },
  { path: '/forgot-password', name: "forgot-password", component: ForgotPasswordPage, meta: { requiresAuth: false } },
  { path: '/forgot-password/success', name: "forgot-password-success", component: ForgotPasswordSuccessPage, meta: { requiresAuth: false } },
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/shop',
    name: 'shop',
    component: () => import('../views/ShopHome.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('../views/shop/ShopProducts.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stats',
    name: 'stats',
    component: () => import('../views/shop/ShopStats.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stats/free',
    name: 'free-stats',
    component: () => import('../views/shop/FreeStats.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/controls',
    name: 'controls',
    component: () => import('../views/shop/ControlProducts.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sales',
    name: 'sales',
    component: () => import('../views/shop/SalesDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sales-list',
    name: 'sales-list',
    component: () => import('../views/shop/SalesList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/active-articles',
    name: 'active-articles',
    component: () => import('../views/shop/ActiveArticlesDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/active-articles-list',
    name: 'active-articles-list',
    component: () => import('../views/shop/ActiveArticlesList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/critical-articles',
    name: 'critical-articles',
    component: () => import('../views/shop/CriticalArticlesDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/critical-articles-list',
    name: 'critical-articles-list',
    component: () => import('../views/shop/CriticalArticlesList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stock-volume',
    name: 'stock-volume',
    component: () => import('../views/shop/StockVolumeDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stock-volume-list',
    name: 'stock-volume-list',
    component: () => import('../views/shop/StockVolumeList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profits',
    name: 'profits',
    component: () => import('../views/shop/ProfitsDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profits-list',
    name: 'profits-list',
    component: () => import('../views/shop/ProfitsList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/supplies',
    name: 'supplies',
    component: () => import('../views/shop/SupplyProducts.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/payment-methods',
    name: 'payment-methods',
    component: () => import('../views/shop/PaymentMethods.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/supplies/actions',
    name: 'supply-product-actions',
    component: () => import('../views/shop/SupplyProductActions.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin-home',
    component: () => import('../views/admin/AdminHome.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/expenses',
    name: 'expenses',
    component: () => import('../views/shop/ExpensesDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/expenses-list',
    name: 'expenses-list',
    component: () => import('../views/shop/ExpensesList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/agent',
    name: 'agent-home',
    component: () => import('../views/admin/AgentHome.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/basic-products',
    name: 'manage-basic-products',
    component: () => import('../views/admin/ManageBasicProducts.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('../views/admin/AdminUsers.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, requiresAdminOnly: true }  // Réservé aux admins : les agents n'ont pas accès
  },
  {
    path: '/admin/shops',
    name: 'admin-shops',
    component: () => import('../views/admin/AdminShops.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/settings',
    name: 'admin-settings',
    component: () => import('../views/admin/AdminSettings.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

function retrieveUserFromLS() {
  var user = JSON.parse(localStorage.getItem('user'));
  if (user) {
    store.state.user = user;
  }
}

router.beforeEach((to) => {
  retrieveUserFromLS()
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.state.user?.access) {
      return { name: 'login' }
    }

    // Vérifier les permissions admin pour les routes qui le nécessitent
    if (to.matched.some(record => record.meta.requiresAdmin)) {
      const user = store.state.user;
      const groups = user?.groups || [];

      // Normaliser les groupes : extraire les noms si ce sont des objets
      let groupNames = [];
      if (Array.isArray(groups) && groups.length > 0) {
        if (typeof groups[0] === 'string') {
          groupNames = groups;
        } else if (typeof groups[0] === 'object' && groups[0] !== null) {
          // Si ce sont des objets, extraire les noms
          groupNames = groups.map(g => g.name || g).filter(Boolean);
        }
      }

      console.log(`[Router Guard] Route: ${to.path}, User: ${user?.username}, Groups:`, groups, 'GroupNames:', groupNames);

      const isAdminOrAgent = groupNames.length > 0 &&
        (groupNames.includes('admin') || groupNames.includes('agent') || groupNames.includes('superuser'));

      if (!isAdminOrAgent) {
        console.log(`[Router Guard] Accès refusé - redirection vers /home`);
        return { name: 'home' }
      }

      // Routes réservées aux admins uniquement (pas aux agents) : ex. Gestion Utilisateurs
      if (to.matched.some(record => record.meta.requiresAdminOnly)) {
        const isAdminOnly = groupNames.includes('admin') || groupNames.includes('superuser');
        if (!isAdminOnly) {
          // Agent : rediriger vers la page agent (accès refusé à la création/gestion utilisateurs)
          console.log(`[Router Guard] Agent tentant d'accéder à une route admin-only - redirection vers /agent`);
          return { name: 'agent-home' }
        }
      }

      console.log(`[Router Guard] Accès autorisé pour ${to.path}`);
    }
  }
  else {
    if (store.state.user?.access) {
      return { name: 'home' }
    }
  }

})

import { HELP_DB } from '@/services/help_db';

// Évite certains warnings Chrome/Ionic liés à aria-hidden + focus lors des transitions
router.afterEach((to) => {
  try {
    const el = typeof document !== 'undefined' ? document.activeElement : null;
    if (el && typeof el.blur === 'function') el.blur();
  } catch {
    // no-op
  }

  // Mise à jour automatique du contexte d'aide
  // On cherche une correspondance exacte ou on prend par défaut
  const helpData = HELP_DB[to.name] || HELP_DB['default'];
  if (helpData) {
    store.commit('SET_HELP_CONTEXT', helpData);
  }
});


export default router
