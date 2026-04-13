<!--
  * @file ShopStats.vue
  * @description Page pour la gestion de Shop Stats.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button @click="$router.push({ name: 'shop' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Statistiques</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="stats-content">
      <div v-if="stats && stats.subscription_plan === 'FREE'" class="trial-info-banner" @click="navigateToPaymentMethods">
        <div class="trial-info-text">
          <span class="trial-badge">ESSAI</span>
          Il vous reste <span class="font-bold">{{ daysRemaining }} jours</span> d'essai gratuit
        </div>
        <ion-icon :icon="chevronForwardOutline" class="trial-banner-arrow"></ion-icon>
      </div>

      <ion-row class="stats-row">
        <!-- Volume Stock -->
        <ion-col size="12" class="stat-card-col">
          <ion-card class="stat-card clickable" @click="navigateToStock">
            <ion-card-header>
              <ion-card-title class="stat-title">Volume Stock</ion-card-title>
              <div class="stat-divider"></div>
              <ion-card-subtitle class="stat-subtitle blue-text">
                {{ stockVolume }} Article(s) Disponible(s)
              </ion-card-subtitle>
            </ion-card-header>
            <ion-icon :icon="chevronForwardOutline" class="stat-arrow"></ion-icon>
          </ion-card>
        </ion-col>

        <!-- Valeur et Coût du Stock -->
        <ion-col size="12" class="stat-card-col">
          <ion-card class="stat-card clickable" @click="navigateToStockValue">
            <ion-card-header>
              <ion-card-title class="stat-title">Valeur et Coût du Stock</ion-card-title>
              <div class="stat-divider"></div>
              <ion-card-subtitle class="stat-subtitle blue-text">
                Valeur du stock : {{ money(stockValue) }} BIF <br/>
                Coût du stock : {{ money(stockCost) }} BIF
              </ion-card-subtitle>
            </ion-card-header>
            <ion-icon :icon="chevronForwardOutline" class="stat-arrow"></ion-icon>
          </ion-card>
        </ion-col>

        <!-- Unités Actives -->
        <ion-col size="12" class="stat-card-col">
          <ion-card class="stat-card clickable" @click="navigateToActiveArticles">
            <ion-card-header>
              <ion-card-title class="stat-title">Articles Actifs</ion-card-title>
              <div class="stat-divider"></div>
              <ion-card-subtitle class="stat-subtitle green-text">
                {{ activeArticlesCount }} Article(s) Actif(s)
              </ion-card-subtitle>
            </ion-card-header>
            <ion-icon :icon="chevronForwardOutline" class="stat-arrow"></ion-icon>
          </ion-card>
        </ion-col>

        <!-- Unités Critiques -->
        <ion-col size="12" class="stat-card-col">
          <ion-card class="stat-card clickable" @click="navigateToCriticalArticles">
            <ion-card-header>
              <ion-card-title class="stat-title">Articles Critiques</ion-card-title>
              <div class="stat-divider"></div>
              <ion-card-subtitle class="stat-subtitle orange-text">
                {{ criticalArticlesCount }} Article(s) Critique(s)
              </ion-card-subtitle>
            </ion-card-header>
            <ion-icon :icon="chevronForwardOutline" class="stat-arrow"></ion-icon>
          </ion-card>
        </ion-col>

        <!-- Mes Ventes -->
        <ion-col size="12" class="stat-card-col">
          <ion-card class="stat-card clickable" @click="navigateToSales">
            <ion-card-header>
              <ion-card-title class="stat-title">Mes Ventes</ion-card-title>
              <div class="stat-divider"></div>
              <ion-card-subtitle class="stat-subtitle orange-text">
                Vente du Jour: {{ money(dailySales) }} BIF
              </ion-card-subtitle>
            </ion-card-header>
            <ion-icon :icon="chevronForwardOutline" class="stat-arrow"></ion-icon>
          </ion-card>
        </ion-col>

        <!-- Mes Dépenses -->
        <ion-col size="12" class="stat-card-col">
          <ion-card class="stat-card clickable" @click="navigateToExpenses">
            <ion-card-header>
              <ion-card-title class="stat-title">Mes Dépenses</ion-card-title>
              <div class="stat-divider"></div>
              <ion-card-subtitle class="stat-subtitle orange-text">
                Dépense du Jour: {{ money(dailyExpenses) }} BIF
              </ion-card-subtitle>
            </ion-card-header>
            <ion-icon :icon="chevronForwardOutline" class="stat-arrow"></ion-icon>
          </ion-card>
        </ion-col>

        <!-- Mes Bénéfices -->
        <ion-col size="12" class="stat-card-col">
          <ion-card class="stat-card clickable" @click="navigateToProfits">
            <ion-card-header>
              <ion-card-title class="stat-title">Mes Bénéfices</ion-card-title>
              <div class="stat-divider"></div>
              <ion-card-subtitle class="stat-subtitle blue-text">
                Bénéfice du Jour: {{ money(dailyProfit) }} BIF <br/>
                <span class="weekly-profit">Rentabilité Net (Semaine): {{ money(weeklyProfit) }} BIF</span>
              </ion-card-subtitle>
            </ion-card-header>
            <ion-icon :icon="chevronForwardOutline" class="stat-arrow"></ion-icon>
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
  IonButton,
  IonBackButton,
  IonTitle,
  IonContent,
  IonRow,
  IonCol,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonIcon,
  alertController,
} from '@ionic/vue';

