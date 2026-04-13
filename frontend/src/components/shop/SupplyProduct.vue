<!--
  * @file SupplyProduct.vue
  * @description Page pour la gestion de Supply Product.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="primary">
          <ion-buttons slot="start">
            <ion-button id="supply-product-back-btn" name="back-button" @click="performClose">
              <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
            </ion-button>
          </ion-buttons>

          <ion-title color="light">Achat : {{ productProp?.name }}</ion-title>

          <ion-buttons slot="end">
            <ion-button id="supply-product-close-btn" name="close-button" @click="performClose">
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
                        id="supply-quantity"
                        name="quantity"
                        label="Quantité"
                        label-placement="stacked"
                        v-model="product.quantity"
                        placeholder="Quantité" 
                        @keydown="initErros"
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
                        id="supply-total-buy-price"
                        name="total_buy_price"
                        label="Prix d'achat total"
                        label-placement="stacked"
                        v-model="product.total_buy_price"
                        placeholder="Prix d'achat total" 
                        @keydown="initErros"
                        @change="updateInfo"
                        type="number"
                        autocomplete="off">
                      </ion-input>
                    </ion-item>
                    <ion-text v-if="errors.total_buy_price.empty" class="error" color="danger">
                      * Valeurs négatives non permises
                    </ion-text>
                  </div>
                  <div class="ion-margin-vertical">
                    <ion-item>
                      <ion-input 
                        id="supply-sale-price"
                        name="sale_price"
                        label="Prix de vente unitaire"
                        label-placement="stacked"
                        :value="product.sale_price"
                        @ionInput="onSalePriceInput"
                        placeholder="Prix de vente unitaire (BIF)" 
                        @keydown="initErros"
                        type="number"
                        min="0"
                        autocomplete="off">
                      </ion-input>
                    </ion-item>
                  </div>
                  <div class="ion-margin-vertical">
                    <ion-text>P.A.U : {{ buyPriceDisplay === '—' ? '' : buyPriceDisplay + ' BIF' }}</ion-text>
                  </div>
                  <div class="ion-margin-vertical" v-if="hasBenefit">
                    <ion-text color="success" class="ion-display-block">Bénéfice unitaire : {{ benefitPerUnit }} BIF</ion-text>
                    <ion-text color="success" class="ion-display-block">Bénéfice total : {{ benefitTotal }} BIF</ion-text>
                  </div>
                  <ion-button
                    color="secondary"
                    expand="block"
                    class="ion-margin-top"
                    :disabled="loading"
                    @click="perfromSupplyProduct"
                  >
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
    IonSegment,
    IonSegmentButton,
    IonTitle,
    IonLabel,
    IonText,
    IonContent,
    IonList,
    IonItemGroup,
    IonItem,
    IonThumbnail,
    IonButton,
    IonButtons,
    IonBackButton,
    IonIcon,
    IonInput,
    modalController,
    IonFooter,
    IonSpinner,
    IonRow,
    IonGrid,
    IonCol
  } from '@ionic/vue';

  import {
    close,
    arrowBackOutline
  } from 'ionicons/icons'
  import { productsService } from '../../services/api'
  
  /**
 * Composant SupplyProduct
 * - Gère l'interface et la logique métier de Supply Product.
 */
