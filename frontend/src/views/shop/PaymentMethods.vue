<!--
  * @file PaymentMethods.vue
  * @description Page pour la gestion de Payment Methods.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="back-to-shop" name="back-to-shop" @click="goBack">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Modes de paiement</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding premium-content">
      <div v-if="shop && shop.subscription_plan === 'FREE'" class="trial-banner">
        <ion-card class="trial-card">
          <ion-card-content>
            <h3>Mode Essai Gratuit</h3>
            <p v-if="daysRemaining > 0">Il vous reste <span class="font-bold">{{ daysRemaining }} jours</span> d'essai.</p>
            <p v-else-if="daysRemaining === 0">Dernier jour d'essai !</p>
            <p v-else class="status-expired">Période d'essai expirée.</p>
            <p class="trial-date">Fin prévue le : {{ formatDate(shop.trial_end_date) }}</p>
          </ion-card-content>
        </ion-card>
      </div>

      <div class="premium-icon">
        <span class="no-ads-icon">ADS</span>
      </div>
      <h1 class="premium-title">Premium</h1>
      <p class="premium-description">
        Profitez de toutes les fonctionnalités avancées de gestion et de statistiques. 
        Choisissez un forfait pour continuer après votre période d'essai.
      </p>
      <div class="subscription-buttons">
        <ion-button expand="block" class="btn-monthly" @click="onMonthly">
          Abonnement Mensuel : 20.000 BIF
        </ion-button>
        <ion-button expand="block" class="btn-6months" @click="on6Months">
          Abonnement 6 mois : 100.000 BIF
        </ion-button>
        <ion-button expand="block" class="btn-annual" @click="onAnnual">
          Abonnement Annuel : 180.000 BIF
        </ion-button>
      </div>
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
  IonBackButton,
  IonButton,
  IonCard,
  IonCardContent,
  IonIcon
} from '@ionic/vue';
import { arrowBackOutline } from 'ionicons/icons';
import { shopsService } from '@/services/api/shops';

/**
 * Composant PaymentMethods
 * - Gère l'interface et la logique métier de Payment Methods.
 */
export default {
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonButtons,
    IonBackButton,
    IonButton,
    IonCard,
    IonCardContent,
    IonIcon
  },
  data() {
    return {
      shop: null,
      daysRemaining: 0,
      arrowBackOutline
    };
  },
  async ionViewWillEnter() {
    await this.fetchShopInfo();
  },
  methods: {
    async fetchShopInfo() {
      try {
        const activeShop = JSON.parse(localStorage.getItem('activeShop'));
        if (activeShop) {
          const response = await shopsService.getShop(activeShop.id);
          this.shop = response.data;
          this.calculateTrialDays();
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des infos de la boutique", error);
      }
    },
    calculateTrialDays() {
      if (this.shop && this.shop.trial_end_date) {
        const end = new Date(this.shop.trial_end_date);
        const today = new Date();
        const diffTime = end - today;
        this.daysRemaining = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    onMonthly() {
      // À configurer plus tard
    },
    on6Months() {
      // À configurer plus tard
    },
    onAnnual() {
      // À configurer plus tard
    },
    goBack() {
      // Navigation explicite pour éviter les "hallucinations" de l'historique
      this.$router.push({ name: 'shop' });
    }
  }
};
</script>

<style lang="scss" scoped>
.premium-content {
  --background: #f5f0f8;
  text-align: center;
  padding: 1.5rem 1rem;
}

.premium-icon {
  margin: 2rem 0 1rem;
  display: flex;
  justify-content: center;
  align-items: center;

  .no-ads-icon {
    font-size: 2.5rem;
    font-weight: 800;
    color: #333;
    letter-spacing: 0.1em;
    position: relative;
    display: inline-block;

    &::after {
      content: '';
      position: absolute;
      top: 50%;
      left: -5%;
      width: 110%;
      height: 3px;
      background: #333;
      transform: rotate(-15deg);
    }
  }
}

.premium-title {
  font-size: 2rem;
  font-weight: 800;
  color: #222;
  margin: 0 0 1.5rem;
}

.premium-description {
  text-align: left;
  color: #333;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 2rem;
}

.font-bold {
  font-weight: bold;
}

.subscription-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  ion-button {
    font-weight: 600;
    font-size: 1rem;
    --border-radius: 12px;
    height: 48px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .btn-monthly {
    --background: #ff8c00;
    --background-hover: #e67e00;
    --background-activated: #cc6f00;
    --color: #fff;
  }

  .btn-6months {
    --background: #e53935;
    --background-hover: #c62828;
    --background-activated: #b71c1c;
    --color: #fff;
  }

  .btn-annual {
    --background: #43a047;
    --background-hover: #388e3c;
    --background-activated: #2e7d32;
    --color: #fff;
  }
}

.trial-banner {
  margin-bottom: 1rem;
  
  .trial-card {
    margin: 0;
    --background: #fff;
    border-left: 4px solid var(--ion-color-primary);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    
    ion-card-content {
      padding: 12px;
      text-align: left;
      
      h3 {
        margin: 0 0 5px;
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--ion-color-primary);
      }
      
      p {
        margin: 2px 0;
        font-size: 0.9rem;
        color: #444;
      }

      .trial-date {
        font-size: 0.8rem;
        color: #888;
        font-style: italic;
      }
      
      .status-expired {
        color: var(--ion-color-danger);
        font-weight: 700;
      }
    }
  }
}
</style>
