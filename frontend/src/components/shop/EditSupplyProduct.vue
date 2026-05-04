<!--
  * @file EditSupplyProduct.vue
  * @description Page pour la gestion de Edit Supply Product.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="edit-supply-product-back-btn" name="back-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>

        <ion-title color="light">Modifier l'achat – {{ productName }}</ion-title>

        <ion-buttons slot="end">
          <ion-button id="edit-supply-product-close-btn" name="close-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-grid fixed>
        <ion-row class="ion-justify-content-center">
          <ion-col size="12">
            <ion-list lines="none">
              <ion-item-group>
                <form>
                  <div class="ion-margin-vertical">
                    <ion-item>
                      <ion-input
                        id="edit-supply-quantity"
                        name="quantity"
                        label="Quantité"
                        label-placement="stacked"
                        v-model="product.quantity"
                        placeholder="Quantité"
                        @keydown="initErrors"
                        @change="updateInfo"
                        type="number"
                        autocomplete="off">
                      </ion-input>
                    </ion-item>
                    <ion-text v-if="errors.quantity.empty" class="error" color="danger">
                      * Quantités négatives non permises
                    </ion-text>
                  </div>
                  <div class="ion-margin-vertical">
                    <ion-item>
                      <ion-input
                        id="edit-supply-total-buy-price"
                        name="total_buy_price"
                        label="Prix d'achat total"
                        label-placement="stacked"
                        v-model="product.total_buy_price"
                        placeholder="Prix d'achat total"
                        @keydown="initErrors"
                        @change="updateInfo"
                        type="number"
                        autocomplete="off">
                      </ion-input>
                    </ion-item>
                    <ion-text v-if="errors.total_buy_price.empty" class="error" color="danger">
                      * Prix négatif non permis
                    </ion-text>
                  </div>
                  <div class="ion-margin-vertical">
                    <ion-item>
                      <ion-input
                        id="edit-supply-sale-price"
                        name="sale_price"
                        label="Prix de vente unitaire"
                        label-placement="stacked"
                        v-model="product.sale_price"
                        placeholder="Prix de vente unitaire (BIF)"
                        @keydown="initErrors"
                        type="number"
                        min="0"
                        autocomplete="off">
                      </ion-input>
                    </ion-item>
                  </div>
                  <div class="ion-margin-vertical">
                    <ion-label class="ion-padding-start">Date de l'achat</ion-label>
                    <ion-datetime
                      id="edit-supply-date"
                      name="created_at"
                      presentation="date"
                      v-model="product.created_at"
                      locale="fr-FR"
                    ></ion-datetime>
                  </div>
                  <div class="ion-margin-vertical">
                    <ion-text>P.A.U : {{ buyPriceDisplay === '—' ? '' : buyPriceDisplay + ' BIF' }}</ion-text>
                  </div>
                  <div class="ion-margin-vertical" v-if="hasBenefit">
                    <ion-text color="success" class="ion-display-block">Bénéfice unitaire : {{ benefitPerUnit }} BIF</ion-text>
                    <ion-text color="success" class="ion-display-block">Bénéfice total : {{ benefitTotal }} BIF</ion-text>
                  </div>
                  <div class="ion-margin-vertical" v-if="supplyProp?.created_at">
                    <ion-text color="medium" class="ion-display-block">Créé le : {{ datetime(supplyProp.created_at) }}</ion-text>
                  </div>
                  <div class="ion-margin-vertical" v-if="lastUpdatedAt">
                    <ion-text color="primary" class="ion-display-block">Dernière modification : {{ lastUpdatedAt }}</ion-text>
                  </div>
                  <ion-button
                    color="secondary"
                    expand="block"
                    class="ion-margin-top"
                    :disabled="loading"
                    @click="performSave">
                    <ion-spinner v-if="loading" slot="start"></ion-spinner>
                    <ion-text color="light">Valider</ion-text>
                  </ion-button>
                </form>
              </ion-item-group>
            </ion-list>
          </ion-col>
        </ion-row>
      </ion-grid>
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
  IonItemGroup,
  IonItem,
  IonInput,
  IonButton,
  IonButtons,
  IonIcon,
  IonFooter,
  IonSpinner,
  IonText,
  modalController,
  IonRow,
  IonCol,
  IonGrid,
  IonLabel,
  IonDatetime
} from '@ionic/vue';
import { close, arrowBackOutline } from 'ionicons/icons';
import { suppliesService, productsService } from '../../services/api';