import { chevronForwardOutline, arrowBackOutline } from 'ionicons/icons';
import { shopsService, suppliesService, productsService, expensesService } from '../../services/api';

/**
 * Composant ShopStats
 * - Gère l'interface et la logique métier de Shop Stats.
 */
export default {
  components: {
    IonHeader,
    IonPage,
    IonToolbar,
    IonButtons,
    IonButton,
    IonBackButton,
    IonTitle,
    IonContent,
    IonRow,
    IonCol,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonIcon,
  },
  data() {
    return {
      chevronForwardOutline,
      arrowBackOutline,
      shop: this.$store.state.shop,
      isLoading: false,
      stats: {},
      products: [],
      stockVolume: 0,
      stockValue: 0,
      stockCost: 0,
      activeArticlesCount: 0,
      criticalArticlesCount: 0,
      dailySales: 0,
      dailyExpenses: 0,
      dailyProfit: 0,
      weeklyProfit: 0,
      generalExpenses: [],
      daysRemaining: 0,
    };
  },
  watch: {
    stats: {
      handler(newStats) {
        if (newStats && newStats.trial_end_date) {
          const end = new Date(newStats.trial_end_date);
          const today = new Date();
          const diffTime = end - today;
          this.daysRemaining = Math.max(0, Math.ceil(diffTime / (1000 * 60 * 60 * 24)));
        }
      },
      deep: true,
    }
  },
  ionViewWillEnter() {
    this.fetchShopInfoLocally();
    this.checkCurrentShop();
    this.fetchStats();
    
    // Initialiser l'aide contextuelle pour le ChatBot
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Tableau de Bord Principal',
      description: 'C\'est le centre de contrôle de votre boutique. Vous y voyez les indicateurs clés de performance en temps réel pour piloter votre rentabilité.',
      elements: [
        { type: 'Individuel', label: 'Marge Brute du Jour', desc: 'Représente le profit généré uniquement par vos ventes d\'aujourd\'hui (Prix de Vente - Prix d\'Achat).' },
        { type: 'Hebdomadaire', label: 'Bénéfice Net', desc: 'C\'est votre profit réel sur les 7 derniers jours après avoir soustrait toutes les dépenses générales (loyer, transport, etc.).' },
        { type: 'Stock', label: 'Volume de Stock', desc: 'La valeur totale de tous vos produits actuellement en rayon, calculée au prix de vente.' },
        { type: 'Alerte', label: 'Articles Critiques', desc: 'Affiche le nombre de produits dont le stock est en dessous du minimum défini. Cliquez pour voir la liste.' }
      ],
      faq: [
        { question: 'Pourquoi mon bénéfice net est-il plus bas que ma marge ?', answer: 'Car le bénéfice net retire vos charges fixes (dépenses) alors que la marge ne regarde que le commerce des produits.' },
        { question: 'Comment mettre à jour ces chiffres ?', answer: 'Les chiffres sont mis à jour automatiquement à chaque vente ou dépense enregistrée.' }
      ]
    });
  },
  computed: {
    shopId() {
      return this.shop?.id;
    },
  },
  methods: {
    fetchShopInfoLocally() {
      this.$store.state.shop = this.getShopFromLocalStorage();
      this.shop = this.$store.state.shop;
    },
    async fetchStats() {
      if (!this.shopId) return;

      this.isLoading = true;
      try {
        const now = new Date();
        const todayStr = now.toISOString().split('T')[0];
        const weekAgo = new Date(now);
        weekAgo.setDate(now.getDate() - 7);
        const weekAgoStr = weekAgo.toISOString().split('T')[0];

        // Charger stats du jour et de la semaine
        const [statsRes, weekStatsRes] = await Promise.all([
          shopsService.getShopStats(this.shopId),
          shopsService.getShopStats(this.shopId, { created_at__gte: weekAgoStr, created_at__lte: todayStr })
        ]);
        
        const data = statsRes?.data ?? {};
        const weekData = weekStatsRes?.data ?? {};
        this.stats = data;

        // Mapper les données du backend vers l'état local
        this.stockVolume = data.stock_volume || 0;
        this.stockValue = data.stock_value || 0;
        this.stockCost = data.stock_cost || 0;
        this.activeArticlesCount = data.active_articles || 0;
        this.criticalArticlesCount = data.critical_articles || 0;
        this.dailySales = data.sales?.total_amount || 0;
        this.dailyExpenses = data.total_general_expenses || 0;
        
        // Calcul des bénéfices
        this.dailyProfit = data.b_sales || 0; // Marge Brute du jour
        this.weeklyProfit = (weekData.b_sales || 0) - (weekData.total_general_expenses || 0); // Net hebdomadaire (Marge - Dépenses)

      } catch (err) {
        // Gestion de l'erreur Premium : on ne redirige plus automatiquement
        if (err?.response?.status === 403) {
            this.isLoading = false;
            // this.$router.push({ name: 'payment-methods' });
            return;
        }
        
        console.error("Error fetching stats:", err);
        this.errorOrRefresh(err, () => this.fetchStats());
      } finally {
        this.isLoading = false;
      }
    },
    calculateMetrics() {
      // Les calculs sont maintenant faits côté backend
    },
    navigateToStock() {
      // Navigation vers la page de volume du stock (Dashboard)
      this.$router.push({ name: 'stock-volume' });
    },
    navigateToStockValue() {
      // Navigation vers la page de valeur du stock (Dashboard)
      this.$router.push({ name: 'active-articles' });
    },
    navigateToActiveArticles() {
      // Navigation vers les articles actives (Dashboard)
      this.$router.push({ name: 'active-articles' });
    },
    navigateToCriticalArticles() {
      // Navigation vers les articles critiques (Dashboard)
      this.$router.push({ name: 'critical-articles' });
    },
    navigateToSales() {
      // Navigation vers les ventes
      this.$router.push({ name: 'sales' });
    },
    navigateToExpenses() {
      // Navigation vers la page de dépenses dédiée
      this.$router.push({ name: 'expenses' });
    },
    navigateToProfits() {
      // Navigation vers les bénéfices (Nouvel architecture : Dashboard -> Liste)
      this.$router.push({ name: 'profits' });
    },
    navigateToFreeStats() {
      // Navigation vers les statistiques gratuites
      this.$router.push({ name: 'free-stats' });
    },
    showSubscriptionRequired() {
      // Redirection automatique sans popup
      this.$router.push({ name: 'payment-methods' });
    },
    navigateToPaymentMethods() {
      this.$router.push({ name: 'payment-methods' });
    },
    money(val) {
      if (!val) return "0";
      return parseFloat(val).toLocaleString('fr-FR');
    }
  },
};
</script>

