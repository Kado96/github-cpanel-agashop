<!--
  * @file ActiveArticlesList.vue
  * @description Page pour la gestion de Active Articles List.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-active-articles" name="back-to-active-articles" @click="$router.push({ name: 'active-articles' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Inventaire Complet</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchProducts">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>

      <ion-toolbar color="secondary">
        <ion-searchbar 
          id="active-articles-search"
          name="active-articles-search"
          v-model="keyword" 
          placeholder="Rechercher un article..." 
          color="light"
          class="custom-searchbar"
        ></ion-searchbar>
      </ion-toolbar>
    </ion-header>

    <ion-content class="history-content">
      <!-- 1. Category Filter Area -->
      <div class="selection-area">
        <div class="filter-row">
          <ion-item lines="none" class="filter-item">
            <ion-select
              id="active-articles-category"
              name="active-articles-category"
              v-model="filterCategoryId"
              placeholder="Toutes les catégories"
              interface="popover"
              class="custom-select"
              @ionDismiss="removeFocus"
            >
              <ion-select-option :value="null">Toutes les catégories</ion-select-option>
              <ion-select-option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </ion-select-option>
            </ion-select>
          </ion-item>
        </div>

        <!-- Date range selectors for harmonization -->
        <div class="range-selector-container">
          <div class="date-picker-item">
            <span class="picker-label">Du :</span>
            <ion-datetime-button datetime="active-start-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="active-start-date" presentation="date" v-model="startDate" @ionChange="fetchProducts" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
          <div class="date-picker-item">
            <span class="picker-label">Au :</span>
            <ion-datetime-button datetime="active-end-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="active-end-date" presentation="date" v-model="endDate" @ionChange="fetchProducts" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
        </div>
      </div>

      <!-- 2. Inventory Summary Bar -->
      <div class="revenue-summary">
        Articles en boutique : <span class="amount blue-text">{{ totalCount }}</span> 
        <br/>
        Valeur totale : <span class="amount blue-text">{{ money(serverTotals.market_value) }} BIF</span>
      </div>

      <!-- 3. Table Header -->
      <div class="table-header">
        <div class="col article-col italic">Article / Catégorie</div>
        <div class="col total-col italic text-right">Stock / V : A</div>
      </div>

      <!-- 4. Products List -->
      <div class="sales-list-container">
        <div v-for="p in filteredProducts" :key="p.id" class="sale-row">
          <div class="col article-col">
            <ion-thumbnail slot="start" class="small-thumb">
              <ion-img :src="productImage(p)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
            </ion-thumbnail>
            <div class="art-info">
              <div class="art-name">{{ p.product?.name }}</div>
              <div class="art-cat">{{ getCategoryLabel(p) }}</div>
            </div>
          </div>
          <div class="col total-col">
            <div class="stock-info">
              <div class="stock-qty" :class="p.quantity <= 0 ? 'red-text' : ''">
                {{ p.quantity }}
              </div>
              <div class="stock-val">V : {{ money(p.quantity * p.sale_price) }}</div>
              <div class="stock-val orange-text">A : {{ money(p.quantity * (p.product?.buy_price || 0)) }}</div>
            </div>
          </div>
        </div>

        <div v-if="filteredProducts.length === 0 && !loading" class="empty-state">
           Aucun article trouvé.
        </div>
      </div>
      <ion-infinite-scroll @ionInfinite="loadMore" :disabled="!hasNextPage">
        <ion-infinite-scroll-content loading-spinner="bubbles" loading-text="Chargement des articles..."></ion-infinite-scroll-content>
      </ion-infinite-scroll>

      <ion-progress-bar v-if="loading" type="indeterminate"></ion-progress-bar>
    </ion-content>
  </ion-page>
</template>

<script>
import {
  IonProgressBar,
  IonSearchbar,
  IonSelect,
  IonSelectOption,
  IonItem,
  IonThumbnail,
  IonInput,
  IonDatetimeButton,
  IonModal,
  IonDatetime,
  IonFab,
  IonFabButton,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  IonImg,
  toastController
} from '@ionic/vue';
import { 
  arrowBackOutline, 
  refreshCircleOutline, 
  addOutline,
  downloadOutline 
} from 'ionicons/icons';
import * as XLSX from 'xlsx';
import { saveWorkbook } from '../../utils/exportExcel';
import { productsService } from '../../services/api/products';
import { categoriesService } from '../../services/api/categories';
import globalMixins from '../../composables/mixins';

/**
 * Composant ActiveArticlesList
 * - Gère l'interface et la logique métier de Active Articles List.
 */
export default {
  mixins: [globalMixins],
  name: 'ActiveArticlesList',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonButtons,
    IonButton,
    IonTitle,
    IonContent,
    IonIcon,
    IonProgressBar,
    IonSearchbar,
    IonSelect,
    IonSelectOption,
    IonItem,
    IonThumbnail,
    IonInput,
    IonDatetimeButton,
    IonModal,
    IonDatetime,
    IonFab,
    IonFabButton,
    IonInfiniteScroll,
    IonInfiniteScrollContent,
    IonImg
  },
  data() {
    return {
      arrowBackOutline,
      refreshCircleOutline,
      addOutline,
      downloadOutline,
      products: [],
      categories: [],
      filterCategoryId: null,
      keyword: '',
      startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
      loading: false,
      shop: this.$store.state.shop,
      currentPage: 1,
      hasNextPage: true,
      totalCount: 0,
      serverTotals: { market_value: 0, cost_value: 0, quantity: 0 },
      searchTimeout: null
    };
  },
  computed: {
    shopId() {
      return this.$store.state.shop?.id || this.shop?.id;
    },
    totalValue() {
      // Obsolète, on utilise serverTotals
      return this.serverTotals.market_value;
    },
    filteredProducts() {
      // Le filtrage se fait désormais majoritairement côté backend
      // On retourne directement la liste pour éviter les tris lourds
      return this.products;
    },
    isReadOnly() {
      return this.$route.query.readonly === '1';
    }
  },
  ionViewDidEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Inventaire et Valeur du Stock',
      description: 'Cet écran vous permet de piloter l\'ensemble de votre marchandise. L\'indicateur principal vous montre combien de capital est actuellement immobilisé dans vos rayons et combien vous gagnerez après la vente.',
      elements: [
        { label: 'Valeur d\'Achat', type: 'Capital', desc: 'Le montant total déboursé pour acquérir le stock actuel. C\'est votre investissement de base.' },
        { label: 'Valeur de Vente', type: 'Potentiel', desc: 'Le chiffre d\'affaires total que vous réaliserez une fois tout le stock vendu aux prix actuels.' },
        { label: 'Unité(s)', type: 'Quantité', desc: 'Nous affichons le nombre précis d\'unités restantes pour chaque produit afin d\'éviter les erreurs de comptage.' },
        { label: 'Filtrer', type: 'Outils', desc: 'Utilisez la loupe pour chercher un nom ou le sélecteur pour filtrer par famille de produits (Catégorie).' }
      ],
      faq: [
        { question: 'Comment changer un prix de vente ?', answer: 'Appuyez sur n\'importe quel article dans la liste. Une fiche s\'ouvrira où vous pourrez modifier le prix, le nom ou la catégorie.' },
        { question: 'Pourquoi la valeur d\'achat est-elle importante ?', answer: 'Elle vous permet de savoir si vos fonds sont trop bloqués dans des produits qui ne se vendent pas vite.' }
      ]
    });
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.initLoading();
    this.fetchCategories();
  },
  watch: {
    keyword() {
      if (this.searchTimeout) clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.initLoading();
      }, 500);
    },
    filterCategoryId() {
      this.initLoading();
    }
  },
  methods: {
    removeFocus() {
      // Un petit délai permet à Ionic de finir ses transitions d'overlay
      setTimeout(() => {
        const activeElement = document.activeElement;
        if (activeElement && activeElement instanceof HTMLElement) {
          activeElement.blur();
        }
        // On force le focus sur le container principal pour "libérer" les éléments cachés
        const content = document.querySelector('ion-content');
        if (content) content.focus();
      }, 100);
    },
    initLoading() {
      this.products = [];
      this.currentPage = 1;
      this.hasNextPage = true;
      this.fetchProducts();
    },
    async fetchProducts(page = 1) {
      if (!this.shopId) return;
      this.loading = true;
      try {
        const params = {
          page,
          page_size: 20
        };

        if (this.keyword) {
          params['product__name__icontains'] = this.keyword;
        }
        
        // Note: Filtrage par catégorie dépend du support backend product__sub_category__category__id
        if (this.filterCategoryId) {
          // Si le backend supporte pas, on filtrera peut-être différemment ou on laisse ainsi
          // On tente l'approche standard
          params['product__sub_category__category'] = this.filterCategoryId;
        }

        const res = await productsService.getProducts(this.shopId, params);
        const data = res.data;
        const results = data.results || data || [];
        const paginated = !!data.results;

        if (page === 1) {
          this.products = results;
        } else {
          // Éviter doublons
          const existingIds = new Set(this.products.map(p => p.id));
          const newEntries = results.filter(p => !existingIds.has(p.id));
          this.products = [...this.products, ...newEntries];
        }

        this.hasNextPage = paginated && !!data.next;
        this.currentPage = page;
        this.totalCount = data.count || this.products.length;
        this.serverTotals = data.totals || { market_value: 0, cost_value: 0, quantity: 0 };
      } catch (err) {
        console.error("[ActiveArticlesList] Erreur:", err);
        this.hasNextPage = false;
      } finally {
        this.loading = false;
      }
    },
    async loadMore(ev) {
      if (this.hasNextPage) {
        await this.fetchProducts(this.currentPage + 1);
      }
      ev.target.complete();
    },
    async exportToExcel() {
       if (this.products.length === 0) {
         this.showToastMsg('Aucune donnée à exporter', 'warning');
         return;
       }

       const data = this.products.map(p => ({
         'Article': p.product?.name,
         'Catégorie': this.getCategoryLabel(p),
         'Quantité': p.quantity,
         'Prix de Vente (BIF)': parseFloat(p.sale_price),
         'Valeur Stock (BIF)': p.quantity * p.sale_price,
         'Prix d\'Achat Unitaire (BIF)': p.product?.buy_price || 0
       }));

       const ws = XLSX.utils.json_to_sheet(data);
       const wb = XLSX.utils.book_new();
       XLSX.utils.book_append_sheet(wb, ws, "Inventaire");
       
       const fileName = `Inventaire_${this.startDate}_au_${this.endDate}.xlsx`;
       await saveWorkbook(wb, fileName);
       this.showToastMsg('Export Excel réussi !', 'success');
    },

    async fetchCategories() {
      try {
        const res = await categoriesService.getCategories();
        this.categories = res.data.results || res.data || [];
      } catch (err) {
        console.error("[ActiveArticlesList] Erreur catégories:", err);
      }
    },
    money(val) {
      if (!val) return "0";
      return parseFloat(val).toLocaleString('fr-FR');
    },
    getShopFromLocalStorage() {
      try {
        const s = localStorage.getItem('current_shop');
        return s ? JSON.parse(s) : null;
      } catch (e) {
        return null;
      }
    }
  }
};
</script>

