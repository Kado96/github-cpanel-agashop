<!--
  * @file SupplyProductActions.vue
  * @description Page pour la gestion de Supply Product Actions.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-back-button color="light" default-href="/supplies"></ion-back-button>
        </ion-buttons>
        <ion-title color="light">{{ productName || 'Historique des achats' }}</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <!-- Uniquement l’historique des achats pour ce produit (exclut quantité / P.A.T = 0) -->
      <ion-list class="ion-margin-top">
        <ion-list-header>Historique des achats – {{ productName }}</ion-list-header>
        <ion-item v-for="s in displayedHistorique" :key="s.id">
          <ion-thumbnail slot="start">
            <ion-img :src="productImage(s)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
          </ion-thumbnail>
          <ion-label>
            <p>Quantité : {{ s.quantity ?? '—' }}</p>
            <ion-text>P.A.U : {{ money(s.quantity ? s.total_buy_price / s.quantity : 0) }} BIF</ion-text>
            <br />
            <ion-text>P.A.T : {{ money(s.total_buy_price ?? 0) }} BIF</ion-text>
            <br />
            <ion-text color="primary">Date : {{ formatDateTime(s.created_at) }}</ion-text>
          </ion-label>
        </ion-item>
        <ion-item v-if="displayedHistorique.length === 0 && !loading" lines="none">
          <ion-label class="ion-text-center">
            <p>Aucun achat enregistré pour ce produit.</p>
          </ion-label>
        </ion-item>
      </ion-list>
      <ion-progress-bar v-if="loading" type="indeterminate"></ion-progress-bar>
    </ion-content>

    <ion-footer class="ion-no-border supply-actions-footer">
      <ion-toolbar color="primary">
        <ion-buttons class="footer-buttons">
          <ion-button fill="clear" color="light" disabled>
            <ion-icon slot="start" :icon="timeOutline"></ion-icon>
            Historique des achats
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-footer>
  </ion-page>
</template>

<script>
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonBackButton,
  IonContent,
  IonFooter,
  IonButton,
  IonIcon,
  IonItem,
  IonLabel,
  IonThumbnail,
  IonImg,
  IonList,
  IonListHeader,
  IonProgressBar
} from '@ionic/vue';
import { timeOutline } from 'ionicons/icons';
import { productsService } from '../../services/api';
import { axiosService } from '../../plugins/axios';

import globalMixins from '../../composables/mixins';

/**
 * Composant SupplyProductActions
 * - Gère l'interface et la logique métier de Supply Product Actions.
 */
export default {
  mixins: [globalMixins],
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonBackButton,
    IonContent,
    IonFooter,
    IonButton,
    IonIcon,
    IonItem,
    IonLabel,
    IonThumbnail,
    IonImg,
    IonList,
    IonListHeader,
    IonProgressBar
  },
  data() {
    return {
      timeOutline,
      supply: null,
      historique: [],
      loading: false
    };
  },
  computed: {
    productName() {
      return this.supply?.product?.name || '';
    },
    productId() {
      return this.supply?.product?.id ?? null;
    },
    displayedHistorique() {
      return (this.historique || []).filter((s) => {
        const q = Number(s?.quantity ?? 0);
        const t = Number(s?.total_buy_price ?? 0);
        return q > 0 && t > 0;
      });
    },
  },
  beforeMount() {
    this.supply = this.$route.params.supply ?? this.$route.meta?.supply ?? this.$route.state?.supply ?? null;
    if (!this.supply) {
      this.$router.replace('/supplies');
      return;
    }
    this.fetchHistorique();
  },
  methods: {
    fetchHistorique() {
      const id = this.productId;
      if (!id) return;
      this.loading = true;
      productsService.getProductStock(id)
        .then((res) => {
          const data = res?.data;
          this.historique = Array.isArray(data) ? data : (data?.results ?? []);
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
          this.historique = [];
        });
    }
  }
};
</script>

<style lang="scss" scoped>
.supply-actions-footer {
  ion-toolbar {
    --padding-start: 12px;
    --padding-end: 12px;
    --padding-top: 8px;
    --padding-bottom: 8px;
  }
  .footer-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
  ion-button {
    color: #fff;
    font-weight: 600;
    margin: 0;
  }
  ion-button ion-icon {
    color: #fff;
  }
}
.product-summary {
  margin: 16px;
  ion-thumbnail {
    --size: 64px;
    --border-radius: 8px;
  }
  ion-img {
    border-radius: 8px;
    object-fit: cover;
  }
}
</style>
