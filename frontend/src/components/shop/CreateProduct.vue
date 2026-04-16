<!--
  * @file CreateProduct.vue
  * @description Page pour la gestion de Create Product.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="primary">
          <ion-buttons slot="start">
            <ion-button id="create-product-back-btn" name="back-button" @click="performClose">
              <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
            </ion-button>
          </ion-buttons>

          <ion-title color="light">Ajout produit</ion-title>

          <ion-buttons slot="end">
            <ion-button id="create-product-close-btn" name="close-button" @click="performClose">
              <ion-icon color="light" size="large" :icon="close"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
  
      <ion-content class="ion-padding">
        <ion-grid fixed>
          <ion-row class="ion-justify-content-center">
            <ion-col size="12" class="form-grid-col">
              <div class="form-container">
                <form @submit.prevent="perfromCreateProduct">
                  
                  <!-- Catégorie -->
                  <div class="ion-margin-vertical">
                    <ion-label for="product-category" position="stacked" class="custom-label">Catégorie</ion-label>
                    <ion-item class="custom-item">
                      <ion-select
                        id="product-category"
                        name="category"
                        interface="popover"
                        :interface-options="{header: 'Veuillez choisir la catégorie'}"
                        v-model="category"
                        placeholder="Sélectionner une catégorie"
                      >
                        <ion-select-option 
                          v-for="item in categories"
                          :key="item.id"
                          :value="item.id">{{item.name}}</ion-select-option>
                      </ion-select>
                    </ion-item>
                    <ion-text v-if="errors.category.empty" class="error-text" color="danger">
                      * Veuillez choisir la catégorie
                    </ion-text>
                  </div>

                  <!-- Sous-Catégorie -->
                  <div class="ion-margin-vertical">
                    <ion-label for="product-sub-category" position="stacked" class="custom-label">Sous-Catégorie</ion-label>
                    <ion-item class="custom-item">
                      <ion-select
                        id="product-sub-category"
                        name="sub_category"
                        interface="popover"
                        :interface-options="{header: 'Veuillez sélectionner la sous-catégorie'}"
                        v-model="sub_category"
                        placeholder="Sélectionner une sous-catégorie"
                      >
                        <ion-select-option 
                          v-for="item in sub_categories"
                          :key="item.id"
                          :value="item.id">{{item.name}}</ion-select-option>
                      </ion-select>
                    </ion-item>
                    <ion-text v-if="errors.sub_category.empty" class="error-text" color="danger">
                      * Veuillez choisir la sous-catégorie
                    </ion-text>
                  </div>

                  <!-- Produit de base -->
                  <div class="ion-margin-vertical">
                    <ion-label for="product-id" position="stacked" class="custom-label">Produit</ion-label>
                    <ion-item class="custom-item">
                      <ion-select
                        id="product-id"
                        name="product_id"
                        interface="popover"
                        :interface-options="{header: 'Veuillez sélectionner le produit'}"
                        v-model="product.product"
                        placeholder="Sélectionner le produit"
                      >
                        <ion-select-option 
                          v-for="item in basic_products"
                          :key="item.id"
                          :value="item.id">{{item.name}}</ion-select-option>
                      </ion-select>
                    </ion-item>
                    <ion-text v-if="errors.product.empty" class="error-text" color="danger">
                      * Veuillez choisir le produit
                    </ion-text>
                  </div>

                  <!-- Quantité -->
                  <div class="ion-margin-vertical">
                    <ion-label for="product-quantity" position="stacked" class="custom-label">Quantité en stock</ion-label>
                    <ion-item class="custom-item">
                      <ion-input 
                        id="product-quantity"
                        name="quantity"
                        v-model.number="product.quantity"
                        placeholder="0" 
                        @keydown="initErros"
                        type="number"
                        min="0">
                      </ion-input>
                    </ion-item>
                    <ion-text v-if="errors.quantity.empty" class="error-text" color="danger">
                      * La quantité doit être supérieure à 0
                    </ion-text>
                  </div>

                  <!-- Prix d'achat total -->
                  <div class="ion-margin-vertical">
                    <ion-label for="product-total-buy-price" position="stacked" class="custom-label">Prix d'achat total (BIF)</ion-label>
                    <ion-item class="custom-item">
                      <ion-input 
                        id="product-total-buy-price"
                        name="total_buy_price"
                        v-model.number="total_buy_price"
                        placeholder="Ex: 100000" 
                        @keydown="initErros"
                        type="number"
                        min="0">
                      </ion-input>
                    </ion-item>
                    <ion-text v-if="errors.total_buy_price.empty" class="error-text" color="danger">
                      * Prix d'achat invalide
                    </ion-text>
                  </div>

                  <!-- Prix de vente unitaire -->
                  <div class="ion-margin-vertical">
                    <ion-label for="product-sale-price" position="stacked" class="custom-label">Prix de vente unitaire (BIF)</ion-label>
                    <ion-item class="custom-item">
                      <ion-input 
                        id="product-sale-price"
                        name="sale_price"
                        v-model.number="product.sale_price"
                        placeholder="Ex: 1500" 
                        @keydown="initErros"
                        type="number"
                        min="0">
                      </ion-input>
                    </ion-item>
                    <ion-text v-if="errors.sale_price.empty" class="error-text" color="danger">
                      * Prix de vente invalide
                    </ion-text>
                  </div>

                  <!-- Bénéfice estimé -->
                  <div class="ion-margin-vertical">
                    <ion-label for="product-benefice" position="stacked" class="custom-label">Bénéfice estimé (Auto)</ion-label>
                    <ion-item class="disabled-item">
                      <ion-input 
                        id="product-benefice"
                        name="benefice"
                        v-model="benefice"
                        disabled
                        type="number">
                      </ion-input>
                    </ion-item>
                  </div>

                  <div class="ion-padding-top">
                    <ion-button
                      class="main-submit-btn"
                      color="secondary"
                      expand="block"
                      type="submit"
                      :disabled="loading"
                    >
                      <ion-spinner v-if="loading" slot="start"></ion-spinner>
                      <ion-text color="light">Ajouter au Stock</ion-text>
                    </ion-button>
                  </div>
                </form>
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
    IonSelectOption,
    IonFooter,
    IonRow
  } from '@ionic/vue';

  import {
    close,
    search,
    arrowBackOutline
  } from 'ionicons/icons'
  import { productsService, basicProductsService, categoriesService, subCategoriesService } from '../../services/api'
  
  /**
 * Composant CreateProduct
 * - Gère l'interface et la logique métier de Create Product.
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
        IonSelectOption,
        IonFooter,
        IonRow
    },
    data() {
      return {
        basic_products:[],
        search,
        imageUrl:null,
        total_buy_price:0,
        benefice:0,
        category:null,
        categories:[],
        sub_category:null,
        sub_categories:[],
        product:{
            shop:"",
            product:null,
            image:null,
            quantity:0,
            sale_price:0,
            buy_price:0
        },
        loading:false,
        errors:{
            product:{
                empty:false,
                custom:false
            },
            categories:{
                empty:false,
                custom:false
            },
            total_buy_price:{
                empty:false,
                custom:false
            },
            buy_price:{
                empty:false,
                custom:false
            },
            category:{
                empty:false,
                custom:false
            },
            sub_category:{
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
        this.fetchCategories()
        this.$store.state.shop = this.getShopFromLocalStorage()
    },
    watch:{
        "product.category":{
            deep:true,
            handler(new_val){
                
                if(new_val)
                this.getCategorySubCat(new_val)
            }
        },
        "total_buy_price":{
            deep:true,
            handler(new_val){
                if(new_val && this.product.quantity>0)
                    this.product.buy_price = (new_val/this.product.quantity).toFixed(1)
                
            }
        },
        "product.sale_price":{
            deep:true,
            handler(new_val){
                this.benefice = (this.product.sale_price*this.product.quantity)-this.total_buy_price
                
            }
        },
        "category":{
            deep:true,
            handler(new_val){
                if(new_val)
                    this.fetchSubCategories(new_val)
            }
        },
        "sub_category":{
            deep:true,
            handler(new_val){
                if(new_val)
                    this.fetchBasicProducts(new_val)
            }
        },
    },
    methods: {
        /**
         * Évite l'avertissement Chrome:
         * "Blocked aria-hidden on an element because its descendant retained focus"
         * en retirant le focus du bouton (ou autre) avant la fermeture du modal.
         */
        blurActiveElement() {
            try {
                const el = typeof document !== 'undefined' ? document.activeElement : null;
                if (el && typeof el.blur === 'function') el.blur();
            } catch {
                // no-op
            }
        },
        getCategorySubCat(category){
            this.sub_categories = category.subCategories
        },
        initErros(){
            this.errors.product.empty=false
            this.errors.quantity.empty=false
            this.errors.sale_price.empty=false
            this.errors.category.empty=false
            this.errors.sub_category.empty=false
            this.errors.total_buy_price.empty=false
        },
        performClose() {
          this.blurActiveElement()
          return modalController.dismiss(null, 'cancel');
        },
        validateInputs(){
            this.initErros()
            this.$store.state.shop = this.getShopFromLocalStorage()
            if(this.category==null){
                this.errors.category.empty=true
                return false
            }
            if(this.sub_category==null){
                this.errors.sub_category.empty=true
                return false
            }
            if(this.product.product==null){
                this.errors.product.empty=true
                return false
            }
            if(this.product.quantity <= 0){
                this.errors.quantity.empty=true
                return false
            }
            if(this.product.sale_price<=0){
                this.errors.sale_price.empty=true
                return false
            }
            if(this.total_buy_price < 0){
                this.errors.total_buy_price.empty=true
                return false
            }
            if(!this.$store.state.shop){
                this.showTostMsg("Boutique introuvable.", "danger",5000)
                return false
            }
            return true
        },
        perfromCreateProduct(){
            if(this.validateInputs()){
                this.loading=true
                this.product.shop=this.$store.state.shop.id
                // sécuriser le buy_price si total_buy_price est fourni
                if (this.total_buy_price && this.product.quantity > 0) {
                    this.product.buy_price = (this.total_buy_price / this.product.quantity).toFixed(1)
                }
                console.log(this.product)
                productsService.createProduct(this.product)
                .then((res)=>{
                    this.loading=false
                    this.$store.state.products.push(res.data)
                    this.showTostMsg("Produit ajouté avec succès !", "success",5000)
                    this.blurActiveElement()
                    modalController.dismiss(null, "cancel")
                }).catch((err)=>{
                    this.loading=false
                    this.errorOrRefresh(err, () => this.perfromCreateProduct())
                })      
            }
        },
        async fetchBasicProducts(id){
            // Charger tous les produits de base pour cette sous-catégorie (plusieurs pages DRF si besoin)
            const all = []
            let page = 1
            const pageSize = 200
            this.loading = true
            try{
                while (true) {
                    const res = await basicProductsService.getBasicProducts({ sub_category: id, page, page_size: pageSize })
                    const results = res.data.results || res.data || []
                    if (!Array.isArray(results) || !results.length) break
                    all.push(...results)
                    if (results.length < pageSize) break
                    page += 1
                }
                // tri alphabétique comme dans le catalogue
                this.basic_products = [...all].sort((a, b) => {
                    const na = (a.name || '').toString().toLowerCase()
                    const nb = (b.name || '').toString().toLowerCase()
                    return na.localeCompare(nb)
                })
            }catch(err){
                this.errorOrRefresh(err, () => this.fetchBasicProducts(id))
            }finally{
                this.loading = false
            }
        },
        fetchCategories(){
            categoriesService.getCategories()
            .then((res)=>{
                this.categories = res.data.results
            }).catch((err)=>{
                this.loading=false
                this.errorOrRefresh(err, () => this.fetchCategories())
            })      
        },
        fetchSubCategories(id){
            subCategoriesService.getSubCategories({ category: id })
            .then((res)=>{
                this.sub_categories = res.data.results
            }).catch((err)=>{
                this.loading=false
                this.errorOrRefresh(err, () => this.fetchCategories())
            })      
            
        },
        
    },
  
  };
  </script>
  
  <style lang="scss" scoped>
  
  ion-content {
      --background: #f8fafc;
      font-family: 'Inter', sans-serif;
  }

  .form-container {
    background: white;
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    margin-top: 10px;
  }

  .custom-label {
    font-weight: 700;
    color: #475569;
    margin-bottom: 8px;
    font-size: 0.9rem;
  }

  .custom-item {
    --padding-start: 12px;
    --border-radius: 12px;
    --border-color: #e2e8f0;
    --background: #f8fafc;
    margin-bottom: 4px;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
  }
  
  .disabled-item {
    --padding-start: 12px;
    --border-radius: 12px;
    --background: #f1f5f9;
    border-radius: 12px;
    opacity: 0.8;
  }

  .error-text {
    font-size: 0.75rem;
    margin-top: 4px;
    margin-left: 4px;
    font-weight: 600;
  }

  .main-submit-btn {
    --border-radius: 12px;
    height: 56px;
    margin-top: 10px;
    font-size: 1.1rem;
    font-weight: 700;
  }

  @media (min-width: 768px) {
    .form-container {
      margin-top: 40px;
      padding: 40px;
    }
  }
  </style>
  