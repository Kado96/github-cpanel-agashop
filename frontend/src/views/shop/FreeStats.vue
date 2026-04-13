<!--
  * @file FreeStats.vue
  * @description Page pour la gestion de Free Stats.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button @click="$router.push({name:'stats'})">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Statistiques</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="free-stats-content">
      <ion-row class="stats-cards-row">
        <!-- Carte Ventes -->
        <ion-col size="6" class="stat-card-col">
          <ion-card class="blue-stat-card">
            <ion-card-header>
              <ion-card-title class="card-title">Ventes</ion-card-title>
            </ion-card-header>
            <ion-card-content>
              <div class="card-detail">Quantité {{ stats?.sales?.total_sales ?? 0 }}</div>
              <div class="card-detail">Prix total : {{ money(stats?.sales?.total_amount ?? 0) }} BIF</div>
            </ion-card-content>
          </ion-card>
        </ion-col>

        <!-- Carte Achats -->
        <ion-col size="6" class="stat-card-col">
          <ion-card class="blue-stat-card">
            <ion-card-header>
              <ion-card-title class="card-title">Achats</ion-card-title>
            </ion-card-header>
            <ion-card-content>
              <div class="card-detail">Quantité {{ supplyTotalsQuantity ?? 0 }}</div>
              <div class="card-detail">Prix total : {{ money(supplyTotals ?? 0) }} BIF</div>
            </ion-card-content>
          </ion-card>
        </ion-col>

        <!-- Carte Bénéfice Ventes -->
        <ion-col size="6" class="stat-card-col">
          <ion-card class="blue-stat-card">
            <ion-card-header>
              <ion-card-title class="card-title">Bénéfice Ventes</ion-card-title>
            </ion-card-header>
            <ion-card-content>
              <div class="card-detail">{{ money(stats?.b_sales ?? 0) }} BIF</div>
            </ion-card-content>
          </ion-card>
        </ion-col>
      </ion-row>
    </ion-content>
  </ion-page>
</template>

<script>
import {
  IonHeader,
  IonPage,
  IonToolbar,
  IonButtons,
  IonBackButton,
  IonTitle,
  IonContent,
  IonRow,
  IonCol,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
} from '@ionic/vue';

import { shopsService, suppliesService } from '../../services/api';

/**
 * Composant FreeStats
 * - Gère l'interface et la logique métier de Free Stats.
 */
export default {
  components: {
    IonHeader,
    IonPage,
    IonToolbar,
    IonButtons,
    IonBackButton,
    IonTitle,
    IonContent,
    IonRow,
    IonCol,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
  },
  data() {
    return {
      shop: this.$store.state.shop,
      isLoading: false,
      stats: {},
      supplyTotals: null,
      supplyTotalsQuantity: null,
    };
  },
  computed: {
    shopId() {
      return this.shop?.id;
    },
  },
  beforeMount() {
    this.$store.state.shop = this.getShopFromLocalStorage();
    this.shop = this.$store.state.shop;
    this.checkCurrentShop();
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      if (!this.shopId) return;
      
      this.isLoading = true;
      try {
        const [statsRes] = await Promise.all([
          shopsService.getShopStats(this.shopId),
          this.fetchSupplies(),
        ]);

        this.stats = statsRes?.data ?? {};
      } catch (err) {
        this.errorOrRefresh(err, () => this.fetchStats());
      } finally {
        this.isLoading = false;
      }
    },
    fetchSupplies() {
      return suppliesService.getSupplies(this.shopId)
        .then((res) => {
          const d = res?.data ?? {};
          this.supplyTotals = d.totals ?? null;
          this.supplyTotalsQuantity = d.totals_quantity ?? null;
        })
        .catch(() => {
          this.supplyTotals = null;
          this.supplyTotalsQuantity = null;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.free-stats-content {
  --background: #ffffff;
  background: #ffffff;
  --padding-start: 16px;
  --padding-end: 16px;
  --padding-top: 16px;
}

.stats-cards-row {
  margin: 0;
  padding: 0;
}

.stat-card-col {
  margin-bottom: 16px;
  padding: 0 8px;
}

.blue-stat-card {
  background: #1976d2;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  margin: 0;
  color: white;

  ion-card-header {
    padding: 16px 16px 8px 16px;
  }

  ion-card-content {
    padding: 0 16px 16px 16px;
  }

  .card-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: white;
    text-align: center;
    margin: 0;
    padding: 0;
  }

  .card-detail {
    font-size: 0.95rem;
    color: white;
    text-align: center;
    margin: 4px 0;
    padding: 0;
  }
}

ion-header {
  ion-toolbar {
    --background: var(--ion-color-primary);
  }
}
</style>

