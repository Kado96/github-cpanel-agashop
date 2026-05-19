<!--
  * @file ProductSupplyHistory.vue
  * @description Modal affichant l'historique complet des achats (Supply) d'un produit.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="supply-history-back-btn" name="back-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>

        <ion-title color="light">Achats – {{ productName }}</ion-title>

        <ion-buttons slot="end">
          <ion-button id="supply-history-close-btn" name="close-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <!-- Résumé du produit -->
      <div class="product-summary">
        <ion-thumbnail class="summary-thumb">
          <ion-img :src="productImage(productProp)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
        </ion-thumbnail>
        <div class="summary-info">
          <h2>{{ productName }}</h2>
          <p class="category-text">{{ categoryLabel }}</p>
          <p>Stock actuel : <strong>{{ productQuantity }}</strong></p>
          <p>Prix de vente : <strong>{{ money(productSalePrice) }} BIF</strong></p>
        </div>
      </div>

      <!-- Totaux -->
      <div class="totals-bar" v-if="supplies.length > 0">
        <div class="total-item">
          <span class="total-label">Total achats</span>
          <span class="total-value">{{ supplies.length }}</span>
        </div>
        <div class="total-item">
          <span class="total-label">Quantité totale</span>
          <span class="total-value">{{ totalQuantity }}</span>
        </div>
        <div class="total-item">
          <span class="total-label">Montant total</span>
          <span class="total-value">{{ money(totalAmount) }} BIF</span>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="ion-text-center ion-padding">
        <ion-spinner name="bubbles" color="primary"></ion-spinner>
        <p>Chargement de l'historique...</p>
      </div>

      <!-- Liste des achats -->
      <ion-list v-if="!loading && supplies.length > 0" class="supplies-list">
        <ion-list-header>
          Historique complet des achats ({{ supplies.length }})
        </ion-list-header>

        <ion-item v-for="(supply, index) in supplies" :key="supply.id || index" class="supply-item">
          <ion-label>
            <div class="supply-row">
              <div class="supply-index">{{ index + 1 }}</div>
              <div class="supply-details">
                <p class="supply-date">
                  <ion-icon :icon="calendarOutline" class="inline-icon"></ion-icon>
                  {{ formatDateTime(supply.created_at) }}
                </p>
                <p>Quantité : <strong>{{ supply.quantity }}</strong></p>
                <p>
                  P.A.U :
                  <strong>{{ money(supply.quantity > 0 ? supply.total_buy_price / supply.quantity : 0) }} BIF</strong>
                </p>
                <p>
                  P.A.T :
                  <ion-text color="secondary"><strong>{{ money(supply.total_buy_price) }} BIF</strong></ion-text>
                </p>
                <p v-if="supply.sale_price > 0">
                  P.V.U :
                  <ion-text color="primary"><strong>{{ money(supply.sale_price) }} BIF</strong></ion-text>
                </p>
              </div>
            </div>
          </ion-label>
        </ion-item>
      </ion-list>

      <!-- Aucun achat -->
      <div v-if="!loading && supplies.length === 0" class="empty-state">
        <ion-icon :icon="cartOutline" class="empty-icon"></ion-icon>
        <p>Aucun achat enregistré pour ce produit.</p>
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
  IonList,
  IonListHeader,
  IonItem,
  IonLabel,
  IonButton,
  IonButtons,
  IonIcon,
  IonSpinner,
  IonText,
  IonThumbnail,
  IonImg,
  modalController
} from '@ionic/vue';
import {
  close,
  arrowBackOutline,
  calendarOutline,
  cartOutline
} from 'ionicons/icons';
import { productsService } from '../../services/api';
import globalMixins from '../../composables/mixins';

/**
 * Composant ProductSupplyHistory
 * - Affiche l'historique complet des achats (Supply) d'un produit donné.
 * - Utilise l'endpoint GET /shops/products/{id}/stock/ qui retourne TOUS les achats sans filtrage de dates.
 */
