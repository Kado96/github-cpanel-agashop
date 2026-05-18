<!--
  * @file SupplyProductPicker.vue
  * @description Page pour la gestion de Supply Product Picker.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="supply-picker-back-btn" name="back-button" class="back-arrow-white" @click="dismiss" fill="clear">
            <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
          <ion-title color="light">
            <div class="header-title-container">
              <span class="main-title">Choisir un produit</span>
              <div class="shop-count-wrapper">
                <span class="count-label">BOUTIQUE:</span>
                <ion-badge color="light" class="shop-count-badge">
                  {{ shopProductsCount || 0 }}
                </ion-badge>
              </div>
            </div>
          </ion-title>
        <ion-buttons slot="end">
          <ion-button id="supply-picker-export-btn" @click="exportToExcel" color="light">
            <ion-icon :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button id="supply-picker-close-btn" name="close-button" color="light" @click="dismiss">
            <ion-icon :icon="closeOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar color="primary">
        <ion-searchbar 
          id="product-picker-search"
          v-model="searchKeyword" 
          placeholder="Rechercher un produit..." 
          show-clear-button="always"
          color="light"
          class="custom-searchbar"
        ></ion-searchbar>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <div class="filter-row ion-margin-horizontal">
        <ion-item lines="none" class="filter-item">
          <ion-select
            id="picker-filter-category"
            name="filter_category"
            :interface-options="{ header: 'Catégorie' }"
            v-model="filterCategoryId"
            placeholder="Catégorie"
            interface="alert"
            @ionChange="onFilterCategoryChange"
          >
            <ion-select-option :value="null">Toutes les catégories</ion-select-option>
            <ion-select-option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </ion-select-option>
          </ion-select>
        </ion-item>
        <ion-item lines="none" class="filter-item">
          <ion-select
            id="picker-filter-sub-category"
            name="filter_sub_category"
            :interface-options="{ header: 'Sous-catégorie' }"
            v-model="filterSubCategoryId"
            placeholder="Sous-catégorie"
            interface="alert"
            :disabled="!filterCategoryId"
          >
            <ion-select-option :value="null">Toutes les sous-catégories</ion-select-option>
            <ion-select-option v-for="sub in filterSubCategories" :key="sub.id" :value="sub.id">
              {{ sub.name }}
            </ion-select-option>
          </ion-select>
        </ion-item>
      </div>

      <ion-list>
        <ion-item-sliding v-for="product in filteredProducts" :key="product.id">

          <ion-item
            button
            @click="select(product)"
            class="product-item"
          >
            <ion-thumbnail slot="start" class="picker-thumb">
              <ion-img :src="productImage(product)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
            </ion-thumbnail>
            <ion-label>
              <h2>{{ product.name || product.product?.name }}</h2>
              <p v-if="product.quantity != null" class="stock-label">Stock : <span>{{ product.quantity }}</span></p>
            </ion-label>
            <ion-icon slot="end" :icon="chevronForwardOutline" class="chevron-icon"></ion-icon>
          </ion-item>

          <ion-item-options side="end">
            <ion-item-option color="secondary" @click.stop="manageShopProduct(product)">
              <div class="option-content">
                <ion-icon :icon="createOutline"></ion-icon>
                <span>Prix/Stock</span>
              </div>
            </ion-item-option>
            <ion-item-option color="danger" @click.stop="confirmRemoveFromShop(product)">
              <div class="option-content">
                <ion-icon :icon="trashOutline"></ion-icon>
                <span>Retirer</span>
              </div>
            </ion-item-option>
          </ion-item-options>
        </ion-item-sliding>
      </ion-list>

      <ion-infinite-scroll @ionInfinite="loadMore" :disabled="!hasNextPage" id="picker-infinite-scroll">
        <ion-infinite-scroll-content loading-spinner="bubbles" loading-text="Chargement des produits..."></ion-infinite-scroll-content>
      </ion-infinite-scroll>

      <ion-item v-if="filteredProducts.length === 0 && !isLoading" lines="none">
        <ion-label class="ion-text-center">
          <p v-if="products.length === 0">Aucun produit dans votre boutique.</p>
          <p v-else>Aucun produit ne correspond à la recherche.</p>
        </ion-label>
      </ion-item>
    </ion-content>
  </ion-page>
