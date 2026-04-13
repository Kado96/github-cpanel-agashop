<!--
  * @file ExpenseForm.vue
  * @description Page pour la gestion de Expense Form.
  * @author Kora Agency
-->
<template>
  <ion-header class="ion-no-border">
    <ion-toolbar color="secondary">
      <ion-buttons slot="start">
        <ion-button id="expense-form-cancel-btn" name="back-button" @click="cancel">
          <ion-icon color="light" slot="icon-only" :icon="closeOutline"></ion-icon>
        </ion-button>
      </ion-buttons>
      <ion-title color="light">{{ mode === 'create' ? 'Nouvelle Dépense' : 'Modifier la Dépense' }}</ion-title>
      <ion-buttons slot="end">
        <ion-button @click="confirm" :disabled="!isValid">
          <ion-icon color="light" slot="icon-only" :icon="checkmarkOutline"></ion-icon>
        </ion-button>
      </ion-buttons>
    </ion-toolbar>
  </ion-header>

  <ion-content class="form-content ion-padding">
    <ion-grid fixed>
      <ion-row class="ion-justify-content-center">
        <ion-col size="12">
          <div class="form-container">
            <form @submit.prevent="confirm">
              <div class="input-card">
                <ion-item lines="none" class="custom-item">
                  <ion-label for="expense-type" position="stacked">Type de dépense</ion-label>
                  <ion-select 
                    id="expense-type"
                    name="expense_type"
                    v-model="formData.expense_type" 
                    placeholder="Sélectionnez un type" 
                    interface="action-sheet" 
                    class="custom-select"
                  >
                    <ion-select-option value="RENT">Loyer</ion-select-option>
                    <ion-select-option value="UTILITIES">Services publics (eau, élec.)</ion-select-option>
                    <ion-select-option value="SALARY">Salaires</ion-select-option>
                    <ion-select-option value="TRANSPORT">Transport</ion-select-option>
                    <ion-select-option value="MARKETING">Marketing/Publicité</ion-select-option>
                    <ion-select-option value="MAINTENANCE">Maintenance/Réparation</ion-select-option>
                    <ion-select-option value="SUPPLIES">Fournitures</ion-select-option>
                    <ion-select-option value="OTHER">Autre</ion-select-option>
                  </ion-select>
                </ion-item>
              </div>

              <div class="input-card">
                <ion-item lines="none" class="custom-item">
                  <ion-label for="expense-amount" position="stacked">Montant (BIF)</ion-label>
                  <ion-input 
                    id="expense-amount"
                    name="amount"
                    v-model.number="formData.amount" 
                    type="number" 
                    placeholder="Ex: 50 000" 
                    class="custom-input"
                    autocomplete="transaction-amount"
                  ></ion-input>
                </ion-item>
              </div>

              <div class="input-card">
                <ion-item lines="none" class="custom-item">
                  <ion-label for="expense-date" position="stacked">Date</ion-label>
                  <ion-input 
                    id="expense-date"
                    name="expense_date"
                    v-model="formData.expense_date" 
                    type="date" 
                    class="custom-input"
                  ></ion-input>
                </ion-item>
              </div>

              <div class="input-card">
                <ion-item lines="none" class="custom-item">
                  <ion-label for="expense-description" position="stacked">Description / Motif</ion-label>
                  <ion-textarea 
                    id="expense-description"
                    name="description"
                    v-model="formData.description" 
                    placeholder="Détails de la dépense..." 
                    rows="3" 
                    class="custom-input"
                  ></ion-textarea>
                </ion-item>
              </div>

              <div class="input-card">
                <ion-item lines="none" class="custom-item">
                  <ion-label for="expense-receipt" position="stacked">Référence / Reçu #</ion-label>
                  <ion-input 
                    id="expense-receipt"
                    name="receipt_number"
                    v-model="formData.receipt_number" 
                    placeholder="Optionnel" 
                    class="custom-input"
                  ></ion-input>
                </ion-item>
              </div>

              <div class="ion-padding-top action-area">
                <ion-button expand="block" shape="round" class="submit-btn" :disabled="!isValid" @click="confirm">
                  {{ mode === 'create' ? 'Enregistrer la Dépense' : 'Mettre à jour' }}
                </ion-button>
              </div>
            </form>
          </div>
        </ion-col>
      </ion-row>
    </ion-grid>
  </ion-content>
</template>

<script>
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonIcon,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonSelect,
  IonSelectOption,
  IonTextarea,
  IonGrid,
  IonRow,
  IonCol,
  modalController
} from '@ionic/vue';
import { closeOutline, checkmarkOutline } from 'ionicons/icons';
import { expensesService } from '../../services/api/expenses';

/**
 * Composant ExpenseForm
 * - Gère l'interface et la logique métier de Expense Form.
 */
export default {
  components: {
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonIcon,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonSelect,
    IonSelectOption,
    IonTextarea,
    IonGrid,
    IonRow,
    IonCol
  },
  props: {
    mode: { type: String, default: 'create' },
    expenseProp: { type: Object, default: () => null },
    shopId: { type: Number, required: true }
  },
  data() {
    return {
      closeOutline,
      checkmarkOutline,
      formData: {
        shop: this.shopId,
        expense_type: 'OTHER',
        amount: null,
        expense_date: new Date().toISOString().split('T')[0],
        description: '',
        receipt_number: ''
      }
    };
  },
  computed: {
    isValid() {
      return this.formData.amount > 0 && this.formData.expense_date;
    }
  },
  created() {
    if (this.mode === 'edit' && this.expenseProp) {
      this.formData = { ...this.expenseProp };
    }
  },
  methods: {
    cancel() {
      modalController.dismiss(null, 'cancel');
    },
    async confirm() {
      if (!this.isValid) return;

      try {
        let res;
        if (this.mode === 'create') {
          res = await expensesService.createExpense(this.formData);
        } else {
          res = await expensesService.updateExpense(this.formData.id, this.formData);
        }
        modalController.dismiss(res.data, 'confirm');
      } catch (err) {
        console.error("[ExpenseForm] Erreur:", err);
      }
    }
  }
};
</script>

<style scoped>
.form-content {
  --background: #f8faff;
  font-family: 'Inter', sans-serif;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding-top: 10px;
}

.input-card {
  background: white;
  border-radius: 16px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  border: 1px solid #edf2f7;
  overflow: hidden;
}

.custom-item {
  --padding-start: 16px;
  --padding-end: 16px;
  --inner-padding-end: 0;
  --background: transparent;
}

.custom-item ion-label {
  font-weight: 800;
  color: #1a202c;
  font-size: 0.9rem;
  margin-bottom: 8px !important;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.custom-input {
  font-weight: 600;
  color: #2d3748;
  font-size: 1.05rem;
}

.custom-select {
  --placeholder-color: #a0aec0;
  --placeholder-opacity: 1;
  font-weight: 700;
  color: #2d3748;
}

.action-area {
  margin-top: 24px;
}

.submit-btn {
  --background: var(--ion-color-secondary);
  --box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
  height: 56px;
  font-weight: 800;
  font-size: 1.1rem;
}

@media (min-width: 768px) {
  .form-container {
    padding-top: 40px;
  }
}
</style>
