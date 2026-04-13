<!--
  * @file StockVolumeList.vue
  * @description Page pour la gestion de Stock Volume List.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-stock-volume" name="back-to-stock-volume" @click="$router.push({ name: 'stock-volume' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Détail des Quantités</span>
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
          id="stock-volume-search"
          name="stock-volume-search"
          v-model="keyword" 
          placeholder="Rechercher..." 
          animated
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
              id="stock-volume-category"
              name="stock-volume-category"
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
          </ion-item>
        </div>

        <!-- Date range selectors for harmonization -->
        <div class="range-selector-container">
          <div class="date-picker-item">
            <span class="picker-label">Du :</span>
            <ion-datetime-button datetime="stock-start-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="stock-start-date" presentation="date" v-model="startDate" @ionChange="fetchProducts" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
          <div class="date-picker-item">
            <span class="picker-label">Au :</span>
            <ion-datetime-button datetime="stock-end-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="stock-end-date" presentation="date" v-model="endDate" @ionChange="fetchProducts" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
        </div>
      </div>

      <!-- 2. Volume Summary Bar -->
      <div class="revenue-summary volume-summary">
        Volume physique total : <span class="amount blue-text">{{ totalUnits }}</span> <span class="unit-label">articles</span>
      </div>

      <!-- 3. Table Header -->
      <div class="table-header volume-header">
        <div class="col article-col italic">Article / Catégorie</div>
        <div class="col total-col italic">Quantité Physique</div>
      </div>

      <!-- 4. Units List -->
      <div class="sales-list-container">
        <div v-for="p in filteredProducts" :key="p.id" class="sale-row">
          <div class="col article-col">
            <ion-thumbnail slot="start" class="small-thumb">
              <img :src="p.product?.image || '/placeholder.png'" />
            </ion-thumbnail>
            <div class="art-info">
              <div class="art-name">{{ p.product?.name }}</div>
              <div class="art-cat">{{ getCategoryLabel(p) }}</div>
            </div>
          </div>
          <div class="col total-col">
            <div class="stock-qty-badge" :class="p.quantity <= 0 ? 'red-bg' : (p.quantity <= 5 ? 'orange-bg' : 'blue-bg')">
              {{ p.quantity }}
            </div>
          </div>
        </div>

        <div v-if="filteredProducts.length === 0 && !loading" class="empty-state">
           Aucun produit correspondant.
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
  IonSelect,
  IonSelectOption,
  IonItem,
  IonThumbnail,
  toastController,
  IonInput,
  IonDatetimeButton,
  IonModal,
  IonDatetime
} from '@ionic/vue';
import { 
  arrowBackOutline, 
  refreshCircleOutline,
  downloadOutline
} from 'ionicons/icons';
import * as XLSX from 'xlsx';
import { productsService } from '../../services/api/products';
import { categoriesService } from '../../services/api/categories';
import globalMixins from '../../composables/mixins';

/**
 * Composant StockVolumeList
 * - Gère l'interface et la logique métier de Stock Volume List.
 */
export default {
  mixins: [globalMixins],
  name: 'StockVolumeList',
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
    IonDatetime
  },
  data() {
    return {
      arrowBackOutline,
      refreshCircleOutline,
      downloadOutline,
      products: [],
      categories: [],
      filterCategoryId: null,
      keyword: '',
      startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
      loading: false,
      shop: this.$store.state.shop
    };
  },
  computed: {
    isReadOnly() {
      return this.$route.query.readonly === '1';
    },
    shopId() {
      return this.$store.state.shop?.id || this.shop?.id;
    },
    totalUnits() {
      return this.products.reduce((sum, p) => sum + Number(p.quantity || 0), 0);
    },
    filteredProducts() {
      let list = this.products;
      if (this.filterCategoryId) {
        list = list.filter(p => {
          const sub = p.product?.sub_category;
          const catId = typeof sub === 'object' ? sub.category?.id : null;
          return catId === this.filterCategoryId;
        });
      }
      if (this.keyword) {
        const k = this.keyword.toLowerCase();
        list = list.filter(p => p.product?.name?.toLowerCase().includes(k));
      }
      return list.sort((a, b) => b.quantity - a.quantity); // Sort by quantity descending
    }
  },
  ionViewDidEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Volume et Valeur Totale du Stock',
      description: 'Cet écran vous donne la vue d\'ensemble de votre patrimoine. Il répond à la question : "Si je vendais tout ce que j\'ai aujourd\'hui, combien gagnerais-je ?"',
      elements: [
        { label: 'Valeur de Vente (V)', type: 'Indicateur', desc: 'Le chiffre d\'affaires brut potentiel contenu dans vos rayons.' },
        { label: 'Valeur d\'Achat (A)', type: 'Indicateur', desc: 'Ce que vous avez réellement payé pour acquérir ce stock. C\'est votre base d\'investissement.' },
        { label: 'Différence (V - A)', type: 'Profit Latent', desc: 'La marge que vous réaliserez une fois tous ces produits vendus.' },
        { label: 'Filtre Catégorie', type: 'Outils', desc: 'Permet de voir la valeur d\'un seul rayon (ex: Boissons uniquement) pour un inventaire ciblé.' }
      ],
      faq: [
        { question: 'À quoi sert cet écran ?', answer: 'Il est crucial lors de vos inventaires de fin de mois. Il permet de s\'assurer que la valeur théorique enregistrée dans AgaShop correspond à ce que vous voyez physiquement en boutique.' },
        { question: 'Pourquoi y a-t-il un bouton Export ?', answer: 'Pour imprimer ou envoyer un fichier Excel de vos stocks à votre comptable ou pour vos archives personnelles.' }
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
        console.error("[StockVolumeList] Erreur:", err);
      } finally {
        this.loading = false;
      }
    },
    exportToExcel() {
       if (this.products.length === 0) {
         this.showToastMsg('Aucune donnée à exporter', 'warning');
         return;
       }

       const data = this.products.map(p => ({
         'Article': p.product?.name,
         'Catégorie': this.getCategoryLabel(p),
         'Quantité Physique': p.quantity,
         'Date': new Date().toLocaleDateString('fr-FR')
       }));

       const ws = XLSX.utils.json_to_sheet(data);
       const wb = XLSX.utils.book_new();
       XLSX.utils.book_append_sheet(wb, ws, "Volume_Stock");
       
       const fileName = `Volume_Stock_${this.startDate}_au_${this.endDate}.xlsx`;
       XLSX.writeFile(wb, fileName);
       this.showToastMsg('Export Excel réussi !', 'success');
    },
    async showToastMsg(message, color = 'dark') {
      const toast = await toastController.create({
        message,
        duration: 2000,
        color,
        position: 'bottom'
      });
      await toast.present();
    },
    async fetchCategories() {
      try {
        const res = await categoriesService.getCategories();
        this.categories = res.data.results || res.data || [];
      } catch (err) {
        console.error("[StockVolumeList] Erreur catégories:", err);
      }
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

.volume-summary {
  font-size: 1.1rem;
}

.amount { font-size: 1.5rem; font-weight: 900; }
.unit-label { font-size: 0.9rem; color: #64748b; margin-left: 6px; font-weight: 600; }
.blue-text { color: var(--ion-color-secondary); }

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

.art-info {
  display: flex;
  flex-direction: column;
}

.art-cat {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 600;
  margin-top: 2px;
}

.stock-qty-badge {
  padding: 8px 16px;
  border-radius: 12px;
  font-weight: 900;
  font-size: 1.05rem;
  color: #fff;
  min-width: 60px;
  text-align: center;
}

.blue-bg { background: var(--ion-color-secondary); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
.orange-bg { background: #f59e0b; box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.2); }
.red-bg { background: #ef4444; box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2); }

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

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
</style>