<style lang="scss" scoped>
.font-bold {
  font-weight: bold;
}

.stats-content {
  --background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
  background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
  --padding-start: 16px;
  --padding-end: 16px;
  --padding-top: 16px;
  --padding-bottom: 16px;
}

.trial-info-banner {
  background: rgba(255, 255, 255, 0.9);
  margin: 0 16px 12px;
  padding: 8px 12px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(var(--ion-color-primary-rgb), 0.2);
  cursor: pointer;

  .trial-info-text {
    font-size: 0.85rem;
    color: #333;
    display: flex;
    align-items: center;
    gap: 8px;

    .trial-badge {
      background: var(--ion-color-primary);
      color: white;
      font-size: 0.65rem;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
    }
  }

  .trial-banner-arrow {
    font-size: 16px;
    color: var(--ion-color-primary);
  }
}

.stats-row {
  margin: 0;
  padding: 0;
  max-width: 100%;
}

.stat-card-col {
  margin-bottom: 18px;
  padding: 0 6px;
}

.stat-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04);
  margin: 0;
  position: relative;
  padding: 4px 8px;
  min-height: 20px;
  max-width: 100%;
  width: 100%;
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: all 0.2s ease;

  &.clickable {
    cursor: pointer;

    &:hover {
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06);
      transform: translateY(-2px);
    }

    &:active {
      transform: translateY(0);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }

  ion-card-header {
    padding: 0;
    margin-bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 20px;
  }

  .stat-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0f172a;
    text-align: center;
    margin: 4px 0;
    padding: 0;
    width: 100%;
    letter-spacing: -0.2px;
    line-height: 1.2;
  }

  .stat-divider {
    width: 60%;
    height: 1.5px;
    background: #e2e8f0;
    margin: 6px auto;
    opacity: 0.8;
  }

  .stat-subtitle {
    font-size: 0.95rem;
    text-align: center;
    margin: 4px 0;
    padding: 0 4px;
    line-height: 1.3;
    font-weight: 700;

    &.blue-text {
      color: #2563eb;
    }
    
    &.green-text {
      color: #166534;
    }

    &.orange-text {
      color: #ea580c;
    }
    
    .weekly-profit {
      font-size: 0.85rem;
      color: #1583C1;
      opacity: 0.9;
    }
  }

  .stat-arrow {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 14px;
    color: #bdbdbd;
    transition: all 0.2s ease;
  }

  &.clickable:hover .stat-arrow {
    color: var(--ion-color-primary);
    transform: translateY(-50%) translateX(1px);
  }
}

ion-header {
  ion-toolbar {
    --background: var(--ion-color-primary);
    --border-width: 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

// Animation d'entrée pour les cartes
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card-col {
  animation: fadeInUp 0.4s ease-out;
  animation-fill-mode: both;

  @for $i from 1 through 9 {
    &:nth-child(#{$i}) {
      animation-delay: #{$i * 0.05}s;
    }
  }
}
</style>
