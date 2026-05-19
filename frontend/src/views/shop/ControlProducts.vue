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

   <ion-list-header v-if="filteredControlledProducts.length>0">
     Déjà contrôlés ({{ filteredControlledProducts.length }})
   </ion-list-header>
 
   <div class="scroll-container ion-margin" v-if="filteredControlledProducts.length>0">
     <div class="controlled-card" v-for="product in filteredControlledProducts" :key="product.id">
       <!-- Badge Check (En haut à droite) -->
       <div class="card-action-badge top-right success">
         <ion-icon color="success" :icon="checkmarkCircle"></ion-icon>
       </div>
       <!-- Badge Cancel (En haut à gauche) -->
       <div class="card-action-badge top-left danger" @click.stop="confirmCancelControl(product)">
         <ion-icon color="danger" :icon="closeCircle"></ion-icon>
       </div>
       <!-- Badge Historique (En bas à droite) -->
       <div class="card-action-badge bottom-right primary" @click.stop="openSupplyHistory(product)">
         <ion-icon color="primary" :icon="receiptOutline"></ion-icon>
       </div>
       
       <!-- Image Container -->
       <div class="controlled-card-img-container">
         <ion-img :src="productImage(product)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
       </div>
       
       <!-- Infos Produit -->
       <div class="controlled-card-info">
         <div class="controlled-card-name">{{ product.name }}</div>
         <p class="controlled-card-cat">{{ getCategoryLabel(product) }}</p>
       </div>
     </div>
   </div>

    <ion-list-header> Non controlés ({{ filteredUnControlledProducts.length }}) </ion-list-header>

    <div class="ion-margin" v-if="filteredUnControlledProducts.length>0">
      <ion-item
        v-for="product in filteredUnControlledProducts"
        :key="product.id"
        @click="performControlProduct(product)"
        >
        <ion-thumbnail slot="start">
          <ion-img :src="productImage(product)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
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
        <ion-buttons slot="end">
          <ion-button fill="clear" @click.stop="openSupplyHistory(product)" title="Historique des achats">
            <ion-icon color="primary" :icon="receiptOutline"></ion-icon>
          </ion-button>
          <ion-icon size="large" color="danger" :icon="close"></ion-icon>
        </ion-buttons>
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
   IonSearchbar,
   IonImg
   
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
   receiptOutline,
 } from 'ionicons/icons'
import ControlProduct from '../../components/shop/ControlProduct.vue';
import ControlFrequency from '../../components/shop/ControlFrequency.vue';
import ProductSupplyHistory from '../../components/shop/ProductSupplyHistory.vue';
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
     IonSearchbar,
     IonImg
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
       receiptOutline,
       categories: [],
       searchTerm: "",
       searchTimeout: null,
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
                  (p.name || '').toLowerCase().includes(search) || 
                  (p.product && (p.product.name || '').toLowerCase().includes(search))
              );
          },
          filteredUnControlledProducts() {
              if (!this.searchTerm) return this.unControlledProducts;
              const search = this.searchTerm.toLowerCase();
              return this.unControlledProducts.filter(p => 
                  (p.name || '').toLowerCase().includes(search) || 
                  (p.product && (p.product.name || '').toLowerCase().includes(search))
              );
          }
    },
    beforeMount(){
        this.$store.state.shop = this.getShopFromLocalStorage()
        this.shop = this.$store.state.shop
        this.checkCurrentShop()
    },
    ionViewWillEnter(){
        this.fetchProducts();
        this.fetchCategories();
    },

   methods:{
       fetchProducts(){
           if (!this.shopId) return;
           const allProducts = [];
           const fetchPage = (page = 1) => {
               productsService.getProducts(this.shopId, { page, page_size: 500 })
               .then((res)=>{
                   const results = res.data.results || res.data || [];
                   allProducts.push(...results);
                   
                   if (res.data.next) {
                       fetchPage(page + 1);
                   } else {
                       this.$store.state.products = allProducts;
                       this.controlledProducts = this.$store.state.products.filter(x=>x.controlled);
                       this.unControlledProducts = this.$store.state.products.filter(x=>x.controlled==false && x.quantity>0);
                   }
               }).catch((err)=>{
                   this.errorOrRefresh(err, () => this.fetchProducts())
               })
           };
           fetchPage(1);
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
       async openSupplyHistory(product) {
            const modal = await modalController.create({
                component: ProductSupplyHistory,
                componentProps: { productProp: product },
                initialBreakpoint: 0.85,
                breakpoints: [0, 0.85, 1],
            });
            await modal.present();
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
  gap: 15px;
  padding: 10px 5px;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
  scroll-snap-type: x mandatory;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.controlled-card {
  position: relative;
  flex: 0 0 135px;
  width: 135px;
  height: 185px;
  scroll-snap-align: start;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 12px 8px;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.controlled-card-img-container {
  width: 75px;
  height: 75px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
}

.controlled-card-img-container ion-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.controlled-card-info {
  width: 100%;
  text-align: center;
}

.controlled-card-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.controlled-card-cat {
  font-size: 0.75rem;
  color: #64748b;
  margin: 2px 0 0 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-action-badge {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  z-index: 10;
  border: 1px solid rgba(0, 0, 0, 0.03);
}

.card-action-badge ion-icon {
  font-size: 22px;
}

.card-action-badge.top-right {
  top: -4px;
  right: -4px;
}

.card-action-badge.top-left {
  top: -4px;
  left: -4px;
}

.card-action-badge.bottom-right {
  bottom: 6px;
  right: 6px;
  width: 26px;
  height: 26px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.card-action-badge.bottom-right ion-icon {
  font-size: 16px;
}

</style>