/**
 * Composant EditSupplyProduct
 * - Gère l'interface et la logique métier de Edit Supply Product.
 */
export default {
  name: 'EditSupplyProduct',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonList,
    IonItemGroup,
    IonItem,
    IonInput,
    IonButton,
    IonButtons,
    IonIcon,
    IonFooter,
    IonSpinner,
    IonText,
    IonRow,
    IonCol,
    IonGrid,
    IonLabel,
    IonDatetime
  },
  props: {
    supplyProp: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      product: {
        quantity: '',
        total_buy_price: '',
        sale_price: '',
        created_at: ''
      },
      loading: false,
      errors: {
        quantity: { empty: false },
        total_buy_price: { empty: false }
      },
      close,
      arrowBackOutline,
      updatedSupply: null
    };
  },
  watch: {
    'product.total_buy_price'() {
      this.syncBuyPrice();
    },
    'product.quantity'() {
      this.syncBuyPrice();
    }
  },
  created() {
    if (!this.supplyProp) return;
    const s = this.supplyProp;
    this.product.quantity = String(s.quantity ?? '');
    this.product.total_buy_price = String(s.total_buy_price ?? '');
    
    // Correction pour iOS/Ionic Datetime (Retirer les microsecondes de Django : "Z" après 6 chiffres)
    let rawDate = s.created_at ?? new Date().toISOString();
    if (typeof rawDate === 'string') {
      rawDate = rawDate.replace(/(\.\d{3})\d+(Z)?$/, '$1$2');
    }
    this.product.created_at = rawDate;

    const sp = s.product?.sale_price ?? s.product?.product?.sale_price;
    const n = Number(sp);
    this.product.sale_price = (sp != null && sp !== '' && !isNaN(n) && n > 0) ? String(n) : '';
  },
  computed: {
    productName() {
      return this.supplyProp?.product?.name ?? this.supplyProp?.product?.product?.name ?? '—';
    },
    supplyId() {
      return this.supplyProp?.id ?? null;
    },
    productId() {
      const p = this.supplyProp?.product;
      return p?.id ?? p?.product?.id ?? null;
    },
    buyPriceDisplay() {
      const q = Number(this.product.quantity);
      const t = Number(this.product.total_buy_price);
      if (this.product.quantity === '' || this.product.total_buy_price === '' || isNaN(q) || isNaN(t) || q <= 0) return '—';
      const p = t / q;
      return (p != null && !isNaN(p) && p > 0) ? p.toFixed(0) : '—';
    },
    effectiveSalePrice() {
      const v = this.product.sale_price;
      return (v != null && v !== '') ? Number(v) : null;
    },
    buyPricePerUnit() {
      const q = Number(this.product.quantity);
      const t = Number(this.product.total_buy_price);
      if (!q || q <= 0 || isNaN(t)) return 0;
      return t / q;
    },
    benefitPerUnit() {
      const sale = this.effectiveSalePrice;
      const buy = this.buyPricePerUnit;
      if (sale == null || isNaN(sale)) return '—';
      const b = sale - buy;
      return (b > 0) ? b.toFixed(0) : '—';
    },
    benefitTotal() {
      const sale = this.effectiveSalePrice;
      const buy = this.buyPricePerUnit;
      const q = Number(this.product.quantity) || 0;
      if (sale == null || isNaN(sale) || q <= 0) return '—';
      const b = (sale - buy) * q;
      return (b > 0) ? b.toFixed(0) : '—';
    },
    hasBenefit() {
      const sale = this.effectiveSalePrice;
      return sale != null && !isNaN(sale) && sale > 0 && Number(this.product.quantity) > 0;
    },
    lastUpdatedAt() {
      const u = this.updatedSupply ?? this.supplyProp;
      const at = u?.updated_at;
      if (!at) return '';
      return this.datetime(at);
    }
  },
  methods: {
    datetime(val) {
      if (!val) return '—';
      try {
        const d = new Date(val);
        if (isNaN(d.getTime())) return String(val);
        const pad = (n) => String(n).padStart(2, '0');
        return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()}, ${pad(d.getHours())}:${pad(d.getMinutes())}`;
      } catch {
        return String(val);
      }
    },
    syncBuyPrice() {
      const q = Number(this.product.quantity);
      const t = Number(this.product.total_buy_price);
      const empty = this.product.quantity === '' || this.product.total_buy_price === '' || isNaN(q) || isNaN(t) || q <= 0;
      if (!empty) this.updateInfo();
    },
    updateInfo() {
      // computed buyPriceDisplay handles display
    },
    onSalePriceInput(e) {
      const v = e.detail?.value;
      if (v === '' || v === null || v === undefined || v === 0 || v === '0') {
        this.product.sale_price = '';
        return;
      }
      this.product.sale_price = String(v);
    },
    initErrors() {
      this.errors.quantity.empty = false;
      this.errors.total_buy_price.empty = false;
    },
    performClose() {
      return modalController.dismiss(null, 'cancel');
    },
    validateInputs() {
      this.initErrors();
      if (this.product.quantity === '' || this.product.quantity == null) {
        this.showTostMsg("Saisissez la quantité", "warning", 3000);
        return false;
      }
      if (this.product.total_buy_price === '' || this.product.total_buy_price == null) {
        this.showTostMsg("Saisissez le prix d'achat total", "warning", 3000);
        return false;
      }
      const q = Number(this.product.quantity);
      const t = Number(this.product.total_buy_price);
            if (isNaN(q) || q <= 0) {
                this.errors.quantity.empty = true;
                return false;
            }
      if (isNaN(t) || t < 0) {
        this.errors.total_buy_price.empty = true;
        return false;
      }
      if (!this.supplyId || !this.productId) {
        this.showTostMsg("Données d'achat indisponibles", "danger", 5000);
        return false;
      }
      return true;
    },
    async performSave() {
      if (!this.validateInputs()) return;
      this.loading = true;
      
      // Sécurisation des données pour éviter d'envoyer NaN (cause fréquente d'erreur 400)
      const quantity = Math.round(Number(this.product.quantity)) || 0;
      const total_buy_price = parseFloat(this.product.total_buy_price) || 0;
      const salePrice = Number(this.product.sale_price) || 0;
      
      const buyPrice = quantity > 0 ? total_buy_price / quantity : 0;

      try {
        const res = await suppliesService.updateSupply(this.supplyId, { 
          quantity, 
          total_buy_price,
          sale_price: salePrice,
          created_at: this.product.created_at 
        });
        this.updatedSupply = res?.data ?? null;
        if (salePrice != null && !isNaN(salePrice) && salePrice > 0) {
          await productsService.changeSalePrice(this.productId, salePrice, Math.round(buyPrice));
        }
        this.showTostMsg("Modification enregistrée. Date et heure de modification mises à jour.", "success", 5000);
        modalController.dismiss({ supply: this.updatedSupply }, 'confirm');
      } catch (err) {
        this.errorOrRefresh(err, () => this.performSave());
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
ion-header ion-buttons[slot="start"] ion-button.back-arrow-white,
ion-header ion-buttons[slot="start"] ion-button.back-arrow-white ion-icon {
  --color: #fff;
  color: #fff;
}
ion-content ion-list {
  ion-item { min-height: 70px; /* Responsive fix */ }
  .error { font-size: 0.75em !important; }
}
ion-footer ion-button {
  height: 2.5em;
  ion-text { font-size: 1.3em; font-weight: bold; }
  ion-spinner { margin-right: 0.9em; }
}
ion-buttons ion-icon { font-size: 24px; }
</style>