export default {
  mixins: [globalMixins],
  name: 'ProductSupplyHistory',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonList,
    IonListHeader,
    IonItem,
    IonLabel,
    IonButton,
    IonButtons,
    IonIcon,
    IonSpinner,
    IonText,
    IonThumbnail,
    IonImg
  },
  props: {
    productProp: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      supplies: [],
      loading: false,
      close,
      arrowBackOutline,
      calendarOutline,
      cartOutline
    };
  },
  computed: {
    productName() {
      return this.productProp?.name
        ?? this.productProp?.product?.name
        ?? '—';
    },
    productQuantity() {
      return this.productProp?.quantity ?? 0;
    },
    productSalePrice() {
      return this.productProp?.sale_price ?? 0;
    },
    productId() {
      return this.productProp?.id ?? null;
    },

    categoryLabel() {
      if (!this.productProp) return '';
      const bp = this.productProp?.product;
      if (!bp) return '';
      const sub = bp?.sub_category;
      if (sub && typeof sub === 'object' && sub.name) {
        const catName = sub.category?.name || '';
        return catName ? `${catName} > ${sub.name}` : sub.name;
      }
      return '';
    },
    totalQuantity() {
      return this.supplies.reduce((sum, s) => sum + (Number(s.quantity) || 0), 0);
    },
    totalAmount() {
      return this.supplies.reduce((sum, s) => sum + (Number(s.total_buy_price) || 0), 0);
    }
  },
  created() {
    if (this.productId) {
      this.fetchSupplyHistory();
    }
  },
  methods: {
    money(x, decimals = 0) {
      let cash = parseFloat(x).toFixed(decimals);
      if (isNaN(x) || x == null) return '—';
      return cash.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    },
    formatDateTime(x) {
      if (!x) return '—';
      try {
        const date = new Date(x);
        if (isNaN(date.getTime())) return String(x);
        return new Intl.DateTimeFormat('fr-FR', {
          dateStyle: 'medium',
          timeStyle: 'short'
        }).format(date);
      } catch {
        return String(x);
      }
    },
    performClose() {
      return modalController.dismiss(null, 'cancel');
    },
    async fetchSupplyHistory() {
      if (!this.productId) return;
      this.loading = true;
      try {
        const res = await productsService.getProductStock(this.productId);
        const data = res?.data ?? [];
        // data peut être un tableau direct ou un objet avec results
        this.supplies = Array.isArray(data) ? data : (data.results ?? []);
        // Trier par date décroissante (plus récent en premier)
        this.supplies.sort((a, b) => {
          const da = new Date(a?.created_at || '1970-01-01').getTime();
          const db = new Date(b?.created_at || '1970-01-01').getTime();
          return db - da;
        });
      } catch (err) {
        console.error('[ProductSupplyHistory] Erreur chargement:', err);
        this.supplies = [];
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
ion-header ion-toolbar {
  --border-radius: 16px 16px 0 0;
}

ion-buttons ion-icon {
  font-size: 24px;
}

.product-summary {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  .summary-thumb {
    width: 72px;
    height: 72px;
    --border-radius: 12px;
    flex-shrink: 0;

    ion-img {
      border-radius: 12px;
      object-fit: cover;
    }
  }

  .summary-info {
    flex: 1;

    h2 {
      font-size: 1.1rem;
      font-weight: 700;
      margin: 0 0 4px 0;
      color: #1e293b;
    }

    .category-text {
      font-size: 0.8rem;
      color: var(--ion-color-primary);
      font-weight: 500;
      margin: 0 0 6px 0;
    }

    p {
      font-size: 0.9rem;
      margin: 2px 0;
      color: #475569;
    }
  }
}

.totals-bar {
  display: flex;
  justify-content: space-around;
  background: var(--ion-color-primary);
  border-radius: 12px;
  padding: 12px 8px;
  margin-bottom: 12px;

  .total-item {
    text-align: center;

    .total-label {
      display: block;
      font-size: 0.7rem;
      color: rgba(255, 255, 255, 0.8);
      font-weight: 500;
      margin-bottom: 2px;
    }

    .total-value {
      display: block;
      font-size: 1rem;
      color: white;
      font-weight: 700;
    }
  }
}

.supplies-list {
  margin-top: 4px;

  ion-list-header {
    font-size: 0.95rem;
    font-weight: 600;
    color: #475569;
  }

  .supply-item {
    margin-bottom: 4px;
    --padding-start: 8px;

    .supply-row {
      display: flex;
      align-items: flex-start;
      gap: 12px;

      .supply-index {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: var(--ion-color-primary-tint);
        color: var(--ion-color-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
        flex-shrink: 0;
        margin-top: 4px;
      }

      .supply-details {
        flex: 1;

        .supply-date {
          font-size: 0.85rem;
          color: var(--ion-color-primary);
          font-weight: 600;
          margin-bottom: 4px;

          .inline-icon {
            font-size: 14px;
            vertical-align: middle;
            margin-right: 4px;
          }
        }

        p {
          font-size: 0.85rem;
          margin: 2px 0;
          color: #475569;
        }
      }
    }
  }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;

  .empty-icon {
    font-size: 64px;
    color: #cbd5e1;
    margin-bottom: 16px;
  }

  p {
    font-size: 1rem;
    color: #94a3b8;
    font-weight: 500;
  }
}
</style>
