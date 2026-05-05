<!--
  * @file ControlProduct.vue
  * @description Page pour la gestion de Control Product.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="primary">
          <ion-buttons slot="start">
            <ion-button id="control-product-back-btn" name="back-button" class="back-arrow-white" @click="performClose" fill="clear">
              <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
            </ion-button>
          </ion-buttons>
          <ion-title color="light">Contrôler : {{ productProp?.name }} {{ money(productProp?.sale_price) }} BIF</ion-title>
          <ion-buttons slot="end">
            <ion-button id="control-product-close-btn" name="close-button" color="light" @click="performClose">
              <ion-icon :icon="close"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
  
      <ion-content >
  
        <ion-footer class="ion-no-border">
            <ion-row>
                <ion-list lines="full">
                <ion-item-group class="ion-margin-horizontal ion-margin-bottom">
                    <form >                    
                    <div class="ion-margin-vertical">
                        <ion-label>Quantité restante : </ion-label>
                        <ion-item>
                            <ion-input 
                                id="control-quantity-rest"
                                name="quantity"
                                aria-label="Quantité restante"
                                v-model="product.quantity"
                                placeholder="Quantité restante" 
                                @keydown="initErros"
                                type="number">
                            </ion-input>
                        </ion-item>
                        <ion-text v-if="errors.quantity.empty" class="error" color="danger">
                            * Quantité négative non permise
                        </ion-text>
                        <ion-text v-if="errors.quantity.custom" class="error" color="danger">
                            * La quantité restante ne doit pas dépasser {{ productProp?.quantity }}
                        </ion-text>
                        <div class="ion-margin-top">
                            <ion-text>Quantité disponible : {{ productProp.quantity }}</ion-text>
                        </div>
                        <div>
                            <ion-text>Quantité restante : {{ product.quantity }}</ion-text>
                        </div>
                        <div>
                            <ion-text>Quantité écoulée : {{ qtSold }}</ion-text>
                        </div>
                        <div>
                            <ion-text>Prix total : {{ money(prixTotal) }} BIF</ion-text>
                        </div>
                        <div class="ion-margin-bottom">
                            <ion-text color="primary">Bénéfice : {{ money(benefice) }} BIF</ion-text>
                        </div>
                    </div>
                    <ion-button
                        color="secondary"
                        expand="block"
                        :disabled="loading"
                        @click="perfromControlProduct"
                    >
                        <ion-spinner v-if="loading" slot="start"></ion-spinner>
                        <ion-text color="light" >Valider</ion-text>
                    </ion-button>
                    </form>
                </ion-item-group>
                </ion-list>
            </ion-row>

            </ion-footer>
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
    IonSelect,
    IonFooter,
    IonRow,
    IonSpinner
  } from '@ionic/vue';

  import {
    close,
    arrowBackOutline
  } from 'ionicons/icons'
  import { productsService } from '../../services/api'
  
  /**
 * Composant ControlProduct
 * - Gère l'interface et la logique métier de Control Product.
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
        IonSelect,
        IonFooter,
        IonRow,
        IonSpinner
    },
    props:["productProp"],
    data() {
      return {
        product:{
            quantity:0,
        },
        loading:false,
        errors:{
            name:{
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
    computed: {
        productId() {
            return this.productProp?.id;
        },
        qtSold() {
            const avail = Number(this.productProp?.quantity);
            const rest = Number(this.product.quantity);
            if (isNaN(avail) || isNaN(rest)) return 0;
            return Math.max(0, avail - rest);
        },
        prixTotal() {
            const sale = Number(this.productProp?.sale_price) || 0;
            return sale * this.qtSold;
        },
        benefice() {
            const sale = Number(this.productProp?.sale_price) || 0;
            const buy = Number(this.productProp?.buy_price) || 0;
            return (sale - buy) * this.qtSold;
        },
    },
    created(){
        if(this.productProp)
            this.product.quantity=this.productProp.quantity
    },
    methods: {
        initErros(){
            this.errors.name.empty = false;
            this.errors.quantity.empty = false;
            this.errors.quantity.custom = false;
            this.errors.sale_price.empty = false;
        },
        performClose() {
          return modalController.dismiss(null, 'cancel');
        },
        validateInputs() {
            this.initErros();
            const q = Number(this.product.quantity);
            if (this.product.quantity === '' || this.product.quantity == null || isNaN(q)) {
                this.showTostMsg("Saisissez la quantité restante", "warning", 3000);
                return false;
            }
            if (q < 0) {
                this.errors.quantity.empty = true;
                return false;
            }
            const max = Number(this.productProp?.quantity);
            if (!isNaN(max) && q > max) {
                this.errors.quantity.custom = true;
                return false;
            }
            if (!this.productId) {
                this.showTostMsg("Produit non disponible", "danger", 5000);
                return false;
            }
            return true;
        },
        perfromControlProduct(){
            if (!this.validateInputs()) return;
            const quantity = parseFloat(this.product.quantity);
            if (isNaN(quantity)) {
                this.showTostMsg("Quantité invalide", "warning", 3000);
                return;
            }
            this.loading = true;
            productsService.controlProduct(this.productId, quantity)
                .then((res) => {
                    this.loading = false;
                    this.productProp.quantity = quantity;
                    this.productProp.controlled = true;
                    this.showTostMsg("Opération réussie", "success", 5000);
                    modalController.dismiss(this.productProp, "confirm");
                })
                .catch((err) => {
                    this.loading = false;
                    const status = err?.response?.status;
                    const data = err?.response?.data || {};
                    if (status === 400) {
                        const msg = data.details
                            || data.detail
                            || (Array.isArray(data.quantity) ? data.quantity[0] : data.quantity)
                            || data.message
                            || "Erreur lors du contrôle";
                        this.showTostMsg(String(msg), "danger", 5000);
                        return;
                    }
                    this.errorOrRefresh(err, () => this.perfromControlProduct());
                });
        }
    },
  
  };
  </script>
  
  <style lang="scss" scoped>
  
  ion-header {
    ion-toolbar {
      --border-radius: 16px 16px 0 0;
      --background: white;
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
  