</template>

<script>
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonIcon,
  IonContent,
  IonList,
  IonItem,
  IonItemSliding,
  IonItemOptions,
  IonItemOption,
  IonLabel,
  IonThumbnail,
  IonImg,
  IonSearchbar,
  IonSelect,
  IonSelectOption,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  IonBadge,
  modalController,
  alertController,
  actionSheetController
} from '@ionic/vue';
import { 
  closeOutline, 
  chevronForwardOutline, 
  arrowBackOutline, 
  createOutline, 
  trashOutline,
  downloadOutline,
  listOutline
} from 'ionicons/icons';
import * as XLSX from 'xlsx';
import { saveWorkbook } from '../../utils/exportExcel';
import { axiosService } from '../../plugins/axios';
import { categoriesService, subCategoriesService, basicProductsService, productsService } from '../../services/api';
import globalMixins from '../../composables/mixins';
import { defineAsyncComponent } from 'vue';

const BasicProductForm = defineAsyncComponent(() => import('../admin/BasicProductForm.vue'));
const ChangeProductPrice = defineAsyncComponent(() => import('./ChangeProductPrice.vue'));

/**
 * Composant SupplyProductPicker
 * - Gère l'interface et la logique métier de Supply Product Picker.
 */
export default {
  name: 'SupplyProductPicker',
  mixins: [globalMixins],
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonIcon,
    IonContent,
    IonList,
    IonItem,
    IonItemSliding,
    IonItemOptions,
    IonItemOption,
    IonLabel,
    IonThumbnail,
    IonImg,
    IonSearchbar,
    IonSelect,
    IonSelectOption,
    IonInfiniteScroll,
    IonInfiniteScrollContent,
    IonBadge
  },
  props: {
    products: {
      type: Array,
      default: () => []
    },
    shopIdProp: {
      type: [Number, String],
      default: null
    }
  },
  setup() {
    return {
      downloadOutline,
      closeOutline,
      chevronForwardOutline,
      arrowBackOutline,
      createOutline,
      trashOutline,
      listOutline
    };
  },
  data() {
    return { 
      searchKeyword: '',
      categories: [],
      filterSubCategories: [],
      filterCategoryId: null,
      filterSubCategoryId: null,
      localProducts: [...this.products],
      currentPage: 1,
      hasNextPage: true,
      isLoading: false,
      totalCountFromBackend: 0
    };
  },
  watch: {
    products: {
      deep: true,
      handler(newVal) {
        if (!this.searchKeyword && !this.filterCategoryId) {
          this.localProducts = [...newVal];
        }
      }
    },
    searchKeyword() {
      if (this.searchTimeout) clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.initLoading();
      }, 500);
    },
    filterCategoryId() {
      this.onFilterCategoryChange();
      this.fetchShopProducts(1);
    },
    filterSubCategoryId() {
      this.fetchShopProducts(1);
    }
  },
  computed: {
    canManage() {
      // Désormais ouvert à tout utilisateur authentifié pour la gestion locale de sa boutique
      return !!this.active_user;
    },
    shopProductsCount() {
      return this.totalCountFromBackend || (this.$store?.state?.products || []).length;
    },
    filteredProducts() {
      // Le filtrage se fait désormais majoritairement côté backend
      // On retourne directement localProducts pour plus de fluidité
      return this.localProducts;
    }
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchCategories();
    this.fetchShopProducts();
    this.fetchActiveShopProducts(); // Pour le compteur
  },
  methods: {
    async fetchActiveShopProducts() {
      const shopId = this.shop?.id;
      if (!shopId) return;
      try {
        const res = await productsService.getProducts(shopId, { page_size: 1000 });
        const results = res.data.results || res.data || [];
        this.$store.state.products = results;
        if (res.data && typeof res.data.count !== 'undefined') {
          this.totalCountFromBackend = res.data.count;
        } else {
          this.totalCountFromBackend = results.length;
        }
      } catch (err) {
        console.error('Error fetching active shop products:', err);
      }
    },
    initLoading() {
      this.localProducts = [];
      this.currentPage = 1;
      this.hasNextPage = true;
      this.fetchShopProducts();
    },
    async fetchShopProducts(page = 1) {
      if (!this.shopIdProp && !this.$store?.state?.shop?.id) return;
      const shopId = this.shopIdProp || this.$store.state.shop.id;
      
      this.isLoading = true;
      try {
        const params = { 
          page, 
          page_size: 20 
        };
        
        // Ajout des filtres backend
        if (this.searchKeyword) {
          params['product__name__icontains'] = this.searchKeyword;
        }
        if (this.filterSubCategoryId) {
          params['product__sub_category'] = this.filterSubCategoryId;
        }

        const res = await productsService.getProducts(shopId, params);
        const data = res.data?.results ?? res.data ?? [];
        const paginated = !!res.data?.results;
        
        if (page === 1) {
          this.localProducts = data;
        } else {
          // Éviter les doublons
          const existingIds = new Set(this.localProducts.map(p => p.id));
          const newItems = data.filter(p => !existingIds.has(p.id));
          this.localProducts = [...this.localProducts, ...newItems];
        }

        this.hasNextPage = paginated && !!res.data?.next;
        this.currentPage = page;
      } catch (err) {
        // Un 404 sur une page > 1 signifie simplement qu'on est arrivé au bout
        if (err?.response?.status !== 404 || page === 1) {
          console.error('Error fetching shop products:', err);
        }
        this.hasNextPage = false;
      } finally {
        this.isLoading = false;
      }
    },
    async loadMore(ev) {
      if (this.hasNextPage) {
        await this.fetchShopProducts(this.currentPage + 1);
      }
      ev.target.complete();
    },
    fetchCategories() {
      return categoriesService.getCategories()
        .then((res) => {
          const raw = res.data.results || res.data || [];
          this.categories = Array.isArray(raw) ? raw : [];
        })
        .catch(() => {
          this.categories = [];
        });
    },
    onFilterCategoryChange() {
      this.filterSubCategoryId = null;
      const catId = this.filterCategoryId;
      if (!catId) {
        this.filterSubCategories = [];
        return;
      }
      subCategoriesService.getSubCategories({ category: catId })
        .then((res) => {
          const raw = res.data.results || res.data || [];
          this.filterSubCategories = Array.isArray(raw) ? raw : [];
        })
        .catch(() => {
          this.filterSubCategories = [];
        });
    },
    select(product) {
      modalController.dismiss(product, 'confirm');
    },
    async exportToExcel() {
      const shopProducts = this.$store?.state?.products || [];
      if (shopProducts.length === 0) {
        this.showTostMsg('Aucun produit dans votre boutique à exporter', 'warning');
        return;
      }

      const data = shopProducts.map(p => {
        const bp = p.product || {};
        return {
          'ID': p.id,
          'Nom du Produit': bp.name || 'N/A',
          'Catégorie': bp.category_name || 'N/A',
          'Quantité en Stock': p.quantity || 0,
          'Prix de Vente (BIF)': p.sale_price || 0,
          'Dernière Mise à jour': new Date(p.updated_at || Date.now()).toLocaleDateString()
        };
      });

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'MaBoutique');
      await saveWorkbook(wb, `AgaShop_MaBoutique_${new Date().toISOString().slice(0,10)}.xlsx`);
      
      this.showTostMsg('La liste des produits a été exportée avec succès', 'success');
    },
    dismiss() {
      modalController.dismiss(null, 'cancel');
    },
    async manageShopProduct(product) {
      if (!this.active_user) {
        this.showTostMsg("Veuillez vous connecter pour gérer les produits.", "warning", 3000);
        return;
      }
      
      const actionSheet = await actionSheetController.create({
        header: `Gérer ${product.name || product.product?.name}`,
        buttons: [
          {
            text: 'Changer le Prix de Vente',
            icon: createOutline,
            handler: () => this.openPriceModal(product)
          },
          {
            text: 'Contrôler le Stock',
            icon: listOutline,
            handler: () => this.openStockControlModal(product)
          },
          {
            text: 'Annuler',
            role: 'cancel'
          }
        ]
      });
      await actionSheet.present();
    },
    async openPriceModal(product) {
      const modal = await modalController.create({
        component: ChangeProductPrice,
        componentProps: { productProp: product }
      });
      await modal.present();
      const { role } = await modal.onDidDismiss();
      if (role === 'confirm') this.initLoading();
    },
    async openStockControlModal(product) {
      const { default: ControlProduct } = await import('./ControlProduct.vue');
      const modal = await modalController.create({
        component: ControlProduct,
        componentProps: { productProp: product }
      });
      await modal.present();
      const { role } = await modal.onDidDismiss();
      if (role === 'confirm') this.initLoading();
    },
    async confirmRemoveFromShop(product) {
      if (!this.active_user) {
        this.showTostMsg("Action non autorisée.", "warning", 3000);
        return;
      }
      const alert = await alertController.create({
        header: 'Retirer de la boutique ?',
        message: `Voulez-vous retirer "${product.name || product.product?.name}" de votre inventaire ?`,
        buttons: [
          { text: 'Annuler', role: 'cancel' },
          { 
            text: 'Oui, retirer', 
            role: 'destructive',
            handler: () => this.deleteFromShop(product.id)
          }
        ]
      });
      await alert.present();
    },
    async deleteFromShop(shopProductId) {
      try {
        await productsService.deleteProduct(shopProductId);
        this.localProducts = this.localProducts.filter(p => p.id !== shopProductId);
        this.showTostMsg("Produit retiré de la boutique.", "success", 3000);
        this.$emit('refresh');
      } catch (err) {
        this.errorOrRefresh(err, () => this.deleteFromShop(shopProductId));
      }
    }
  }
};
</script>

