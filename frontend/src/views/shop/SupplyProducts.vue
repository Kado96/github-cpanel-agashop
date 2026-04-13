<!--
  * @file SupplyProducts.vue
  * @description Page pour la gestion de Supply Products.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="secondary">
          <ion-buttons slot="start">
            <ion-button id="back-to-shop" name="back-to-shop" @click="$router.push({ name: 'shop' })">
              <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
            </ion-button>
          </ion-buttons>

          <ion-title color="light">
            <div class="header-title-container">
              <span>Mes Achats</span>
            </div>
          </ion-title>

          <ion-buttons slot="end">
            <ion-button @click="fetchSupplies(1)">
              <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
            </ion-button>
            <ion-button v-if="mode === 'historique'" @click="deepSearch">
              <ion-icon color="light" size="large" :icon="options"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
        <ion-toolbar v-if="mode === 'historique'">
          <ion-searchbar 
            id="supply-history-search"
            name="search"
            v-model="keyword" 
            show-clear-button="focus" 
            placeholder="Rechercher"
          ></ion-searchbar>
          <ion-progress-bar type="indeterminate" v-if="loading"></ion-progress-bar>
        </ion-toolbar>
    </ion-header>

<ion-content>
  <div class="supply-actions-bar">
    <ion-toolbar color="primary">
      <ion-buttons class="ion-justify-content-center ion-no-padding">
        <ion-button fill="clear" color="light" :class="{ active: mode === 'enregistrer' }" @click="onEnregistrerClick">
          <ion-icon slot="start" :icon="documentTextOutline"></ion-icon>
          Enregistrer un achat
        </ion-button>
        <ion-button fill="clear" color="light" :class="{ active: mode === 'historique' }" @click="setMode('historique')">
          <ion-icon slot="start" :icon="timeOutline"></ion-icon>
          Historique des achats
        </ion-button>
      </ion-buttons>
    </ion-toolbar>
  </div>

  <!-- En mode Historique : liste des achats avec glissement (Modifier / Supprimer) -->
  <template v-if="mode === 'historique'">
    <!-- Filtres par catégorie et sous-catégorie -->
    <div class="filter-row ion-margin-horizontal">
      <ion-item lines="none" class="filter-item">
        <ion-select
          id="history-filter-category"
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
          id="history-filter-sub-category"
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

    <ion-list ref="historiqueList" class="products-list-compact">
      <ion-list-header>Totals : {{ money(totals ?? 0) }} BIF · Quantité : {{ totals_quantity ?? 0 }}</ion-list-header>
      <ion-item-sliding v-for="supply in filteredDisplayedSupplies" :key="supply.id">
        <ion-item-options side="start">
          <ion-item-option @click="openEditSupplyModal(supply)" color="primary">
            <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
            Modifier
          </ion-item-option>
          <ion-item-option @click="confirmDeleteSupply(supply)" color="danger">
            <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
            Supprimer
          </ion-item-option>
        </ion-item-options>

        <ion-item>
          <ion-thumbnail slot="start">
            <ion-img :src="productImage(supply)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
          </ion-thumbnail>
          <ion-label>
            <h2>{{ supply?.product?.name }}</h2>
            <p v-if="getCategoryLabel(supply)" class="category-label">{{ getCategoryLabel(supply) }}</p>
            <p>Quantité : {{ supply?.quantity ?? '—' }}</p>
            <ion-text>P.A.U : {{ money(supply?.quantity ? supply.total_buy_price / supply.quantity : 0) }} BIF</ion-text>
            <br />
            <ion-text>P.A.T : {{ money(supply?.total_buy_price ?? 0) }} BIF</ion-text>
            <br />
            <ion-text color="primary">Date : {{ formatDateTime(supply?.created_at) }}</ion-text>
          </ion-label>
        </ion-item>

        <ion-item-options side="end">
          <ion-item-option @click="openEditSupplyModal(supply)" color="primary">
            <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
            Modifier
          </ion-item-option>
          <ion-item-option @click="confirmDeleteSupply(supply)" color="danger">
            <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
            Supprimer
          </ion-item-option>
        </ion-item-options>
      </ion-item-sliding>
      
      <ion-infinite-scroll @ionInfinite="loadMoreSupplies" :disabled="!hasNextPage" id="supplies-infinite-scroll">
        <ion-infinite-scroll-content loading-spinner="bubbles" loading-text="Chargement de l'historique..."></ion-infinite-scroll-content>
      </ion-infinite-scroll>

      <ion-item v-if="filteredDisplayedSupplies.length === 0 && !loading" lines="none">
        <ion-label class="ion-text-center">
          <p v-if="displayedSupplies.length === 0">Aucun achat sur la période.</p>
          <p v-else>Aucun achat ne correspond aux filtres sélectionnés.</p>
        </ion-label>
      </ion-item>
    </ion-list>
  </template>

  <!-- En mode Enregistrer : uniquement la barre d’actions -->
  <div v-else class="ion-padding ion-text-center">
    <p>Cliquez sur « Enregistrer un achat » pour ajouter un achat.</p>
  </div>
