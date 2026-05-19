<!--
  * @file SalesList.vue
  * @description Page pour la gestion de Sales List.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-sales" name="back-to-sales" @click="$router.push({ name: 'sales' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Historiques des Ventes</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button id="refresh-sales-btn" @click="fetchSales">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="history-content">
      <!-- 1. Selection Mode Area (DESIGN ORIGINAL RESTAURÉ) -->
      <div class="selection-area">
        <div class="selection-row">
          
          <ion-button id="select-date-mode" fill="clear" class="mode-option-btn" @click="handleDateClick">
            <div :class="['radio-circle', { checked: selectionMode === 'date' }]">
              <div class="inner-dot" v-if="selectionMode === 'date'"></div>
            </div>
            <span class="mode-label">Par période</span>
          </ion-button>
        </div>

        <!-- Date range selectors -->
        <div v-if="selectionMode === 'date'" class="range-selector-container">
          <div class="date-picker-item">
            <span class="picker-label">Du :</span>
            <ion-datetime-button datetime="sales-start-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="sales-start-date" presentation="date" v-model="startDate" @ionChange="fetchSales" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
          <div class="date-picker-item">
            <span class="picker-label">Au :</span>
            <ion-datetime-button datetime="sales-end-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="sales-end-date" presentation="date" v-model="endDate" @ionChange="fetchSales" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
        </div>
      </div>



      <!-- 2. Date Navigation Bar (Only for Year/Month mode) -->
      <div v-if="selectionMode === 'year'" class="date-nav-bar">
        <ion-button id="prev-month-btn" fill="clear" @click="prevMonth" class="nav-btn">
          <ion-icon slot="icon-only" :icon="chevronBack" color="light"></ion-icon>
        </ion-button>
        <div class="date-display">
          {{ currentMonthName }} {{ currentYear }}
        </div>
        <ion-button id="next-month-btn" fill="clear" @click="nextMonth" class="nav-btn">
          <ion-icon slot="icon-only" :icon="chevronForward" color="light"></ion-icon>
        </ion-button>
      </div>

      <!-- 3. Monthly/Daily Revenue Summary -->
      <div class="revenue-summary">
        {{ selectionMode === 'date' ? 'Recette du jour :' : 'Recette du mois :' }} 
        <span class="amount">{{ money(monthlyTotal) }} BIF</span>
      </div>

      <!-- 4. Table Header -->
      <div class="table-header">
        <div class="col article-col italic">Article</div>
        <div class="col qty-col italic">Qt</div>
        <div class="col total-col italic">S.Total</div>
      </div>

      <!-- 5. Sales List -->
      <div class="sales-list-container">
        <div v-for="sale in filteredSales" :key="sale.id" class="sale-row">
          <div class="col article-col">
            <div class="art-info">
              <div class="art-name">{{ sale?.product?.name || '---' }}</div>
              <div class="art-cat">{{ getCategoryLabel(sale) }}</div>
            </div>
          </div>
          <div class="col qty-col">{{ sale?.quantity || 0 }}</div>
          <div class="col total-col">{{ money(sale?.amount) }}</div>
        </div>

        <div v-if="filteredSales.length === 0" class="empty-state">
          Aucune vente pour cette période.
        </div>
      </div>

      <ion-progress-bar v-if="loading" type="indeterminate"></ion-progress-bar>
    </ion-content>

    <!-- Year Selection Popover (OUTSIDE ion-content) -->
    <div v-if="showYearList" class="year-popover-overlay" @click="showYearList = false">
      <div class="year-list-card" @click.stop>
        <div class="year-card-header">Sélectionner une année</div>
        <div v-for="year in years" :key="year" 
             :class="['year-item', { 'year-item-active': year === currentYear }]" 
             @click="selectYear(year)">
          {{ year }}
        </div>
      </div>
    </div>


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
  IonSpinner,
  IonSelect,
  IonSelectOption,
  IonItem,
  IonDatetimeButton,
  IonModal,
  IonDatetime,
  IonLabel,
  IonBackButton,
  toastController
} from '@ionic/vue';
import { 
  arrowBackOutline, 
  chevronBack, 
  chevronForward, 
  calendarOutline, 
  refreshCircleOutline,
  downloadOutline 
} from 'ionicons/icons';
import * as XLSX from 'xlsx';
import { saveWorkbook } from '../../utils/exportExcel';
import { salesService } from '../../services/api/sales';
import { categoriesService } from '../../services/api/categories';
import globalMixins from '../../composables/mixins';

/**
 * Composant SalesList
 * - Gère l'interface et la logique métier de Sales List.
 */
export default {
  mixins: [globalMixins],
  name: 'SalesList',
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
    IonSpinner,
    IonSelect,
    IonSelectOption,
    IonItem,
    IonDatetimeButton,
    IonModal,
    IonDatetime,
    IonLabel,
    IonBackButton
  },
  data() {
    return {
      arrowBackOutline,
      chevronBack,
      chevronForward,
      calendarOutline,
      refreshCircleOutline,
      downloadOutline,
      selectionMode: 'year',
      currentDate: new Date(),
      startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
      products: [],
      categories: [],
      keyword: '',
      sales: [],
      loading: false,
      monthlyTotal: 0,
      showYearList: false,
      showInlineCalendar: false,
      years: Array.from({ length: 11 }, (_, i) => 2026 + i),
      shop: this.$store.state.shop
    };
  },
  computed: {
    shopId() {
      return this.$store.state.shop?.id || this.shop?.id;
    },
    currentMonthName() {
      const months = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
      ];
      return months[this.currentDate.getMonth()];
    },
    currentYear() {
      return this.currentDate.getFullYear();
    },
    filteredSales() {
      return this.sales || [];
    },
    isReadOnly() {
      return this.$route.query.readonly === '1';
    }
  },
  ionViewDidEnter() {
    // Initialiser l'aide contextuelle pour la liste des ventes
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Historique des Ventes',
      description: 'C\'est ici que vous suivez tout votre chiffre d\'affaires. Chaque ligne représente une transaction client avec le détail des produits vendus.',
      elements: [
        { label: 'Ticket de Caisse', type: 'Liste', desc: 'Chaque ligne représente une transaction. Cliquez sur une ligne si vous voulez voir le détail des produits vendus.' },
        { label: 'Télécharger', type: 'Bouton', desc: 'Génère un export Excel de vos ventes pour votre comptabilité.' }
      ],
      faq: [
        { question: 'C\'est quoi le Chiffre d\'Affaires ?', answer: 'Le Chiffre d\'Affaires (Ventes Totales) représente tout l\'argent reçu de vos clients, avant d\'avoir payé vos fournisseurs ou vos charges.' },
        { question: 'Comment annuler une vente ?', answer: 'Pour l\'instant, une vente enregistrée est définitive dans les journaux pour des raisons de sécurité de caisse. Il faut faire une régularisation manuelle si nécessaire.' }
      ]
    });
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchSales();
    this.fetchCategories();
  },

  ionViewWillEnter() {
    this.fetchSales();
  },
  methods: {
    removeFocus() {
      if (document.activeElement) {
        document.activeElement.blur();
      }
    },
    formatDateDay(date) {
      if (!date) return "";
      const d = new Date(date);
      const day = String(d.getDate()).padStart(2, '0');
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const year = d.getFullYear();
      return `${day}/${month}/${year}`;
    },
    handleYearClick() {
      if (this.selectionMode === 'year') {
        this.showYearList = !this.showYearList;
      } else {
        this.selectionMode = 'year';
        this.showYearList = true;
        this.fetchSales();
      }
    },
    handleDateClick() {
      if (this.selectionMode === 'date') {
        this.toggleInlineCalendar();
      } else {
        this.selectionMode = 'date';
        this.showYearList = false;
        this.showInlineCalendar = true;
        this.fetchSales(true);
      }
    },
    toggleInlineCalendar() {
      this.showInlineCalendar = !this.showInlineCalendar;
    },
    onInlineDateSelected(ev) {
      const val = ev.detail.value;
      if (val) {
        // Ionic datetime value can be ISO string
        const datePart = val.split('T')[0];
        this.currentDate = new Date(datePart + 'T00:00:00');
        this.showInlineCalendar = false;
        this.fetchSales(true);
      }
    },
    selectYear(year) {
      this.currentDate = new Date(year, this.currentDate.getMonth(), 1);
      this.showYearList = false;
      this.fetchSales();
    },
    toInputDateString(date) {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, '0');
      const d = String(date.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    },
    async fetchSales() {
      if (!this.shopId) {
        console.warn("[SalesList] fetchSales avorté : shopId manquant.", { shop: this.shop, store: this.$store.state.shop });
        return;
      }
      this.loading = true;

      // Helper pour formater en YYYY-MM-DD local
      const toLocalISO = (date) => {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
      };

      let firstDay, lastDay;
      if (this.selectionMode === 'date') {
        firstDay = this.startDate;
        lastDay = this.endDate;
      } else {
        const y = this.currentDate.getFullYear();
        const m = this.currentDate.getMonth();
        firstDay = toLocalISO(new Date(y, m, 1));
        lastDay = toLocalISO(new Date(y, m + 1, 0));
      }

      try {
        const res = await salesService.getSales(this.shopId, { 
          created_at__gte: firstDay, 
          created_at__lte: lastDay,
          no_pagination: 'true'
        });
        this.sales = res.data.results || res.data || [];
        this.monthlyTotal = this.sales.reduce((sum, s) => sum + (parseFloat(s.amount) || 0), 0);
      } catch (err) {
        this.errorOrRefresh(err, () => this.fetchSales());
      } finally {
        this.loading = false;
      }
    },
    async exportToExcel() {
       if (this.sales.length === 0) {
         this.showToastMsg('Aucune donnée à exporter', 'warning');
         return;
       }

       const data = this.sales.map(s => ({
         'Date': s.created_at ? s.created_at.split('T')[0] : '-',
         'Produit': s?.product?.name || '---',
         'Prix Unitaire': parseFloat(s.price),
         'Quantité': parseInt(s.quantity),
         'Sous-Total (BIF)': parseFloat(s.amount)
       }));

       const ws = XLSX.utils.json_to_sheet(data);
       const wb = XLSX.utils.book_new();
       XLSX.utils.book_append_sheet(wb, ws, "Ventes");
       
       const fileName = `Ventes_${this.startDate}_au_${this.endDate}.xlsx`;
       await saveWorkbook(wb, fileName);
       this.showToastMsg('Export Excel réussi !', 'success');
    },

    prevMonth() {
      const d = new Date(this.currentDate);
      d.setMonth(d.getMonth() - 1);
      this.currentDate = d;
      this.fetchSales();
    },
    nextMonth() {
      const d = new Date(this.currentDate);
      d.setMonth(d.getMonth() + 1);
      this.currentDate = d;
      this.fetchSales();
    },
    money(val) {
      if (!val) return "0";
      return parseFloat(val).toLocaleString('fr-FR');
    },
    async fetchCategories() {
      try {
        const res = await categoriesService.getCategories();
        this.categories = res.data.results || res.data || [];
      } catch (err) {
        console.error("[SalesList] Erreur catégories:", err);
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

.selection-row {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  padding: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.radio-circle {
  width: 20px;
  height: 20px;
  border: 2px solid #94a3b8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.radio-circle.checked {
  border-color: var(--ion-color-secondary);
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

.inner-dot {
  width: 10px;
  height: 10px;
  background-color: var(--ion-color-secondary);
  border-radius: 50%;
}

.mode-option-btn {
  --padding-start: 12px;
  --padding-end: 12px;
  text-transform: none;
  height: 44px;
  color: #475569;
  font-weight: 700;
  font-size: 0.9rem;
}

.mode-label {
  margin-left: 8px;
}

.range-selector-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 12px;
  background: white;
  margin: 10px 12px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
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
  border: 1px solid #cbd5e1;
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

.date-nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  margin: 0 12px 16px 12px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  height: 56px;
}

.nav-btn {
  --color: #64748b;
  margin: 0;
  height: 100%;
  width: 56px;
}

.date-display {
  flex: 1;
  text-align: center;
  font-weight: 800;
  font-size: 1.1rem;
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

.amount {
  font-weight: 800;
  color: var(--ion-color-secondary);
}

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

.col { display: flex; align-items: center; min-width: 0; }
.article-col { flex: 2; overflow: hidden; }
.qty-col { flex: 0.5; justify-content: center; white-space: nowrap; flex-shrink: 0; }
.total-col { flex: 1.2; justify-content: flex-end; white-space: nowrap; flex-shrink: 0; }

.sales-list-container {
  padding: 0 12px 30px 12px;
}

.sale-row {
  display: flex;
  padding: 18px 16px;
  background: white;
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  margin: 0 12px 12px 12px;
  color: #1e293b;
  font-size: 0.95rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  animation: fadeInUp 0.4s ease-out both;
  align-items: center;
}

.art-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.art-name {
  font-weight: 800;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.art-cat {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
  margin-top: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  font-weight: 600;
}

.year-popover-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.year-list-card {
  background: white;
  width: 280px;
  max-height: 400px;
  border-radius: 24px;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.year-card-header {
  padding: 20px;
  font-weight: 800;
  color: #0f172a;
  text-align: center;
  border-bottom: 1.5px solid #f1f5f9;
}

.year-item {
  padding: 14px;
  text-align: center;
  font-weight: 600;
  color: #475569;
  border-bottom: 1px solid #f1f5f9;
}

.year-item:active { background: #f8fafc; }
.year-item-active { color: var(--ion-color-secondary); font-weight: 800; background: #f0f7ff; }

@media (max-width: 480px) {
  .table-header {
    padding: 10px 10px;
    margin: 0 6px;
    font-size: 0.7rem;
  }
  .sales-list-container {
    padding: 0 6px 30px 6px;
  }
  .sale-row {
    padding: 12px 10px;
    margin: 0 6px 8px 6px;
    font-size: 0.85rem;
  }
  .art-name {
    font-size: 0.9rem;
  }
  .art-cat {
    font-size: 0.7rem;
  }
  .revenue-summary {
    padding: 12px;
    margin: 10px 6px;
    font-size: 1rem;
  }
  .selection-area {
    margin: 10px 6px;
  }
  .range-selector-container {
    padding: 10px 8px;
    gap: 8px;
  }
}
</style>