export default {
  
    name: 'TransactionsView',
    components:{
        IonPage,
        IonHeader,
        IonToolbar,
        IonSegment,
        IonSegmentButton,
        IonTitle,
        IonLabel,
        IonText,
        IonContent,
        IonList,
        IonItemGroup,
        IonItem,
        IonThumbnail,
        IonButton,
        IonButtons,
        IonIcon,
        IonInput,
        IonBackButton,
        IonFooter,
        IonSpinner,
        IonRow,
        IonGrid,
        IonCol
    },
    props:["productProp"],
    data() {
      return {
        buy_price: '',
        product: {
            quantity: '',
            buy_price: '',
            total_buy_price: '',
            sale_price: ''
        },
        loading:false,
        errors:{
            name:{
                empty:false,
                custom:false
            },
            total_buy_price:{
                empty:false,
                custom:false
            },
            quantity:{
                empty:false,
                custom:false
            },
            sale_price:{
                empty:false,
                custom:false
            },
        },
        close,
        arrowBackOutline
      };
    },
    watch: {
        "product.total_buy_price"(newVal) {
            this.syncBuyPrice();
        },
        "product.quantity"() {
            this.syncBuyPrice();
        },
    },
    created() {
      const sp = this.productProp?.sale_price;
      const n = Number(sp);
      const hasPrice = sp != null && sp !== '' && !isNaN(n) && n > 0;
      this.product.sale_price = hasPrice ? String(n) : '';
    },
    computed: {
        productId() {
            return this.productProp?.id;
        },
        benefitPerUnit() {
            const sale = this.effectiveSalePrice;
            const buy = Number(this.buy_price) || 0;
            if (sale == null || sale === '' || isNaN(sale)) return '—';
            const b = sale - buy;
            return (b > 0) ? b.toFixed(0) : '—';
        },
        benefitTotal() {
            const sale = this.effectiveSalePrice;
            const buy = Number(this.buy_price) || 0;
            const q = Number(this.product.quantity) || 0;
            if (sale == null || sale === '' || isNaN(sale) || q <= 0) return '—';
            const b = (sale - buy) * q;
            return (b > 0) ? b.toFixed(0) : '—';
        },
        hasBenefit() {
            const sale = this.effectiveSalePrice;
            return sale != null && sale !== '' && !isNaN(sale) && Number(this.product.quantity) > 0;
        },
        effectiveSalePrice() {
            const v = this.product.sale_price;
            return (v != null && v !== '') ? Number(v) : null;
        },
        buyPriceDisplay() {
            const q = Number(this.product.quantity);
            const t = Number(this.product.total_buy_price);
            if (this.product.quantity === '' || this.product.total_buy_price === '' || isNaN(q) || isNaN(t) || q <= 0) return '—';
            const p = t / q;
            return (p != null && !isNaN(p) && p > 0) ? p.toFixed(0) : '—';
        }
    },
    methods: {
        syncBuyPrice() {
            const q = Number(this.product.quantity);
            const t = Number(this.product.total_buy_price);
            const empty = this.product.quantity === '' || this.product.total_buy_price === '' || isNaN(q) || isNaN(t) || q <= 0;
            this.buy_price = empty ? '' : (t / q).toFixed(0);
        },
        updateInfo() {
            this.syncBuyPrice();
        },
        onSalePriceInput(e) {
            const v = e.detail?.value;
            if (v === '' || v === null || v === undefined || v === 0 || v === '0') {
                this.product.sale_price = '';
                return;
            }
            this.product.sale_price = String(v);
        },
        initErros(){
            this.errors.name.empty = false;
            this.errors.quantity.empty = false;
            this.errors.total_buy_price.empty = false;
            this.errors.sale_price.empty = false;
        },
        performClose() {
          return modalController.dismiss(null, 'cancel');
        },
        validateInputs() {
            this.initErros();
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
            if (isNaN(q) || q < 0) {
                this.errors.quantity.empty = true;
                return false;
            }
            if (isNaN(t) || t < 0) {
                this.errors.total_buy_price.empty = true;
                return false;
            }
            if (!this.productId) {
                this.showTostMsg("Produit non disponible", "danger", 5000);
                return false;
            }
            return true;
        },
        async perfromSupplyProduct(){
            if (!this.validateInputs()) return;
            this.loading = true;
            const quantity = Number(this.product.quantity);
            const total_buy_price = parseFloat(this.product.total_buy_price);
            const salePrice = this.effectiveSalePrice;
            const buyPrice = quantity > 0 ? total_buy_price / quantity : 0;
            try {
                await productsService.supplyProduct(this.productId, { quantity, total_buy_price });
                if (salePrice != null && !isNaN(salePrice) && salePrice > 0) {
                    await productsService.changeSalePrice(this.productId, salePrice, Math.round(buyPrice));
                }
                this.productProp.quantity = (this.productProp.quantity || 0) + parseInt(this.product.quantity, 10);
                this.showTostMsg("Opération réussie avec succès", "success", 5000);
                modalController.dismiss(null, "cancel");
            } catch (err) {
                this.errorOrRefresh(err, () => this.perfromSupplyProduct());
            } finally {
                this.loading = false;
            }
        }
    },
  
  };
  </script>
  
  <style lang="scss" scoped>
  
  ion-header {
    ion-toolbar {
      --border-radius: 16px 16px 0 0;
    }
    ion-buttons[slot="start"] ion-button.back-arrow-white,
    ion-buttons[slot="start"] ion-button.back-arrow-white ion-icon {
      --color: #fff;
      color: #fff;
    }
  }
  
  ion-content {
      ion-list {
          ion-item{
            min-height: 70px; /* Responsive fix */
          }
      }
  }

  ion-footer {
    ion-row {
        background: transparent;
        display: block;
        ion-fab-button {
            margin-right: 2.5vh;
        }
        ion-list {
            border-radius: 20px 20px 0 0;
            ion-list-header {
                ion-label {
                    font-weight: bold;
                    font-size: 1.8em;
                }
            }
            ion-input, ion-text {
                font-size: 1em;
            }
        
            ion-button{
              height: 2.5em;
              ion-text{
                font-size: 1.3em;
                font-weight: bold;
              }
              ion-spinner{
                margin-right: 0.9em;
              }
            }
            
            .error {
                font-size: 0.75em !important;
            }
        }
    }
}
  ion-buttons {
    margin-right: 2em;
      ion-icon{
      font-size:24px;
      color: var(--ion-color-primary);
      }
  }
   
  </style>
  