</ion-content>
</ion-page>
</template>

<script>
 import {
   IonHeader,
   IonPage,
   modalController,
   alertController,
   IonToolbar,
   IonButtons,
   IonButton,
   IonIcon,
   IonBadge,
   IonText,
   IonContent,
   IonItem,
   IonItemSliding,
   IonItemOptions,
   IonItemOption,
   IonLabel,
   IonThumbnail,
   IonListHeader,
   IonSelect,
   IonSelectOption,
   IonRow,
   IonCol,
   IonCard,
   IonTitle,
   IonFab,
   IonFabButton,
   IonList,
   IonPopover,
   IonImg,
   IonBackButton,
   IonSearchbar,
   IonProgressBar,
   actionSheetController,
   IonInfiniteScroll,
   IonInfiniteScrollContent,
 } from '@ionic/vue';
 
 import {
   cartOutline,
   exitOutline,
   home,
   addOutline,
   fastFoodOutline,
   personOutline,
   ellipsisVertical,
   arrowBackOutline,
   options,
   refreshCircleOutline,
   documentTextOutline,
   timeOutline,
   createOutline,
   trashOutline,
 } from 'ionicons/icons'
import CustomSearch from '../../components/CustomSearch.vue';
import { suppliesService, productsService, categoriesService, subCategoriesService } from '../../services/api';
import { axiosService } from '../../plugins/axios';
import globalMixins from '../../composables/mixins';

function getMediaBaseUrl() {
  const base = axiosService?.defaults?.baseURL ?? '';
  return base.replace(/\/api\/?$/, '') || (typeof window !== 'undefined' ? window.location.origin : '');
}
import SupplyProduct from '../../components/shop/SupplyProduct.vue';
import SupplyProductPicker from '../../components/shop/SupplyProductPicker.vue';
import EditSupplyProduct from '../../components/shop/EditSupplyProduct.vue';
 
 /**
 * Composant SupplyProducts
 * - Gère l'interface et la logique métier de Supply Products.
 */
