<!--
  * @file StockProduct.vue
  * @description Page pour la gestion de Stock Product.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="primary">
          <ion-buttons slot="start">
            <ion-button id="stock-product-back-btn" name="back-button" class="back-arrow-white" @click="performClose" fill="clear">
              <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
            </ion-button>
          </ion-buttons>
          <ion-title color="light">Stock de : {{ productProp?.name }} {{ money(productProp?.sale_price) }} BIF</ion-title>
          <ion-buttons slot="end">
            <ion-button id="stock-product-close-btn" name="close-button" color="light" @click="performClose">
              <ion-icon :icon="close"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
  
    <ion-content class="ion-padding">
      <ion-grid fixed>
        <ion-row class="ion-justify-content-center">
          <ion-col size="12">
            <ion-list class="ion-margin-top" v-if="stocks.length>0">
              <ion-item v-for="stock in stocks" :key="stock.id">
                <ion-thumbnail slot="start">
                  <img src="../../assets/avatar.png" />
                </ion-thumbnail>
                <ion-label>
                  {{stock?.product.name}}
                  <p>Quantité : {{stock?.quantity}}</p>
                  <p>
                    <ion-text color="primary">Date : {{datetime(stock?.created_at)}}</ion-text>
                  </p>
                </ion-label>
              </ion-item>
            </ion-list>
            <div v-else class="ion-text-center ion-padding">
              <ion-text color="medium">Aucun mouvement de stock trouvé.</ion-text>
            </div>
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
    IonSelect,
    IonFooter
  } from '@ionic/vue';

  import {
    close,
    arrowBackOutline
  } from 'ionicons/icons'
  import { productsService } from '../../services/api'
  
  /**
 * Composant StockProduct
 * - Gère l'interface et la logique métier de Stock Product.
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
        IonFooter
    },
    props:["productProp"],
    data() {
      return {
        stocks:[],
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
    created(){
        this.fetchStockProduit()
    },
    computed:{
        productId(){
            return this.productProp.id
        }
    },
    methods: {
        initErros(){
            this.errors.name.empty=false
            this.errors.quantity.empty=false
            this.errors.sale_price.empty=false
        },
        performClose() {
          return modalController.dismiss(null, 'cancel');
        },
        fetchStockProduit(){
            this.loading=true
            productsService.getProductStock(this.productId)
            .then((res)=>{
                this.stocks = res.data
            }).catch((err)=>{
                this.loading=false
                this.errorOrRefresh(err, () => this.fetchStockProduit())
            })      
            
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
            height: 150px;
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
  