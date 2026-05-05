<!--
  * @file ControlProducts.vue
  * @description Page pour la gestion de Control Products.
  * @author Kora Agency
-->
<template>
    <ion-page>
   <ion-header class="ion-no-border">
     <ion-toolbar color="secondary">
       <ion-buttons slot="start">
         <ion-button @click="$router.push({name:'shop'})">
           <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
         </ion-button>
       </ion-buttons>

        <ion-title color="light">
          <div class="header-title-container">
            <span>Contrôles</span>
          </div>
        </ion-title>

       <ion-buttons slot="end">
         <ion-button @click="fetchProducts">
           <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
         </ion-button>
         <ion-button @click="openControlFrequency">
           <ion-icon color="light" size="large" :icon="timer"></ion-icon>
         </ion-button>
       </ion-buttons>
     </ion-toolbar>
   </ion-header>
 
 <ion-content>
    <ion-searchbar 
      v-model="searchTerm" 
      placeholder="Rechercher un produit..." 
      animated="true"
      class="ion-padding-horizontal"
      style="--background: #f1f5f9; --border-radius: 12px; margin-top: 10px;"
    ></ion-searchbar>

   <ion-list-header v-if="filteredControlledProducts.length>0"> Déjà controlés </ion-list-header>
 
     <div class="scroll-container ion-margin" v-if="filteredControlledProducts.length>0" >
       <ion-card color="light" v-for="product in filteredControlledProducts" :key="product.id">
         <ion-badge
           color="light"
           style="position: absolute;top: 0;right: 0;"
         >
         <ion-icon size="large" color="success" :icon="checkmarkCircle"></ion-icon>
         </ion-badge>
         <ion-badge
           color="light"
           style="position: absolute; top: 0; left: 0; padding: 0; border-radius: 50%;"
           @click.stop="confirmCancelControl(product)"
         >
           <ion-icon size="large" color="danger" :icon="closeCircle"></ion-icon>
         </ion-badge>
         <img :src="product.product.image" />
          <ion-label>
            {{product.name}}
            <p class="art-cat">{{ getCategoryLabel(product) }}</p>
          </ion-label>
       </ion-card>
     </div>

    <ion-list-header> Non controlés ({{ filteredUnControlledProducts.length }}) </ion-list-header>

    <div class="ion-margin" v-if="filteredUnControlledProducts.length>0">
      <ion-item
        v-for="product in filteredUnControlledProducts"
        :key="product.id"
        @click="performControlProduct(product)"
        >
        <ion-thumbnail slot="start">
          <img :src="product.product.image" />
        </ion-thumbnail>

        <ion-label>
          {{product.name}}
          <p class="art-cat">{{ getCategoryLabel(product) }}</p>
          <p>Quantité : {{product?.quantity}}</p>
            <p>
              <ion-text color="primary">P.T : {{money(product?.sale_price*product.quantity)}} BIF</ion-text>
            </p>
            <p>
              <ion-text color="secondary">Bénéfice : {{
                money(
                product?.sale_price*product.quantity-
                product?.buy_price*product.quantity
                )
              }} BIF</ion-text>
            </p>
        </ion-label>
        <ion-icon size="large" color="danger" :icon="close" slot="end"></ion-icon>
      </ion-item>
    </div>
    <div v-else class="ion-padding ion-text-center">
       <ion-text color="medium">Aucun produit trouvé</ion-text>
    </div>

 </ion-content>
</ion-page>
 </template>
 
 <script>
 import {
   IonHeader,
   IonPage,
   modalController,
   alertController,
   IonToolbar,
   IonButtons,
   IonButton,
   IonIcon,
   IonBadge,
   IonText,
   IonContent,
   IonItem,
   IonLabel,
   IonThumbnail,
   IonListHeader,
   IonRow,
   IonCol,
   IonCard,
   IonTitle,
   IonFab,
   IonFabButton,
   IonList,
   IonPopover,
   IonSearchbar
   
 } from '@ionic/vue';
 
 import {
   cartOutline,
   exitOutline,
   home,
   addOutline,
   fastFoodOutline,
   personOutline,
   ellipsisVertical,
   arrowBackOutline,
   refreshCircleOutline,
   checkmarkCircle,
   star,
   close,
   closeCircle,
   timer,
 } from 'ionicons/icons'
import ControlProduct from '../../components/shop/ControlProduct.vue';
import ControlFrequency from '../../components/shop/ControlFrequency.vue';
import { productsService, categoriesService, subCategoriesService } from '../../services/api';
import globalMixins from '../../composables/mixins';
 
 /**
 * Composant ControlProducts
 * - Gère l'interface et la logique métier de Control Products.
 */
