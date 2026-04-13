<!--
  * @file ProfitsList.vue
  * @description Page pour la gestion de Profits List.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-profits" name="back-to-profits" @click="$router.push({ name: 'profits' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Historiques des Bénéfices</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchData">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="history-content">
      <!-- 1. Selection Mode Area -->
      <div class="selection-area">
        <div class="selection-row">
          <ion-button fill="clear" class="mode-option-btn" @click="handleYearClick">
            <div :class="['radio-circle', { checked: selectionMode === 'year' }]">
              <div class="inner-dot" v-if="selectionMode === 'year'"></div>
            </div>
            <span class="mode-label">Sélectionner une année</span>
          </ion-button>
          
          <ion-button fill="clear" class="mode-option-btn" @click="handleDateClick">
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
            <ion-datetime-button datetime="profits-start-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="profits-start-date" presentation="date" v-model="startDate" @ionChange="fetchData" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
          <div class="date-picker-item">
            <span class="picker-label">Au :</span>
            <ion-datetime-button datetime="profits-end-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="profits-end-date" presentation="date" v-model="endDate" @ionChange="fetchData" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
        </div>
      </div>

      <!-- 2. Date Navigation Bar -->
      <div v-if="selectionMode === 'year'" class="date-nav-bar">
        <ion-button fill="clear" @click="prevMonth" class="nav-btn">
          <ion-icon slot="icon-only" :icon="chevronBack" color="light"></ion-icon>
        </ion-button>
        <div class="date-display">
          {{ currentMonthName }} {{ currentYear }}
        </div>
        <ion-button fill="clear" @click="nextMonth" class="nav-btn">
          <ion-icon slot="icon-only" :icon="chevronForward" color="light"></ion-icon>
        </ion-button>
      </div>

      <!-- 3. Profit Summary Cards -->
      <div class="profit-summary-container ion-padding">
        <ion-row>
          <ion-col size="12">
            <ion-card class="summary-card v-card">
              <ion-card-content>
                <div class="summary-label">Marge sur Ventes</div>
                <div class="summary-value green-text">{{ money(totalSalesProfit) }} BIF</div>
              </ion-card-content>
            </ion-card>
          </ion-col>
          <ion-col size="12">
            <ion-card class="summary-card d-card">
              <ion-card-content>
                <div class="summary-label">Total Dépenses</div>
                <div class="summary-value red-text">{{ money(totalExpenses) }} BIF</div>
              </ion-card-content>
            </ion-card>
          </ion-col>
          <ion-col size="12">
            <ion-card class="summary-card b-card">
              <ion-card-content>
                <div class="summary-label">Bénéfice Net</div>
                <div class="summary-value" :class="netProfit >= 0 ? 'blue-text' : 'red-text'">
                  {{ netProfit >= 0 ? '' : '-' }} {{ money(Math.abs(netProfit)) }} BIF
                </div>
              </ion-card-content>
            </ion-card>
          </ion-col>
        </ion-row>
      </div>

      <!-- 4. Table Header -->
      <div class="table-header">
        <div class="col item-col italic">Type</div>
        <div class="col val-col italic">Journalier</div>
      </div>

      <!-- 5. Comparison List -->
      <div class="sales-list-container">
        <div class="sale-row">
          <div class="col item-col">💰 Marge sur Ventes</div>
          <div class="col val-col green-text">+ {{ money(totalSalesProfit) }}</div>
        </div>
        <div class="sale-row">
          <div class="col item-col">💸 Dépenses</div>
          <div class="col val-col red-text">- {{ money(totalExpenses) }}</div>
        </div>
        <div class="sale-row profit-highlight">
          <div class="col item-col">📈 Bénéfice Net</div>
          <div class="col val-col" :class="netProfit >= 0 ? 'blue-text' : 'red-text'">
            {{ netProfit >= 0 ? '+' : '-' }} {{ money(Math.abs(netProfit)) }}
          </div>
        </div>
      </div>

      <ion-progress-bar v-if="loading" type="indeterminate"></ion-progress-bar>
    </ion-content>

    <!-- Year Selection Popover -->
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
  IonDatetime,
  IonRow,
  IonCol,
  IonCard,
  IonCardContent,
  toastController,
  IonInput,
  IonDatetimeButton,
  IonModal
} from '@ionic/vue';
import { 
  arrowBackOutline, 
  chevronBack, 
  chevronForward, 
  refreshCircleOutline,
  downloadOutline 
} from 'ionicons/icons';
import * as XLSX from 'xlsx';
import { salesService } from '../../services/api/sales';
import { expensesService } from '../../services/api/expenses';
import { suppliesService } from '../../services/api/supplies';

/**
 * Composant ProfitsList
 * - Gère l'interface et la logique métier de Profits List.
 */
export default {
  name: 'ProfitsList',
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
    IonDatetime,
    IonRow,
    IonCol,
    IonCard,
    IonCardContent,
    IonDatetimeButton,
    IonModal
  },
  data() {
    return {
      arrowBackOutline,
      chevronBack,
      chevronForward,
      refreshCircleOutline,
      downloadOutline,
      selectionMode: 'year',
      currentDate: new Date(),
      startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
      totalSales: 0,
      totalExpenses: 0,
      totalSalesProfit: 0,
      loading: false,
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
    netProfit() {
      // Bénéfice = Marge réelle sur ventes - Dépenses générales
      return this.totalSalesProfit - this.totalExpenses;
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
    isReadOnly() {
      return this.$route.query.readonly === '1';
    }
  },
  ionViewDidEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Analyse de la Rentabilité Net',
      description: 'Cet écran est le juge de paix de votre commerce. Il calcule ce qu\'il vous reste réellement en poche après avoir payé vos fournisseurs et vos charges d\'exploitation.',
      elements: [
        { label: 'Chiffre d\'Affaires', type: 'Encaissé', desc: 'Le montant total brut reçu de vos clients sur la période.' },
        { label: 'Marge sur Ventes', type: 'Profit Brut', desc: 'La différence entre vos prix de vente et vos prix d\'achat. C\'est ce que le commerce vous rapporte avant vos frais.' },
        { label: 'Dépenses', type: 'Charges', desc: 'Le total de vos frais fixes (loyer, électricité, sacs, transport) notés dans le menu Dépenses.' },
        { label: 'Bénéfice Net', type: 'Reste à vivre', desc: 'Le résultat final : Marge - Dépenses. C\'est l\'argent qui vous appartient réellement.' }
      ],
      faq: [
        { question: 'Pourquoi mon bénéfice est négatif ?', answer: 'Cela arrive si vos dépenses (charges) sont plus élevées que la marge générée par vos ventes. Vérifiez si vous n\'avez pas eu des frais exceptionnels ce mois-ci.' },
        { question: 'Puis-je changer la période ?', answer: 'Oui, utilisez les flèches ou le calendrier pour analyser vos profits par semaine, par mois ou par année.' }
      ]
    });
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchData();
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
        this.fetchData();
      }
    },
    handleDateClick() {
      if (this.selectionMode === 'date') {
        this.toggleInlineCalendar();
      } else {
        this.selectionMode = 'date';
        this.showYearList = false;
        this.showInlineCalendar = true;
        this.fetchData(true);
      }
    },
    toggleInlineCalendar() {
      this.showInlineCalendar = !this.showInlineCalendar;
    },
    onInlineDateSelected(ev) {
      const val = ev.detail.value;
      if (val) {
        const datePart = val.split('T')[0];
        this.currentDate = new Date(datePart + 'T00:00:00');
        this.showInlineCalendar = false;
        this.fetchData(true);
      }
    },
    selectYear(year) {
      this.currentDate = new Date(year, this.currentDate.getMonth(), 1);
      this.showYearList = false;
      this.fetchData();
    },
    toInputDateString(date) {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, '0');
      const d = String(date.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    },
    async fetchData() {
      if (!this.shopId) return;
      this.loading = true;
      this.totalSales = 0;
      this.totalExpenses = 0;
      this.totalSalesProfit = 0;

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
        const [salesRes, expRes, suppRes] = await Promise.all([
          salesService.getSales(this.shopId, { 
            created_at__gte: firstDay, 
            created_at__lte: lastDay,
            limit: 1000
          }),
          expensesService.getExpenses(this.shopId, {
            expense_date__gte: firstDay,
            expense_date__lte: lastDay,
            created_at__gte: firstDay, 
            created_at__lte: lastDay,
            limit: 1000
          }),
          suppliesService.getSupplies(this.shopId, {
            created_at__gte: firstDay,
            created_at__lte: lastDay,
            limit: 1000
          })
        ]);

        const sales = salesRes.data.results || salesRes.data || [];
        const rawExp = expRes.data.results || expRes.data || [];
        const exp = rawExp.filter(e => {
          const d = e.expense_date?.split('T')[0] || e.created_at?.split('T')[0];
          return d && d >= firstDay && d <= lastDay;
        });

        const supp = suppRes.data.results || suppRes.data || [];

        this.totalSales = sales.reduce((sum, s) => sum + (parseFloat(s.amount) || 0), 0);
        this.totalExpenses = exp.reduce((sum, e) => sum + (parseFloat(e.amount) || 0), 0);

        // Calcul de la marge réelle sur les ventes (Prix Vente Total - Coût Achat Total)
        this.totalSalesProfit = sales.reduce((sum, s) => {
          const qty = parseFloat(s.quantity) || 0;
          const totalAmount = parseFloat(s.amount) || 0; // Montant TOTAL de la ligne de vente
          const buyPrice = parseFloat(s.buy_price || s.product?.buy_price) || 0; // Prix unitaire d'achat
          const profit = totalAmount - (buyPrice * qty);
          return sum + profit;
        }, 0);
      } catch (err) {
        console.error("[ProfitsList] Erreur:", err);
      } finally {
        this.loading = false;
      }
    },
    exportToExcel() {
       const data = [
         { 'Type': '💰 Marge sur Ventes', 'Montant (BIF)': this.totalSalesProfit },
         { 'Type': '💸 Dépenses', 'Montant (BIF)': this.totalExpenses },
         { 'Type': '📈 Bénéfice Net', 'Montant (BIF)': this.netProfit }
       ];

       const ws = XLSX.utils.json_to_sheet(data);
       const wb = XLSX.utils.book_new();
       XLSX.utils.book_append_sheet(wb, ws, "Bénéfices");
       
       const fileName = `Benefices_${this.startDate}_au_${this.endDate}.xlsx`;
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
    prevMonth() {
      const d = new Date(this.currentDate);
      d.setMonth(d.getMonth() - 1);
      this.currentDate = d;
      this.fetchData();
    },
    nextMonth() {
      const d = new Date(this.currentDate);
      d.setMonth(d.getMonth() + 1);
      this.currentDate = d;
      this.fetchData();
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
  --background: #f1f5f9;
}

.selection-area {
  padding: 16px 12px;
}

.selection-row {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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

.mode-label { margin-left: 8px; }

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
  border-color: var(--ion-color-secondary);
}

.date-nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  margin: 0 12px 16px 12px;
  border-radius: 16px;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  height: 56px;
}

.nav-btn { --color: #64748b; margin: 0; height: 100%; width: 56px; }

.date-display {
  flex: 1;
  text-align: center;
  font-weight: 800;
  font-size: 1.1rem;
  color: #0f172a;
}

.profit-summary-container { 
  padding: 0 12px;
  animation: fadeInUp 0.5s ease-out;
}

.summary-card {
  margin: 0 0 12px 0;
  border-radius: 20px;
  background: white;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 16px;
}

.summary-label {
  font-size: 0.8rem;
  color: #475569;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 1.4rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.orange-text { color: #f59e0b; }
.red-text { color: #ef4444; }
.blue-text { color: #2563eb; }
.green-text { color: #166534; }

.a-card { border-left: 8px solid #f59e0b; }
.d-card { border-left: 8px solid #ef4444; }
.v-card { border-left: 8px solid #166534; }
.b-card { border-left: 8px solid #2563eb; }

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
  margin: 10px 12px 0 12px;
}

.col { display: flex; align-items: center; }
.item-col { flex: 2; }
.val-col { flex: 1.5; justify-content: flex-end; }

.sales-list-container { padding: 0 12px 30px 12px; }

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

.profit-highlight { background: #f0f7ff; border-color: #bfdbfe; }

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

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
</style>
