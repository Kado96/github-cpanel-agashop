<!--
  * @file ExpensesList.vue
  * @description Page pour la gestion de Expenses List.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-expenses" name="back-to-expenses" @click="$router.push({ name: isReadOnly ? 'expenses' : 'shop' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Historiques des Dépenses</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchExpenses">
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
            <ion-datetime-button datetime="expenses-start-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="expenses-start-date" presentation="date" v-model="startDate" @ionChange="fetchExpenses" locale="fr-FR"></ion-datetime>
            </ion-modal>
          </div>
          <div class="date-picker-item">
            <span class="picker-label">Au :</span>
            <ion-datetime-button datetime="expenses-end-date"></ion-datetime-button>
            <ion-modal :keep-contents-mounted="true" @didDismiss="removeFocus">
              <ion-datetime id="expenses-end-date" presentation="date" v-model="endDate" @ionChange="fetchExpenses" locale="fr-FR"></ion-datetime>
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

      <!-- 3. Monthly/Daily Total Summary -->
      <div class="revenue-summary">
        {{ selectionMode === 'date' ? 'Dépense du jour :' : 'Dépense du mois :' }} 
        <span class="amount red-text">{{ money(monthlyTotal) }} BIF</span>
      </div>

      <!-- 4. Table Header -->
      <div class="table-header">
        <div class="col article-col italic">Type / Description</div>
        <div class="col total-col italic">Montant</div>
      </div>

      <!-- 5. Expenses List -->
      <div class="sales-list-container">
        <template v-for="expense in expenses" :key="expense.id">
          <!-- Manageable mode with click options -->
          <div v-if="!isReadOnly" class="sale-row clickable-row" @click="openExpenseOptions(expense)">
            <div class="col article-col">
              <div class="art-info">
                <div class="art-cat">{{ expense.expense_type_display }}</div>
                <div class="art-desc">{{ expense.description }}</div>
              </div>
            </div>
            <div class="col total-col red-text">
              <span class="price-val">- {{ money(expense.amount) }}</span>
              <ion-icon class="options-icon" :icon="ellipsisVerticalOutline"></ion-icon>
            </div>
          </div>

          <!-- Simple row for Read-only mode (Stats) -->
          <div v-else class="sale-row">
            <div class="col article-col">
              <div class="art-info">
                <div class="art-cat">{{ expense.expense_type_display }}</div>
                <div class="art-desc">{{ expense.description }}</div>
              </div>
            </div>
            <div class="col total-col red-text">- {{ money(expense.amount) }}</div>
          </div>
        </template>

        <div v-if="expenses.length === 0 && !loading" class="empty-state">
          Aucune dépense pour cette période.
        </div>
      </div>

      <ion-progress-bar v-if="loading" type="indeterminate"></ion-progress-bar>
    </ion-content>

    <!-- Floating Action Button for Adding Expenses (Hidden in Read-only) -->
    <ion-fab v-if="!isReadOnly && !loading" vertical="bottom" horizontal="end" slot="fixed" style="bottom: 72px !important; transform: none !important; z-index: 10001 !important;">
      <ion-fab-button color="danger" @click="openCreateModal">
        <ion-icon :icon="addOutline"></ion-icon>
      </ion-fab-button>
    </ion-fab>

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
  IonLabel,
  IonFab,
  IonFabButton,
  IonItemSliding,
  IonItemOptions,
  IonItemOption,
  IonInput,
  IonDatetimeButton,
  IonModal,
  modalController,
  alertController,
  toastController,
  actionSheetController
} from '@ionic/vue';
import { 
  arrowBackOutline, 
  chevronBack, 
  chevronForward, 
  refreshCircleOutline, 
  addOutline,
  createOutline,
  trashOutline,
  ellipsisVerticalOutline,
  closeOutline,
  downloadOutline
} from 'ionicons/icons';
import * as XLSX from 'xlsx';
import { saveWorkbook } from '../../utils/exportExcel';
import { expensesService } from '../../services/api/expenses';
import ExpenseForm from '../../components/shop/ExpenseForm.vue';

/**
 * Composant ExpensesList
 * - Gère l'interface et la logique métier de Expenses List.
 */
export default {
  name: 'ExpensesList',
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
    IonLabel,
    IonFab,
    IonFabButton,
    IonItemSliding,
    IonItemOptions,
    IonItemOption,
    IonInput,
    IonDatetimeButton,
    IonModal
  },
  data() {
    return {
      arrowBackOutline,
      chevronBack,
      chevronForward,
      refreshCircleOutline,
      addOutline,
      createOutline,
      trashOutline,
      ellipsisVerticalOutline,
      closeOutline,
      downloadOutline,
      selectionMode: 'year',
      currentDate: new Date(),
      startDate: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
      endDate: new Date().toISOString().split('T')[0],
      expenses: [],
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
    isReadOnly() {
      return this.$route.query.readonly === 'true';
    }
  },
  ionViewDidEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Registre des Dépenses',
      description: 'C\'est ici que vous notez tout ce qui sort de la caisse et qui n\'est pas un achat de marchandise (loyer, transport, repas...). Ces charges réduisent votre bénéfice net.',
      elements: [
        { label: 'Sélecteur de période', type: 'Filtre', desc: 'Affiche les dépenses sur la plage sélectionnée.' },
        { label: 'Total des Dépenses', type: 'Indicateur', desc: 'La somme de toutes vos charges sur la période.' },
        { label: 'Bouton (+)', type: 'Bouton Flottant', desc: 'Cliquez ici pour créer une nouvelle dépense.' },
        { label: 'Télécharger', type: 'Bouton', desc: 'Exporte le registre des charges en Excel.' }
      ],
      faq: [
        { question: 'Quelle est la différence entre Dépense et Achat (Stock) ?', answer: 'Un Achat de marchandise augmente votre stock pour être revendu. Une Dépense est une charge "perdue" (comme l\'électricité ou le transport) nécessaire pour faire tourner la boutique.' },
        { question: 'Comment supprimer une dépense ?', answer: 'Glissez la dépense vers la gauche pour faire apparaître le bouton rouge "Supprimer".' },
        { question: 'Pourquoi noter mes dépenses ?', answer: 'Si vous ne notez que vos ventes, AgaShop vous montrera un bénéfice trop élevé. Noter vos dépenses permet de voir ce qu\'il vous reste réellement en poche.' },
        { question: 'Quelle catégorie choisir ?', answer: 'Utilisez des noms clairs comme "Transport marchandise" ou "Loyer" pour mieux analyser vos postes de coûts.' }
      ]
    });
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchExpenses();
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
        this.fetchExpenses();
      }
    },
    handleDateClick() {
      if (this.selectionMode === 'date') {
        this.toggleInlineCalendar();
      } else {
        this.selectionMode = 'date';
        this.showYearList = false;
        this.showInlineCalendar = true;
        this.fetchExpenses(true);
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
        this.fetchExpenses(true);
      }
    },
    selectYear(year) {
      this.currentDate = new Date(year, this.currentDate.getMonth(), 1);
      this.showYearList = false;
      this.fetchExpenses();
    },
    toInputDateString(date) {
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, '0');
      const d = String(date.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    },
    async fetchExpenses() {
      if (!this.shopId) return;
      this.loading = true;
      this.monthlyTotal = 0;

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
        const res = await expensesService.getExpenses(this.shopId, { 
          expense_date__gte: firstDay, 
          expense_date__lte: lastDay,
          created_at__gte: firstDay,
          created_at__lte: lastDay,
          page_size: 1000
        });
        const rawExpenses = res.data.results || res.data || [];
        // Sécurité : filtrage local si le backend ignore les paramètres de date
        this.expenses = rawExpenses.filter(e => {
          const d = e.expense_date?.split('T')[0] || e.created_at?.split('T')[0];
          return d && d >= firstDay && d <= lastDay;
        });
        this.monthlyTotal = this.expenses.reduce((sum, e) => sum + (parseFloat(e.amount) || 0), 0);
      } catch (err) {
        console.error("[ExpensesList] Erreur:", err);
      } finally {
        this.loading = false;
      }
    },
    async exportToExcel() {
       if (this.expenses.length === 0) {
         this.showToastMsg('Aucune donnée à exporter', 'warning');
         return;
       }

       const data = this.expenses.map(e => ({
         'Date': e.expense_date,
         'Type': e.expense_type_display,
         'Description': e.description,
         'Montant (BIF)': parseFloat(e.amount),
         'Référence': e.receipt_number || '-'
       }));

       const ws = XLSX.utils.json_to_sheet(data);
       const wb = XLSX.utils.book_new();
       XLSX.utils.book_append_sheet(wb, ws, "Dépenses");
       
       const fileName = `Depenses_${this.startDate}_au_${this.endDate}.xlsx`;
       await saveWorkbook(wb, fileName);
       this.showToastMsg('Export Excel réussi !', 'success');
    },
    prevMonth() {
      const d = new Date(this.currentDate);
      d.setMonth(d.getMonth() - 1);
      this.currentDate = d;
      this.fetchExpenses();
    },
    nextMonth() {
      const d = new Date(this.currentDate);
      d.setMonth(d.getMonth() + 1);
      this.currentDate = d;
      this.fetchExpenses();
    },
    money(val) {
      if (!val) return "0";
      return parseFloat(val).toLocaleString('fr-FR');
    },
    async openCreateModal() {
      const modal = await modalController.create({
        component: ExpenseForm,
        componentProps: { shopId: this.shopId, mode: 'create' }
      });
      await modal.present();
      const { data, role } = await modal.onDidDismiss();
      if (role === 'confirm') {
        this.fetchExpenses();
        this.showToastMsg('Dépense ajoutée.', 'success');
      }
    },
    async openEditModal(expense) {
      const modal = await modalController.create({
        component: ExpenseForm,
        componentProps: { shopId: this.shopId, mode: 'edit', expenseProp: expense }
      });
      await modal.present();
      const { data, role } = await modal.onDidDismiss();
      if (role === 'confirm') {
        this.fetchExpenses();
        this.showToastMsg('Dépense mise à jour.', 'success');
      }
    },
    async openExpenseOptions(expense) {
      const actionSheet = await actionSheetController.create({
        header: 'Options de la dépense',
        buttons: [
          {
            text: 'Modifier',
            icon: this.createOutline,
            role: 'edit'
          },
          {
            text: 'Supprimer',
            icon: this.trashOutline,
            role: 'destructive'
          },
          {
            text: 'Annuler',
            icon: this.closeOutline,
            role: 'cancel'
          }
        ]
      });
      await actionSheet.present();
      
      const { role } = await actionSheet.onDidDismiss();
      if (role === 'edit') {
        this.openEditModal(expense);
      } else if (role === 'destructive') {
        this.confirmDelete(expense);
      }
    },
    async confirmDelete(expense) {
      const alert = await alertController.create({
        header: 'Supprimer',
        message: 'Voulez-vous vraiment supprimer cette dépense ?',
        buttons: [
          { text: 'Annuler', role: 'cancel' },
          {
            text: 'Supprimer',
            role: 'destructive'
          }
        ]
      });
      await alert.present();
      
      const { role } = await alert.onDidDismiss();
      if (role === 'destructive') {
        this.deleteExpense(expense.id);
      }
    },
    async deleteExpense(id) {
      try {
        await expensesService.deleteExpense(id);
        this.fetchExpenses();
        this.showToastMsg('Dépense supprimée.', 'success');
      } catch (err) {
        console.error("[ExpensesList] Erreur delete:", err);
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

.range-selector-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 12px;
  background: white;
  margin: 10px 12px;
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

.red-text { color: #ef4444; }
.amount { font-weight: 800; }

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
.total-col { flex: 1.5; justify-content: flex-end; align-items: center; gap: 8px; white-space: nowrap; flex-shrink: 0; }
.options-icon { font-size: 20px; color: #64748b; }
.price-val { font-weight: 800; white-space: nowrap; }

.clickable-row { cursor: pointer; transition: background-color 0.2s; }
.clickable-row:active { background-color: #f8fafc; }

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
  color: #1e293b;
  font-size: 0.95rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  animation: fadeInUp 0.4s ease-out both;
  align-items: center;
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

.no-border { border: none; box-shadow: none; margin-bottom: 0; }

.exp-type { font-weight: 800; color: #0f172a; font-size: 1rem; }
.exp-desc { font-size: 0.85rem; color: #64748b; font-weight: 600; margin-top: 2px; }

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

.expense-slide-item {
  --background: transparent;
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  margin-bottom: 10px;
  overflow: hidden;
}

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.art-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
  flex: 1;
}

.art-cat {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--ion-color-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: rgba(37, 99, 235, 0.08);
  padding: 2px 8px;
  border-radius: 6px;
  display: inline-block;
  width: fit-content;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.art-desc {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

ion-fab {
  bottom: 72px !important;
  right: 16px !important;
  z-index: 10001 !important;
}

@media (max-width: 480px) {
  .table-header {
    padding: 10px 10px;
    margin: 0 6px;
    font-size: 0.7rem;
  }
  .sales-list-container {
    padding: 0 6px 60px 6px;
  }
  .sale-row {
    padding: 12px 10px;
    margin: 0 6px 8px 6px;
    font-size: 0.85rem;
  }
  .art-desc {
    font-size: 0.95rem;
  }
  .art-cat {
    font-size: 0.75rem;
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
