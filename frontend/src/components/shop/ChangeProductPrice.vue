<!--
  * @file ChangeProductPrice.vue
  * @description Page pour la gestion de Change Product Price.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="change-price-back-btn" name="back-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>

        <ion-title color="light">Changement P.V : {{ productProp?.name }}</ion-title>

        <ion-buttons slot="end">
          <ion-button id="change-price-close-btn" name="close-button" @click="performClose">
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
                        id="price-old-value"
                        name="old_price"
                        label="Ancien prix de vente"
                        label-placement="stacked"
                        v-model="product.old_price"
                        placeholder="Ancien prix de vente" 
                        @keydown="initErros"
                        disabled="true"
                        type="number">
                      </ion-input>
                    </ion-item>
                  </div>
                  <div class="ion-margin-vertical">
                    <ion-item>
                      <ion-input 
                        id="price-new-value"
                        name="new_price"
                        label="Nouveau prix de vente"
                        label-placement="stacked"
                        v-model.number="product.new_price"
                        placeholder="Nouveau prix de vente" 
                        @keydown="initErros"
                        type="number"
                        autocomplete="off">
                      </ion-input>
                    </ion-item>
                    <ion-text v-if="errors.new_price.empty" class="error" color="danger">
                      * Prix négatif non permis
                    </ion-text>
                  </div>
                  <ion-button
                    color="secondary"
                    expand="block"
                    class="ion-margin-top"
                    :disabled="loading"
                    @click="validateSalePrice"
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
  IonTitle,
  IonLabel,
  IonText,
  IonContent,
  IonList,
  IonItemGroup,
  IonItem,
  IonButton,
  IonButtons,
  IonIcon,
  IonInput,
  modalController,
  IonSpinner,
  IonGrid,
  IonRow,
  IonCol
} from '@ionic/vue';

import {
  close,
  arrowBackOutline
} from 'ionicons/icons'
import { productsService } from '../../services/api'

/**
 * Composant ChangeProductPrice
 * - Gère l'interface et la logique métier de Change Product Price.
 */
export default {

  name: 'ChangeProductPrice',
  components:{
      IonPage,
      IonHeader,
      IonToolbar,
      IonTitle,
      IonLabel,
      IonText,
      IonContent,
      IonList,
      IonItemGroup,
      IonItem,
      IonButton,
      IonButtons,
      IonIcon,
      IonInput,
      IonSpinner,
      IonGrid,
      IonRow,
      IonCol
  },
  props:["productProp"],
  data() {
    return {
      buy_price:0,
      product:{
          new_price:0,
          old_price:0
      },
      loading:false,
      errors:{
          new_price:{
              empty:false,
              custom:false
          },
      },
      close,
      arrowBackOutline
    };
  },
  created(){
      this.product.old_price=this.productProp.sale_price
  },
  computed:{
      productId(){
          return this.productProp.id
      }
  },
  methods: {
      initErros(){
          this.errors.new_price.empty=false
      },
      performClose() {
        return modalController.dismiss(null, 'cancel');
      },
      validateInputs(){
          this.initErros()
          if(this.product.new_price <=0){
              this.errors.new_price.empty=true
              return false
          }
          if(this.product.new_price == this.product.old_price){
              this.showTostMsg("Prix identiques", "danger",5000)
              return false
          }
          if(!this.productId){
              this.showTostMsg("Produit non disponible", "danger",5000)
              return false
          }
          return true
      },
      validateSalePrice(){
          if(this.validateInputs()){
              this.loading=true
              productsService.changeSalePrice(this.productId, this.product.new_price, this.productProp.buy_price)
              .then(()=>{
                  this.loading=false
                  this.productProp.sale_price=this.product.new_price
                  this.showTostMsg("Opération réussie avec succès", "success",5000)
                  modalController.dismiss(null, "cancel")
              }).catch((err)=>{
                  this.loading=false
                  this.errorOrRefresh(err, () => this.validateSalePrice())
              })      
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
  ion-buttons[slot="start"] ion-button,
  ion-buttons[slot="start"] ion-button ion-icon {
    --color: #fff;
    color: #fff;
  }
}

ion-content {
    ion-list {
        ion-item{
          min-height: 70px; /* Responsive fix */
        }
        .error {
            font-size: 0.75em !important;
        }
    }
}

ion-buttons ion-icon {
    font-size: 24px;
}
 
</style>