export default {
   mixins: [globalMixins],
   components:{
     IonHeader,
     IonPage,
     IonToolbar,
     IonButtons,
     IonButton,
     IonIcon,
     IonBadge,
     IonText,
     IonContent,
     IonItem,
     IonLabel,
     IonThumbnail,
     IonListHeader,
     IonRow,
     IonCol,
     IonCard,
     IonTitle,
     IonFab,
     IonFabButton,
     IonList,
     IonPopover,
     IonSearchbar
   },
   data(){
     return{
       cartOutline,
       home,
       exitOutline,
       addOutline,
       ellipsisVertical,
       personOutline,
       fastFoodOutline,
       shop:this.$store.state.shop,
       arrowBackOutline,
       refreshCircleOutline,
       checkmarkCircle,
       controlledProducts:[],
       unControlledProducts:[],
       star,
       close,
       closeCircle,
       timer,
       categories: [],
       searchTerm: "",
     }
   },
   computed:{
        shopId(){
            return this.shop ? this.shop.id : null
        },
        filteredControlledProducts() {
            if (!this.searchTerm) return this.controlledProducts;
            const search = this.searchTerm.toLowerCase();
            return this.controlledProducts.filter(p => 
                p.name.toLowerCase().includes(search) || 
                (p.product && p.product.name.toLowerCase().includes(search))
            );
        },
        filteredUnControlledProducts() {
            if (!this.searchTerm) return this.unControlledProducts;
            const search = this.searchTerm.toLowerCase();
            return this.unControlledProducts.filter(p => 
                p.name.toLowerCase().includes(search) || 
                (p.product && p.product.name.toLowerCase().includes(search))
            );
        }
    },
    beforeMount(){
        this.$store.state.shop = this.getShopFromLocalStorage()
        this.shop = this.$store.state.shop
        this.checkCurrentShop()
        if(this.$store.state.products.length<=0)
            this.fetchProducts()
        else{
          this.controlledProducts = this.$store.state.products.filter(x=>x.controlled)
          this.unControlledProducts = this.$store.state.products.filter(x=>x.controlled==false && x.quantity>0)
        }
        this.fetchCategories();
    },

   methods:{
       fetchProducts(){
           if (!this.shopId) return;
           productsService.getProducts(this.shopId)
           .then((res)=>{
               this.$store.state.products=res.data.results
               this.controlledProducts = this.$store.state.products.filter(x=>x.controlled)
               this.unControlledProducts = this.$store.state.products.filter(x=>x.controlled==false && x.quantity>0)
           }).catch((err)=>{
               this.errorOrRefresh(err, () => this.fetchProducts())
           }) 
       },
       async fetchCategories() {
         try {
           const res = await categoriesService.getCategories();
           this.categories = res.data.results || res.data || [];
         } catch (err) {
           console.error("[ControlProducts] Erreur catégories:", err);
         }
       },
       controlProduct(product){
        if(product.quantity<=0)
          this.showTostMsg("Kontrole ntikunda, stoke ingana na 0", "danger",5000)
        else
          this.performControlProduct(product)
       },
       async performControlProduct(product) {
           const modal = await modalController.create({
               initialBreakpoint:1,
               component: ControlProduct,
               componentProps:{productProp:product}
           });
           modal.present();

           const { data, role } = await modal.onWillDismiss();

           if (role === 'confirm') {
                this.fetchProducts()
           }        
       },

       async openControlFrequency() {
           const modal = await modalController.create({
               initialBreakpoint: 1,
               component: ControlFrequency,
           });
           modal.present();
           const { data, role } = await modal.onWillDismiss();
           if (role === 'confirm') this.fetchProducts();
       },
       async confirmCancelControl(product) {
           const alert = await alertController.create({
               header: 'Annuler le contrôle ?',
               message: `Voulez-vous vraiment annuler le contrôle de "${product.name}" ? Le stock sera restauré et la vente associée sera supprimée.`,
               buttons: [
                   {
                       text: 'Non',
                       role: 'cancel'
                   },
                   {
                       text: 'Oui, annuler',
                       role: 'confirm',
                       handler: () => {
                           this.cancelControl(product);
                       }
                   }
               ]
           });
           await alert.present();
       },
       cancelControl(product) {
           productsService.cancelControl(product.id)
               .then(() => {
                   this.showTostMsg("Contrôle annulé avec succès", "success", 3000);
                   this.fetchProducts();
               })
               .catch((err) => {
                   this.errorOrRefresh(err, () => this.cancelControl(product));
               });
       },
   }
}
</script>

<style lang="scss" scoped>
ion-header {
  ion-toolbar {
    --background: white;
    ion-badge {
      position: absolute;
      top: 0;
      right: 0;
      border-radius: 50%;
      margin: 0 -0.3rem 0 0;
      display: flex;
      align-items: center;
      justify-content: center;
      ion-text {
        font-size: 0.6rem;
        font-weight: bold;
      }
      ion-icon{
       font-size:44px;
      }
    }
  }
}

ion-item {
  ion-label {
    font-size: 1.4rem;
    font-weight: bold;

    .art-cat {
      font-size: 0.8rem;
      color: #64748b;
      font-weight: 600;
      margin-top: 2px;
      display: block;
    }

    p {
      margin-top: 5px;
      font-size: 0.9rem;
      font-weight: normal;
    }
  }
}

img {
  margin-bottom: 0px;
  border-radius: 10px;
   width: 100%;
}

ion-list-header {
  font-size: 1.1rem;
  font-weight: normal;
}

ion-card {
  box-shadow: none;
  margin: 10px 5px;
  height: 15vh;
  flex-direction: column;
  ion-thumbnail {
    border-radius: 10px;
    width: 3rem;
    height: 3rem;
    margin-bottom: 1.3vh;
    ion-icon {
      font-size: 2rem;
    }
  }
  ion-label {
    font-size: 1rem;
    font-weight: 500;
  }
}

ion-card, ion-thumbnail {
  display: flex;
  align-items: center;
  justify-content: center;
}

ion-fab{
    position:absolute;
    bottom:72px !important;
    right: 1em !important; z-index: 10001 !important;
    ion-fab-button{
      ion-icon{
        color:white
      }
      
    }
}

ion-buttons {
    ion-icon{
    font-size:24px;
    color: white;
    }
}

.scroll-container {
 display: flex;
 overflow-x: auto;
 scroll-snap-type: x mandatory; /* Ensures smooth scrolling */
 gap: 10px; /* Adds space between images */
 padding: 10px;
 height:300px;
 white-space: nowrap;
}

.scroll-container ion-card {
 flex: 0 0 auto; /* Prevents shrinking */
 width: 250px; /* Adjust width as needed */
 scroll-snap-align: start; /* Snaps cards into place */
 height:300px;
 width:150px;
}

</style>