export default {
   mixins: [globalMixins],
   components: {
    IonImg,
    IonHeader,
    IonBackButton,
    IonPage,
    SupplyProduct,
    SupplyProductPicker,
    EditSupplyProduct,
    IonToolbar,
    IonButtons,
    IonButton,
    IonIcon,
    IonBadge,
    IonText,
    IonContent,
    IonItem,
    IonItemSliding,
    IonItemOptions,
    IonItemOption,
   IonList,
   IonSelect,
   IonSelectOption,
   IonPopover,
   IonLabel,
    IonThumbnail,
    IonListHeader,
    IonRow,
    IonCol,
    IonCard,
    IonTitle,
    IonFab,
    IonFabButton,
    IonSearchbar,
    IonProgressBar,
    IonInfiniteScroll,
    IonInfiniteScrollContent,
    IonImg
   },
   setup() {
     return {
       cartOutline,
       home,
       exitOutline,
       addOutline,
       fastFoodOutline,
       personOutline,
       ellipsisVertical,
       arrowBackOutline,
       refreshCircleOutline,
       options,
       documentTextOutline,
       timeOutline,
       createOutline,
       trashOutline,
     };
   },
   data() {
      return {
        supplies: [],
        mode: 'historique',
        dateRange: { du: '', au: '' },
        totals: null,
        totals_quantity: null,
        shop: this.$store.state.shop,
        loading: false,
        keyword: '',
        filterCategoryId: null,
        categories: [],
        filterSubCategoryId: null,
        filterSubCategories: [],
        currentPage: 1,
        hasNextPage: true,
        searchTimeout: null
      };
   },
    watch: {
    '$store.state.supplies'(val) {
      const res = val?.results ?? [];
      const tot = val?.totals ?? null;
      const totQty = val?.totals_quantity ?? null;
      this.supplies = this.keyword ? this.filterSupplies(res, this.keyword) : res;
      this.totals = tot;
      this.totals_quantity = totQty;
    },
    keyword(v) {
      const base = this.$store.state.supplies?.results ?? [];
      this.supplies = v ? this.filterSupplies(base, v) : base;
    },
   },
   computed: {
    shopId() {
      return this.$store.state.shop?.id;
    },
    /** Achats avec quantité > 0 et P.A.T > 0 uniquement (exclut les lignes à zéro) */
    displayedSupplies() {
      return (this.supplies || []).filter((s) => {
        const q = Number(s?.quantity ?? 0);
        const t = Number(s?.total_buy_price ?? 0);
        return q > 0 && t > 0;
      });
    },
    filteredDisplayedSupplies() {
      let list = this.displayedSupplies || [];
      const catId = this.filterCategoryId;
      const subId = this.filterSubCategoryId;

      const getSubCategoryId = (s) => {
        const bp = s?.product?.product ?? s?.product;
        const sub = bp?.sub_category;
        return bp?.sub_category_id ?? sub?.id ?? sub ?? null;
      };

      if (subId != null && subId !== '') {
        list = list.filter((s) => Number(getSubCategoryId(s)) === Number(subId));
      } else if (catId != null && catId !== '') {
        const validSubIds = (this.filterSubCategories || []).map((s) => Number(s.id));
        list = list.filter((s) => {
          const scId = getSubCategoryId(s);
          return scId != null && validSubIds.includes(Number(scId));
        });
      }

      return [...list].sort((a, b) => {
        const na = (a?.product?.name || a?.product?.product?.name || '').toLowerCase();
        const nb = (b?.product?.name || b?.product?.product?.name || '').toLowerCase();
        return na.localeCompare(nb);
      });
    },
   },
   beforeMount() {
    this.$store.state.shop = this.getShopFromLocalStorage();
    this.checkCurrentShop();
    const existing = this.$store.state.supplies;
    const hasResults = existing?.results?.length > 0;
    this.fetchCategories();
    if (!hasResults) this.fetchSupplies();
    else {
      this.supplies = existing.results ?? [];
      this.totals = existing.totals ?? null;
      this.totals_quantity = existing.totals_quantity ?? null;
    }
   },
   methods:{
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
        fetchSupplies(page = 1) {
          if (!this.shopId) return;
          // Si page est un événement (clic direct du bouton), on revient à 1
          const pageNumber = typeof page === 'number' ? page : 1;
          
          this.loading = true;
          if (pageNumber === 1) this.dateRange = { du: '', au: '' };

          suppliesService.getSupplies(this.shopId, { page: pageNumber, page_size: 20 })
            .then((res) => {
              const data = res?.data ?? {};
              const results = data?.results ?? [];
              const paginated = !!data?.results;

              if (page === 1) {
                this.supplies = results;
                this.$store.state.supplies = data;
              } else {
                this.supplies = [...this.supplies, ...results];
                // Mise à jour partielle du store si nécessaire
                if (this.$store.state.supplies) {
                  this.$store.state.supplies.results = this.supplies;
                }
              }

              this.totals = data?.totals ?? this.totals;
              this.totals_quantity = data?.totals_quantity ?? this.totals_quantity;
              this.hasNextPage = paginated && !!data?.next;
              this.currentPage = page;
              this.loading = false;
            })
            .catch((err) => {
              this.loading = false;
              this.hasNextPage = false;
              this.errorOrRefresh(err, () => this.fetchSupplies(page));
            });
        },
        async loadMoreSupplies(ev) {
          if (this.hasNextPage && !this.loading) {
            await this.fetchSupplies(this.currentPage + 1);
          }
          ev.target.complete();
        },
       setMode(m) {
         this.mode = m;
       },
       filterSupplies(list, q) {
         const k = (q || '').toLowerCase();
         return (list || []).filter((x) => JSON.stringify(x).toLowerCase().includes(k));
       },
       performDeepSearch(du, au) {
         this.loading = true;
         this.dateRange = { du: du || '', au: au || '' };
         suppliesService.getSupplies(this.shopId, { created_at__gte: du, created_at__lte: au })
           .then((res) => {
             const data = res?.data ?? {};
             const results = data?.results ?? [];
             const hasResults = results.length > 0;
             if (!hasResults)
               this.showTostMsg('Aucun achat sur cette période. La liste affiche le vide.', 'tertiary', 5000);
             this.$store.state.supplies = data;
             this.supplies = results;
             this.totals = data?.totals ?? null;
             this.totals_quantity = data?.totals_quantity ?? null;
             this.loading = false;
           })
           .catch((err) => {
             this.loading = false;
             this.errorOrRefresh(err, () => this.fetchSupplies());
           });
       },
       async deepSearch() {
         if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
         const modal = await modalController.create({
           component: CustomSearch,
           componentProps: { shopIdProp: this.shopId, initialDu: this.dateRange.du, initialAu: this.dateRange.au, introMessage: 'Choisissez la période pour filtrer les achats.' },
           initialBreakpoint: 0.75,
           breakpoints: [0, 0.75, 1],
         });
         await modal.present();
         const { data, role } = await modal.onWillDismiss();
         if (role === 'confirm' && data?.du && data?.au) {
           this.performDeepSearch(data.du, data.au);
           await this.fetchCategories();
           if (this.filterCategoryId) this.onFilterCategoryChange();
         }
       },
       goToSupplyActions(supply) {
           this.$router.push({ name: 'supply-product-actions', state: { supply } });
       },
       async openEditSupplyModal(supply) {
         if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
         const modal = await modalController.create({
           component: EditSupplyProduct,
           componentProps: { supplyProp: supply },
           initialBreakpoint: 0.75,
           breakpoints: [0, 0.75, 1],
         });
         await modal.present();
         const { role } = await modal.onWillDismiss();
         if (role === 'confirm') {
           this.fetchSupplies();
           await this.fetchCategories();
           if (this.filterCategoryId) this.onFilterCategoryChange();
         }
       },
       async confirmDeleteSupply(supply) {
         const productName = supply?.product?.name ?? supply?.product?.product?.name ?? 'cet achat';
         const alert = await alertController.create({
           header: 'Supprimer l\'achat',
           message: `Voulez-vous vraiment supprimer l'achat « ${productName } » ? Cette action est irréversible.`,
           buttons: [
             { text: 'Annuler', role: 'cancel' },
             { text: 'Supprimer', role: 'destructive', handler: () => this.deleteSupply(supply) }
           ]
         });
         await alert.present();
       },
       async deleteSupply(supply) {
         const id = supply?.id;
         if (!id) return;
         try {
           await suppliesService.deleteSupply(id);
           this.showTostMsg('Achat supprimé.', 'success', 3000);
           this.fetchSupplies();
         } catch (err) {
           this.errorOrRefresh(err, () => this.fetchSupplies());
         }
       },
       onEnregistrerClick() {
         this.setMode('enregistrer');
         this.openEnregistrerAchat();
       },
       async openEnregistrerAchat() {
         if (!this.shopId) return;
         try {
           if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
           const pickerModal = await modalController.create({
             component: SupplyProductPicker,
             componentProps: { shopIdProp: this.shopId },
             initialBreakpoint: 0.75,
             breakpoints: [0, 0.75, 1],
           });
           await pickerModal.present();
           const { data: selectedProduct, role } = await pickerModal.onWillDismiss();
           if (role !== 'confirm' || !selectedProduct) return;
           const supplyModal = await modalController.create({
             component: SupplyProduct,
             componentProps: { productProp: selectedProduct },
           });
           await supplyModal.present();
           await supplyModal.onWillDismiss();
           this.fetchSupplies();
           await this.fetchCategories();
           if (this.filterCategoryId) this.onFilterCategoryChange();
           this.setMode('historique');
         } catch (err) {
           console.error('Error opening supply picker:', err);
         }
       },
   }
 }
 </script>

<style lang="scss" scoped>
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

.products-list-compact {
  margin: 4px 16px 16px 16px;
}

.supply-actions-bar {
  ion-toolbar {
    --min-height: 52px;
  }
  ion-button {
    color: rgba(255,255,255,0.85);
    font-weight: 600;
  }
  ion-button.active {
    color: #fff;
    font-weight: 700;
  }
  ion-button ion-icon {
    color: inherit;
  }
}
ion-item {
  margin-bottom: 1vh;
  ion-thumbnail {
    width: 5rem;
    height: 6rem;
    --border-radius: 10px;
    ion-img {
      border-radius: 10px;
      object-fit: cover;
    }
  }
  h2 {
    font-weight: 600;
    font-size: 1rem;
  }
  ion-label, ion-text {
    font-size: 1rem;
    font-weight: 600;
  }
  p {
    font-size: 0.875rem;
    font-weight: normal;
    margin-top: 10px;
  }
  .category-label {
    font-size: 0.8rem;
    color: var(--ion-color-primary);
    font-weight: 500;
    margin-top: 2px;
  }
}

ion-button {
    ion-icon {
        font-size: 2rem;
    }
}
</style>