<!--
  * @file CriticalArticlesList.vue
  * @description Page pour la gestion de Critical Articles List.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-critical-articles" name="back-to-critical-articles" @click="$router.push({ name: 'critical-articles' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Alertes Stock</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchProducts">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
          <ion-button @click="openCustomSearch">
            <ion-icon color="light" size="large" :icon="options"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>

      <ion-toolbar color="secondary">
        <ion-searchbar 
          id="critical-articles-search"
          name="critical-articles-search"
          v-model="keyword" 
          placeholder="Rechercher un article..." 
          color="light"
          class="custom-searchbar"
        ></ion-searchbar>
        <!-- Assuming the user intended to add an ion-select here, based on the provided attributes -->
        <!-- The original instruction had ion-searchbar tags around ion-select attributes, which is syntactically incorrect. -->
        <!-- This is a corrected interpretation of the user's intent to add an ion-select. -->
        <ion-select
          v-model="filterCategoryId"
          placeholder="Filtre par catégorie"
          interface="popover"
          class="custom-select"
          @ionDismiss="removeFocus"
        >
          <ion-select-option :value="null">Toutes les catégories</ion-select-option>
          <ion-select-option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </ion-select-option>
        </ion-select>
      </ion-toolbar>
    </ion-header>

    <ion-content class="history-content">
      <!-- 1. Filters & Summary -->
      <div class="selection-area">
        <!-- Date range selectors for harmonization -->
        <div class="range-selector-container">
          <div class="date-picker-item">
            <span class="picker-label">Du :</span>
            <ion-datetime-button datetime="critical-start-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="critical-start-date" presentation="date" v-model="startDate" @ionChange="fetchProducts" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
          <div class="date-picker-item">
            <span class="picker-label">Au :</span>
            <ion-datetime-button datetime="critical-end-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="critical-end-date" presentation="date" v-model="endDate" @ionChange="fetchProducts" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
        </div>
      </div>

      <div class="revenue-summary alert-summary">
        Articles en difficulté : <span class="amount red-text">{{ filteredProducts.length }}</span> 
        <br/>
        <span class="sub-alert">Stock inférieur ou égal à 5 unités</span>
      </div>

      <!-- 2. Table Header -->
      <div class="table-header">
        <div class="col article-col italic">Article / Alerte</div>
        <div class="col total-col italic text-right">Stock</div>
      </div>

      <!-- 3. Critical List -->
      <div class="sales-list-container">
        <div v-for="p in filteredProducts" :key="p.id" class="sale-row">
          <div class="col article-col">
            <ion-thumbnail slot="start" class="small-thumb">
              <img :src="p.product?.image || '/placeholder.png'" />
            </ion-thumbnail>
            <div class="art-info">
              <div class="art-name">{{ p.product?.name }}</div>
              <div class="art-cat">{{ getCategoryLabel(p) }}</div>
              <div class="art-status" :class="p.quantity <= 0 ? 'red-text' : 'orange-text'">
                {{ p.quantity <= 0 ? 'RUPTURE DE STOCK' : 'STOCK CRITIQUE' }}
              </div>
            </div>
          </div>
          <div class="col total-col">
            <div class="stock-action-box">
              <div class="stock-qty-val" :class="p.quantity <= 0 ? 'red-text' : 'orange-text'">
                {{ p.quantity }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredProducts.length === 0 && !loading" class="empty-state">
           🎉 Aucun article en stock critique !
        </div>
      </div>

      <ion-progress-bar v-if="loading" type="indeterminate"></ion-progress-bar>
    </ion-content>
  </ion-page>
</template>

<script>
import {
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
  IonThumbnail,
  modalController,
  toastController,
  IonInput,
  IonDatetimeButton,
  IonModal,
  IonDatetime,
  IonSelect,
  IonSelectOption
} from '@ionic/vue';
import { 
  arrowBackOutline, 
  refreshCircleOutline, 
  options, 
  addCircle,
  downloadOutline 
} from 'ionicons/icons';
import * as XLSX from 'xlsx';
import { saveWorkbook } from '../../utils/exportExcel';
import { productsService } from '../../services/api/products';
import { categoriesService } from '../../services/api/categories';
import globalMixins from '../../composables/mixins';
import SupplyProduct from '../../components/shop/SupplyProduct.vue';

/**
 * Composant CriticalArticlesList
 * - Gère l'interface et la logique métier de Critical Articles List.
 */
export default {
  mixins: [globalMixins],
  name: 'CriticalArticlesList',
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
    IonThumbnail,
    IonInput,
    IonDatetimeButton,
    IonModal,
    IonDatetime,
    IonSelect,
    IonSelectOption
  },
  data() {
    return {
      arrowBackOutline,
      refreshCircleOutline,
      options,
      addCircle,
      downloadOutline,
      products: [],
      categories: [],
      keyword: '',
      filterCategoryId: null, // Added for the new ion-select
      startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
      loading: false,
      shop: this.$store.state.shop
    };
  },
  computed: {
    shopId() {
      return this.$store.state.shop?.id || this.shop?.id;
    },
    filteredProducts() {
      let list = this.products.filter(p => p.quantity <= 5);
      if (this.keyword) {
        const k = this.keyword.toLowerCase();
        list = list.filter(p => p.product?.name?.toLowerCase().includes(k));
      }
      // Add filtering by category if filterCategoryId is set
      if (this.filterCategoryId) {
        list = list.filter(p => {
          const bp = p.product;
          const sub = bp?.sub_category;
          const subId = bp?.sub_category_id ?? (typeof sub === 'number' ? sub : sub?.id);
          if (!subId) return false;
          
          if (this.categories && this.categories.length) {
            const cat = this.categories.find(c => {
               const subs = c.sub_categories || c.subCategories || [];
               return subs.some(s => Number(s.id) === Number(subId));
            });
            return cat && Number(cat.id) === Number(this.filterCategoryId);
          }
          return sub?.category?.id === this.filterCategoryId;
        });
      }
      return list.sort((a, b) => a.quantity - b.quantity);
    }
  },
  ionViewDidEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Alerte Stocks Critiques',
      description: 'C\'est votre tableau de bord d\'urgence. Ici sont listés uniquement les produits dont la quantité en rayon est tombée à 5 unités ou moins. C\'est le signal qu\'il faut commander à nouveau.',
      elements: [
        { label: 'Indicateur (X)', type: 'Alerte', desc: 'Le nombre en gros devant chaque produit indique la quantité restante exacte. Si c\'est 0, vous êtes en rupture.' },
        { label: 'Contrôle rapide', type: 'Action', desc: 'Le bouton "Contrôle" permet d\'ajouter du stock immédiatement si vous venez de recevoir une livraison de ce produit.' },
        { label: 'Recherche', type: 'Filtre', desc: 'Permet de trouver rapidement un article spécifique pour vérifier s\'il doit être réapprovisionné.' }
      ],
      faq: [
        { question: 'Pourquoi cet écran est important ?', answer: 'Il vous permet d\'anticiper les ruptures de stock qui font perdre de l\'argent. Un produit sur cet écran doit être votre priorité d\'achat.' },
        { question: 'Comment faire disparaître un article ?', answer: 'Dès que vous enregistrez un "Achat" ou un "Contrôle" qui remonte le stock au-dessus de 5 unités, il disparaît automatiquement de cette liste.' }
      ]
    });
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchProducts();
    this.fetchCategories();
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
    async fetchProducts() {
      if (!this.shopId) return;
      this.loading = true;
      try {
        const res = await productsService.getProducts(this.shopId, {
          created_at__gte: this.startDate,
          created_at__lte: this.endDate
        });
        this.products = res.data.results || res.data || [];
      } catch (err) {
        console.error("[CriticalArticlesList] Erreur:", err);
      } finally {
        this.loading = false;
      }
    },
    async fetchCategories() {
      try {
        const res = await categoriesService.getCategories();
        this.categories = res.data.results || res.data || [];
      } catch (err) {
        console.error("[CriticalArticlesList] Erreur catégories:", err);
      }
    },
    async exportToExcel() {
       if (this.filteredProducts.length === 0) {
         this.showToastMsg('Aucune alerte à exporter', 'warning');
         return;
       }

       const data = this.filteredProducts.map(p => ({
         'Article': p.product?.name,
         'Statut': p.quantity <= 0 ? 'RUPTURE' : 'CRITIQUE',
         'Stock Actuel': p.quantity,
         'Prix de Vente (BIF)': parseFloat(p.sale_price)
       }));

       const ws = XLSX.utils.json_to_sheet(data);
       const wb = XLSX.utils.book_new();
       XLSX.utils.book_append_sheet(wb, ws, "Alertes_Stock");
       
       const fileName = `Alertes_Stock_${this.startDate}_au_${this.endDate}.xlsx`;
       await saveWorkbook(wb, fileName);
       this.showToastMsg('Export Excel réussi !', 'success');
    },

    async supplyItem(product) {
       const modal = await modalController.create({
         component: SupplyProduct,
         componentProps: { productProp: product }
       });
       await modal.present();
       const { role } = await modal.onDidDismiss();
       if (role === 'confirm') {
         this.fetchProducts();
         this.showToast('Approvisionnement réussi', 'success');
       }
    },
    openCustomSearch() {
      // Pour une duplication exacte, on garde l'icône mais on pourrait ajouter plus de filtres ici.
      console.log('Filtres avancés');
    },
    async showToast(message, color = 'dark') {
      const toast = await toastController.create({ message, duration: 2000, color });
      await toast.present();
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
  --background: #f1f5f9;
}

.selection-area {
  padding: 16px 12px;
}

.history-content {
  --background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
  background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
}

.range-selector-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 12px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin: 10px 12px;
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
  border-color: #ef4444;
}

.revenue-summary {
  text-align: center;
  color: #0f172a;
  font-weight: 800;
  font-size: 1.15rem;
  margin: 16px 12px;
  background: white;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-top: 6px solid #ef4444;
}

.sub-alert {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 600;
  margin-top: 4px;
  display: block;
}

.red-text { color: #ef4444; font-weight: 800; }
.orange-text { color: #f59e0b; font-weight: 800; }

.table-header {
  display: flex;
  background: #ef4444;
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

.art-status {
  font-size: 0.75rem;
  font-weight: 800;
  margin-top: 4px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.stock-action-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stock-qty-val {
  font-size: 1.2rem;
  font-weight: 900;
}

.supply-icon-btn {
  --padding-start: 0;
  --padding-end: 0;
  margin: 0;
  --color: #ef4444;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #10b981;
  font-weight: 800;
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