<style lang="scss" scoped>
ion-header ion-buttons[slot="start"] ion-button.back-arrow-white,
ion-header ion-buttons[slot="start"] ion-button.back-arrow-white ion-icon {
  --color: #fff;
  color: #fff;
}
ion-item {
  --padding-start: 16px;
  --inner-padding-end: 16px;
  ion-thumbnail {
    --size: 56px;
    --border-radius: 10px;
  }
  ion-img {
    border-radius: 10px;
    object-fit: cover;
  }
  h2 {
    font-weight: 700;
    font-size: 1.05rem;
    color: #1e293b;
    margin-bottom: 2px;
  }
  .stock-label {
    font-weight: 500;
    color: #64748b;
    span {
      color: var(--ion-color-primary);
      font-weight: 700;
    }
  }
  .chevron-icon {
    font-size: 1.2rem;
    color: #cbd5e1;
  }
}

ion-item-option {
  --padding-start: 16px;
  --padding-end: 16px;
  .option-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
  }
  ion-icon {
    font-size: 1.5rem;
  }
}

.header-title-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding-right: 8px;

  .main-title {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    flex: 1;
  }

  .shop-count-wrapper {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.15);
    padding: 4px 8px;
    border-radius: 12px;

    .count-label {
      font-size: 0.65rem;
      font-weight: 800;
      color: rgba(255, 255, 255, 0.9);
      letter-spacing: 0.05em;
    }

    .shop-count-badge {
      font-size: 0.8rem;
      --padding-start: 6px;
      --padding-end: 6px;
      border-radius: 8px;
      color: var(--ion-color-primary);
      background: #fff;
      font-weight: 800;
      min-width: 24px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  }
}

.toolbar-shop-count {
  font-size: 0.8rem;
  font-weight: 700;
  color: #fff;
  background: rgba(0, 0, 0, 0.2);
  padding: 2px 10px;
  border-radius: 20px;
  margin-top: 4px;
}

.custom-searchbar {
  --background: rgba(255, 255, 255, 0.95);
  --border-radius: 12px;
  --placeholder-color: #64748b;
  --icon-color: var(--ion-color-primary);
  padding: 8px 16px;
}
.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-top: 8px;
  margin-bottom: 4px;
}
.filter-item {
  flex: 1;
  min-width: 140px;
  --background: rgba(255, 255, 255, 0.95);
  border-radius: 10px;
  --padding-start: 12px;
  --padding-end: 12px;
  --inner-padding-end: 0;

  ion-select {
    max-width: 100%;
    width: 100%;
  }
}
</style>
