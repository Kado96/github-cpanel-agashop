<!--
  * @file AgentCommissions.vue
  * @description Interface du suivi des commissions pour les Agents AgaShop.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button @click="$router.back()">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          💼 Mes Commissions Agent
        </ion-title>
        <ion-buttons slot="end">
          <ion-button @click="fetchCommissions">
            <ion-icon color="light" size="large" :icon="refreshOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <!-- Synthèse des Gains -->
      <ion-row class="stats-row">
        <ion-col size="6">
          <ion-card class="stat-card pending-card">
            <ion-card-content>
              <div class="stat-title">En attente</div>
              <div class="stat-amount">{{ formatBIF(totalPending) }}</div>
            </ion-card-content>
          </ion-card>
        </ion-col>
        <ion-col size="6">
          <ion-card class="stat-card paid-card">
            <ion-card-content>
              <div class="stat-title">Payé</div>
              <div class="stat-amount">{{ formatBIF(totalPaid) }}</div>
            </ion-card-content>
          </ion-card>
        </ion-col>
      </ion-row>

      <!-- Liste des Commissions -->
      <div class="list-header">
        <h2>Historique des Commissions (10%)</h2>
      </div>

      <ion-loading :is-open="loading" message="Chargement des commissions..."></ion-loading>

      <div v-if="!loading && commissions.length === 0" class="empty-state">
        <ion-icon :icon="walletOutline" class="empty-icon"></ion-icon>
        <p>Aucune commission enregistrée pour le moment.</p>
        <small>Les commissions sont automatiquement générées (10%) lorsqu'une boutique souscrit un abonnement LumiCash.</small>
      </div>

      <ion-list v-else>
        <ion-item v-for="item in commissions" :key="item.id" class="commission-item">
          <ion-icon 
            slot="start" 
            :icon="cashOutline" 
            :color="item.status === 'PAID' ? 'success' : 'warning'"
            class="item-icon"
          ></ion-icon>
          <ion-label>
            <h3>{{ item.shop_name || 'Boutique AgaShop' }}</h3>
            <p>{{ item.notes || 'Commission sur abonnement' }}</p>
            <p class="date-text">{{ formatDate(item.created_at) }}</p>
          </ion-label>
          <div slot="end" class="amount-badge">
            <span class="amount-val">+{{ formatBIF(item.amount) }}</span>
            <ion-badge :color="item.status === 'PAID' ? 'success' : 'warning'" class="status-badge">
              {{ item.status === 'PAID' ? 'Payé' : 'En attente' }}
            </ion-badge>
          </div>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script>
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonButton,
  IonIcon,
  IonRow,
  IonCol,
  IonCard,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonBadge,
  IonLoading
} from '@ionic/vue';
import { arrowBackOutline, refreshOutline, walletOutline, cashOutline } from 'ionicons/icons';
import { axiosService } from '@/plugins/axios';

export default {
  name: 'AgentCommissions',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonButtons,
    IonButton,
    IonIcon,
    IonRow,
    IonCol,
    IonCard,
    IonCardContent,
    IonList,
    IonItem,
    IonLabel,
    IonBadge,
    IonLoading
  },
  data() {
    return {
      commissions: [],
      loading: false,
      arrowBackOutline,
      refreshOutline,
      walletOutline,
      cashOutline
    };
  },
  computed: {
    totalPending() {
      return this.commissions
        .filter(c => c.status === 'PENDING')
        .reduce((sum, c) => sum + parseFloat(c.amount || 0), 0);
    },
    totalPaid() {
      return this.commissions
        .filter(c => c.status === 'PAID')
        .reduce((sum, c) => sum + parseFloat(c.amount || 0), 0);
    }
  },
  mounted() {
    this.fetchCommissions();
  },
  methods: {
    async fetchCommissions() {
      this.loading = true;
      try {
        const response = await axiosService.get('/shops/commissions/');
        this.commissions = response.data.results || response.data;
      } catch (error) {
        console.error("Erreur récupération commissions agent:", error);
      } finally {
        this.loading = false;
      }
    },
    formatBIF(amount) {
      if (!amount) return '0 BIF';
      return new Intl.NumberFormat('fr-BI', { maximumFractionDigits: 0 }).format(amount) + ' BIF';
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      return new Date(dateStr).toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.stats-row {
  margin-bottom: 1rem;
}
.stat-card {
  margin: 0;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.pending-card {
  border-left: 4px solid var(--ion-color-warning);
}
.paid-card {
  border-left: 4px solid var(--ion-color-success);
}
.stat-title {
  font-size: 0.85rem;
  color: #666;
  text-transform: uppercase;
  font-weight: 600;
}
.stat-amount {
  font-size: 1.1rem;
  font-weight: 800;
  color: #111;
  margin-top: 4px;
}
.list-header h2 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 1rem 0 0.5rem;
  color: #333;
}
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #888;
}
.empty-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}
.commission-item {
  --padding-start: 0;
  --inner-padding-end: 0;
  margin-bottom: 8px;
}
.item-icon {
  font-size: 1.8rem;
  margin-right: 12px;
}
.date-text {
  font-size: 0.75rem;
  color: #888;
}
.amount-badge {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}
.amount-val {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--ion-color-success);
}
.status-badge {
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 4px;
}
</style>