<style scoped>
.history-content {
  --background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
  background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
}

.selection-area {
  padding: 16px 12px;
  animation: fadeInUp 0.5s ease-out;
}

.filter-item {
  --background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 12px;
}

.range-selector-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 12px;
  background: white;
  border-radius: 16px;
  border: 1.5px solid #e2e8f0;
}

.date-picker-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.picker-label {
  font-weight: 700;
  color: #64748b;
  font-size: 0.9rem;
}

.custom-date-input {
  border: 1.5px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 12px;
  font-family: inherit;
  font-size: 1rem;
  color: #0f172a;
  background: #f8fafc;
  outline: none;
}

.custom-date-input:focus {
  border-color: var(--ion-color-secondary);
}

.custom-select {
  width: 100%;
  font-weight: 700;
  color: #0f172a;
  font-size: 0.95rem;
}

.revenue-summary {
  text-align: center;
  color: #0f172a;
  font-weight: 800;
  font-size: 1.15rem;
  margin: 16px 12px;
  background: white;
  padding: 16px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.blue-text { color: var(--ion-color-secondary); font-weight: 800; }
.red-text { color: #ef4444; }

.table-header {
  display: flex;
  background: #0f172a;
  padding: 12px 16px;
  color: #ffffff;
  font-weight: 800;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  border-radius: 12px 12px 0 0;
  margin: 0 12px;
}

.col { display: flex; align-items: center; }
.article-col { flex: 2; }
.total-col { flex: 1.2; justify-content: flex-end; }

.sales-list-container {
  padding: 0 12px 60px 12px;
}

.sale-row {
  display: flex;
  padding: 18px 16px;
  background: white;
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  margin: 0 12px 12px 12px;
  align-items: center;
  color: #1e293b;
  font-size: 0.95rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  animation: fadeInUp 0.4s ease-out both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.small-thumb {
  width: 44px;
  height: 54px;
  margin-right: 14px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #f1f5f9;
}

.art-info {
  display: flex;
  flex-direction: column;
}

.art-name {
  font-weight: 800;
  color: #0f172a;
  font-size: 1rem;
}

.art-cat {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
  margin-top: 2px;
}

.stock-info {
  text-align: right;
}

.stock-qty {
  font-weight: 800;
  color: var(--ion-color-secondary);
  font-size: 1.1rem;
}

.stock-val {
  font-size: 0.8rem;
  color: #475569;
  font-weight: 700;
  margin-top: 2px;
}

.orange-text {
  color: #f59e0b;
}

.text-right {
  text-align: right;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  font-weight: 600;
}

.custom-searchbar {
  --background: rgba(255, 255, 255, 0.15);
  --color: #fff;
  --placeholder-color: rgba(255, 255, 255, 0.7);
  --icon-color: #fff;
  --border-radius: 12px;
  padding: 8px 16px 16px 16px;
}

.art-info {
  display: flex;
  flex-direction: column;
}

.art-name {
  font-weight: 800;
  color: #0f172a;
  font-size: 1rem;
}

.art-cat {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
  margin-top: 2px;
}

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
</style>
