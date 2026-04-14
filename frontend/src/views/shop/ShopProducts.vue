<!--
  * @file ShopProducts.vue
  * @description Page pour la gestion de Shop Products.
  * @author Kora Agency
-->
<template>
     <ion-page>
   <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-shop" name="back-to-shop" @click="$router.push({ name: 'shop' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span class="main-title">Catalogue Produits</span>
            <div class="header-badges">
              <ion-badge color="light" class="shop-count-badge">
                {{ shopProductsCount }} en boutique
              </ion-badge>
              <ion-badge v-if="basicProductsCount" color="secondary" class="catalog-count-badge">
                {{ basicProductsCount }} catalogue
              </ion-badge>
            </div>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="analyzeDuplicates" color="warning">
            <ion-icon color="light" size="large" :icon="copyOutline"></ion-icon>
          </ion-button>
          <ion-button @click="exportToExcel" color="light">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchCurrentShop">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>

      <ion-toolbar color="secondary">
        <ion-searchbar 
          id="shop-catalog-search"
          v-model="searchKeyword" 
          placeholder="Rechercher un produit..." 
          show-clear-button="always"
          color="light"
          class="custom-searchbar"
        ></ion-searchbar>
      </ion-toolbar>
    </ion-header>
  
  <ion-content>
    <!-- Filtres par catégorie et sous-catégorie -->
    <div class="filter-row ion-margin-horizontal">
      <ion-item lines="none" class="filter-item">
        <ion-select
          id="shop-filter-category"
          name="filter_category"
          :interface-options="{ header: 'Catégorie' }"
          v-model="filterCategoryId"
          placeholder="Catégorie"
          interface="alert"
          @ionChange="onFilterCategoryChange"
        >
          <ion-select-option :value="null">Toutes les catégories</ion-select-option>
          <ion-select-option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </ion-select-option>
        </ion-select>
      </ion-item>
      <ion-item lines="none" class="filter-item">
        <ion-select
          id="shop-filter-sub-category"
          name="filter_sub_category"
          :interface-options="{ header: 'Sous-catégorie' }"
          v-model="filterSubCategoryId"
          placeholder="Sous-catégorie"
          interface="alert"
          :disabled="!filterCategoryId"
        >
          <ion-select-option :value="null">Toutes les sous-catégories</ion-select-option>
          <ion-select-option v-for="sub in filterSubCategories" :key="sub.id" :value="sub.id">
            {{ sub.name }}
          </ion-select-option>
        </ion-select>
      </ion-item>
    </div>

    <!-- Liste des articles du catalogue central -->
    <ion-list class="products-list-compact">
      <ion-item-sliding v-for="basic in filteredProducts" :key="basic.id">
        <ion-item>
          <ion-thumbnail slot="start" class="picker-thumb">
            <ion-img :src="productImage(basic)" @ionError="(e) => e.target.src = '/placeholder.png'"></ion-img>
          </ion-thumbnail>

          <ion-label>
            <h2 class="product-name-label">{{ basic.name }}</h2>
            <p class="art-cat">{{ getCategoryLabel(basic) }}</p>
            <div v-if="isInShop(basic.id)" class="product-shop-info">
               <p class="qty-label">Stock: <ion-text color="primary">{{ getShopProduct(basic.id)?.quantity || 0 }}</ion-text></p>
               <p class="price-label">Prix: <ion-text color="success">{{ money(getShopProduct(basic.id)?.sale_price) }} BIF</ion-text></p>
            </div>
            <p v-else class="not-in-shop">Non présent dans votre boutique</p>
          </ion-label>

          <ion-button
            fill="clear"
            slot="end"
            @click="toggleInShop(basic)"
            :id="'toggle-shop-product-' + basic.id"
            :name="'toggle_shop_product_' + basic.id"
          >
            <ion-icon
              :icon="isInShop(basic.id) ? star : starOutline"
              color="primary"
              size="large"
            />
          </ion-button>
        </ion-item>

        <ion-item-options side="end">
          <ion-item-option v-if="isInShop(basic.id)" color="secondary" @click.stop="manageShopProduct(basic)">
            <div class="option-content">
              <ion-icon :icon="createOutline"></ion-icon>
              <span>Prix/Stock</span>
            </div>
          </ion-item-option>
          <ion-item-option v-if="isInShop(basic.id)" color="danger" @click.stop="confirmRemoveFromShop(basic)">
            <div class="option-content">
              <ion-icon :icon="trashOutline"></ion-icon>
              <span>Retirer</span>
            </div>
          </ion-item-option>
          <ion-item-option v-if="!isInShop(basic.id) && canManageCatalog" color="medium" @click.stop="editProduct(basic)">
            <div class="option-content">
              <ion-icon :icon="createOutline"></ion-icon>
              <span>Catalog Info</span>
            </div>
          </ion-item-option>
        </ion-item-options>
      </ion-item-sliding>

      <!-- Même si la liste est vide, on garde la structure de la page -->
      <ion-item v-if="filteredProducts.length === 0">
        <ion-label>
          <p v-if="basicProducts.length === 0">Aucun article pour le moment.</p>
          <p v-else>Aucun article ne correspond aux filtres sélectionnés.</p>
          <p v-if="basicProducts.length === 0">Ajoutez des produits au catalogue pour les voir ici.</p>
        </ion-label>
      </ion-item>
      <ion-infinite-scroll @ionInfinite="loadMore" :disabled="!hasNextPage && !hasMoreBasic" id="shop-infinite-scroll">
        <ion-infinite-scroll-content loading-spinner="bubbles" loading-text="Chargement des produits..."></ion-infinite-scroll-content>
      </ion-infinite-scroll>
    </ion-list>
  </ion-content>

  <!-- Barre de navigation en bas (Accueil / Listes / Ajouter) -->
  <ion-footer v-if="canManageCatalog" class="bottom-bar ion-no-border">
    <ion-toolbar>
      <div class="bottom-actions">
        <ion-button fill="clear" class="primary-btn" @click="createProduct">
          <ion-icon slot="start" :icon="addOutline"></ion-icon>
          <ion-label>Ajouter</ion-label>
        </ion-button>
        <ion-button fill="clear" @click="openDeleteMode">
          <ion-icon slot="start" :icon="removeOutline"></ion-icon>
          <ion-label>Supprimer</ion-label>
        </ion-button>
      </div>
    </ion-toolbar>
  </ion-footer>
</ion-page>
  </template>
  
  <script>
  import {
    IonHeader,
    IonPage,
    modalController,
    IonToolbar,
    IonButtons,
    IonButton,
    IonIcon,
    IonBadge,
    IonText,
    IonContent,
    IonItem,
    IonItemSliding,
    IonItemOptions,
    IonItemOption,
    IonLabel,
    IonThumbnail,
    IonListHeader,
    IonSelect,
    IonSelectOption,
    IonRow,
    IonCol,
    IonCard,
    IonTitle,
    IonFab,
    IonFabButton,
    IonList,
    IonPopover,
    IonFooter,
    IonSearchbar,
    IonInfiniteScroll,
    IonInfiniteScrollContent,
    IonImg,
    alertController,
    actionSheetController
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
    chevronForward,
    eye,
    createOutline,
    addCircle,
    star,
    starOutline,
    listOutline,
    removeOutline,
    copyOutline,
    downloadOutline,
    trashOutline
  } from 'ionicons/icons'
import * as XLSX from 'xlsx';
import { saveWorkbook } from '../../utils/exportExcel';
import { defineAsyncComponent } from 'vue';

const BasicProductForm = defineAsyncComponent(() => import('../../components/admin/BasicProductForm.vue'));
import CreateProduct from '../../components/shop/CreateProduct.vue';
import SupplyProduct from '../../components/shop/SupplyProduct.vue';
import ChangeProductPrice from '../../components/shop/ChangeProductPrice.vue';
import StockProduct from '../../components/shop/StockProduct.vue';
import { shopsService, productsService, basicProductsService, categoriesService, subCategoriesService } from '../../services/api';
import globalMixins from '../../composables/mixins';
import { axiosService } from '../../plugins/axios';
  
  /**
 * Composant ShopProducts
 * - Gère l'interface et la logique métier de Shop Products.
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
      IonItemSliding,
      IonItemOptions,
      IonItemOption,
      IonList,
      IonSelect,
      IonSelectOption,
      IonPopover,
      IonLabel,
      IonThumbnail,
      IonListHeader,
      IonRow,
      IonCol,
      IonCard,
      IonTitle,
      IonFab,
      IonFabButton,
      IonSearchbar,
      IonFooter,
      IonInfiniteScroll,
      IonInfiniteScrollContent,
      IonImg
    },
    setup() {
      return {
        cartOutline,
        home,
        exitOutline,
        addOutline,
        ellipsisVertical,
        personOutline,
        fastFoodOutline,
        arrowBackOutline,
        refreshCircleOutline,
        chevronForward,
        eye,
        createOutline,
        addCircle,
        star,
        starOutline,
        copyOutline,
        downloadOutline,
        trashOutline
      };
    },
    watch: {
      filterCategoryId() {
        this.onFilterCategoryChange();
      }
    },
    data(){
      return{
        shop:this.$store.state.shop,
        basicProducts: [],
        basicProductsCount: null,
        inShopIds: [],
        deleteMode: false,
        categories: [],
        filterSubCategories: [],
        filterCategoryId: null,
        filterSubCategoryId: null,
        searchKeyword: '',
        isExporting: false,
        hasNextPage: true,
        currentPage: 1,
        isBasicLoading: false,
        hasMoreBasic: true,
        currentBasicPage: 1,
        searchTimeout: null
      }
    },
    computed:{
        filteredProducts() {
          let list = this.basicProducts || [];
          const catId = this.filterCategoryId;
          const subId = this.filterSubCategoryId;

          if (subId != null && subId !== '') {
            list = list.filter((p) => {
              const sub = p.sub_category;
              const pSubId = p.sub_category_id ?? sub?.id ?? sub;
              return Number(pSubId) === Number(subId);
            });
          }
          
          if (this.searchKeyword && this.searchKeyword.trim() !== '') {
            const kw = this.searchKeyword.trim().toLowerCase();
            list = list.filter(p => {
              const name = (p.name || '').toLowerCase();
              const cat = (this.getCategoryLabel(p) || '').toLowerCase();
              return name.includes(kw) || cat.includes(kw);
            });
          }

          return [...list].sort((a, b) => {
            const na = (a.name || '').toLowerCase();
            const nb = (b.name || '').toLowerCase();
            return na.localeCompare(nb);
          });
        },
        shopId(){
            return this.shop?.id
        },
        /** Nombre de produits dans la boutique (pour affichage X/Y dans la toolbar) */
        shopProductsCount(){
            return (this.$store.state.products || []).length
        },
        // Seuls les utilisateurs "privilégiés" (admin / agent) voient Ajouter / Supprimer
        canManageCatalog(){
            return this.active_user_is('admin','agent','superuser');
        }
    },
    beforeMount(){
        this.$store.state.shop = this.getShopFromLocalStorage()
        this.shop = this.$store.state.shop
        
        // On charge toujours les catégories et le catalogue de base, même sans boutique
        this.fetchCategories()
        this.fetchBasicProducts()
        
        const storedShop = this.getShopFromLocalStorage()
        if (storedShop) {
          this.$store.state.shop = storedShop
          this.shop = storedShop
          this.fetchProducts()
        } else {
          console.log("[ShopProducts] Mode catalogue : aucune boutique active.")
        }
    },
    methods:{
        fetchCurrentShop(){
          this.$store.state.shop = this.getShopFromLocalStorage()
          this.shop = this.$store.state.shop
          const id = this.shop?.id
          if (id == null || id === '' || String(id) === 'undefined') {
            this.$router.replace({ name: 'home' })
            return
          }
          shopsService.getShop(id)
            .then((res)=>{
                this.$store.state.shop=res.data
                this.shop=res.data
            }).catch((err)=>{
                if (err.response?.status === 404) {
                  localStorage.removeItem('current_shop')
                  this.$store.state.shop = null
                  this.shop = null
                  this.showTostMsg('Boutique introuvable. Veuillez choisir une boutique.', 'warning', 4000)
                  return
                }
                this.errorOrRefresh(err, () => this.fetchCurrentShop())
            }).finally(()=>{
                if (this.shop?.id) {
                    this.fetchProducts()
                }
            })
        },
        async fetchProducts(page = 1) {
            if (!this.shopId) return;
            this.loading = true;
            try {
                const res = await productsService.getProducts(this.shopId, { page, page_size: 20 });
                const data = res.data;
                const results = data.results || data || [];
                
                if (page === 1) {
                  this.$store.state.products = results;
                } else {
                  this.$store.state.products = [...(this.$store.state.products || []), ...results];
                }

                this.hasNextPage = !!data.next;
                this.currentPage = page;
                this.refreshInShopIds();
            } catch (err) {
                console.error("[ShopProducts] Error fetching products:", err);
                this.hasNextPage = false;
            } finally {
                this.loading = false;
            }
        },
        fetchCategories() {
          return categoriesService.getCategories()
            .then((res) => {
              const raw = res.data.results || res.data || [];
              this.categories = Array.isArray(raw) ? raw : [];
            })
            .catch(() => {
              this.categories = [];
            });
        },
        onFilterCategoryChange() {
          this.filterSubCategoryId = null;
          const catId = this.filterCategoryId;
          if (!catId) {
            this.filterSubCategories = [];
            return;
          }
          subCategoriesService.getSubCategories({ category: catId })
            .then((res) => {
              const raw = res.data.results || res.data || [];
              this.filterSubCategories = Array.isArray(raw) ? raw : [];
            })
            .catch(() => {
              this.filterSubCategories = [];
            });
        },
        fetchBasicProducts() {
            this.isBasicLoading = true;
            const all = [];

            const fetchPage = async (url) => {
              try {
                const res = url 
                  ? await axiosService.get(url) 
                  : await basicProductsService.getBasicProducts({ page_size: 500 });
                  
                const data = res.data;
                const raw = data.results || data || [];
                const results = Array.isArray(raw) ? raw : [];
                all.push(...results);

                if (data.next) {
                  return fetchPage(data.next);
                } else {
                  this.basicProducts = [...all].sort((a, b) => {
                    const na = (a.name || '').toString().toLowerCase();
                    const nb = (b.name || '').toString().toLowerCase();
                    return na.localeCompare(nb);
                  });
                  this.basicProductsCount = all.length;
                  this.hasMoreBasic = false;
                  this.isBasicLoading = false;
                }
              } catch (err) {
                console.error("[ShopProducts] Error fetching basic products:", err);
                this.isBasicLoading = false;
                this.hasMoreBasic = false;
              }
            };

            fetchPage();
        },
        async loadMore(ev) {
            if (this.hasNextPage && this.shopId) {
              await this.fetchProducts(this.currentPage + 1);
            }
            ev.target.complete();
        },
        refreshInShopIds(){
            const products = this.$store.state.products || []
            this.inShopIds = products
              .filter(p => p.product && p.product.id)
              .map(p => p.product.id)
        },
        isInShop(basicId){
            return this.inShopIds.includes(basicId)
        },
        getShopProduct(basicId) {
            return (this.$store.state.products || []).find(p => p.product && p.product.id === basicId);
        },
        async exportToExcel() {
            if (this.basicProducts.length === 0) {
                this.showTostMsg('Aucun produit à exporter', 'warning');
                return;
            }

            const data = this.basicProducts.map(p => {
                const shopProd = this.getShopProduct(p.id);
                return {
                    'ID': p.id,
                    'Nom': p.name,
                    'Catégorie': this.getCategoryLabel(p),
                    'Dans Boutique': this.isInShop(p.id) ? 'OUI' : 'NON',
                    'Stock': shopProd ? shopProd.quantity : 0,
                    'Prix de vente': shopProd ? shopProd.sale_price : 0,
                    'Unité': p.unit || 'Pièce'
                };
            });

            const ws = XLSX.utils.json_to_sheet(data);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Catalogue");
            
            const fileName = `Catalogue_AgaShop_${new Date().toISOString().split('T')[0]}.xlsx`;
            await saveWorkbook(wb, fileName);
            this.showTostMsg('Export Excel réussi !', 'success');
        },
        async toggleInShop(basic){
            if (!this.shopId) {
              this.showTostMsg("Veuillez d'abord sélectionner ou créer une boutique active.", "warning", 4000);
              return;
            }
            if (this.isInShop(basic.id)) {
              const product = (this.$store.state.products || []).find(p => p.product && p.product.id === basic.id)
              if (!product) return
              try{
                await productsService.deleteProduct(product.id)
                this.$store.state.products = this.$store.state.products.filter(p => p.id !== product.id)
                this.refreshInShopIds()
                this.showTostMsg("Produit retiré de votre boutique.", "success", 3000)
              }catch(err){
                this.errorOrRefresh(err, () => this.toggleInShop(basic))
              }
              return
            }

            const payload = {
              shop: Number(this.shopId),
              product: Number(basic.id),
              quantity: 0,
              sale_price: 0,
              buy_price: 0
            }
            try {
              const res = await productsService.createProduct(payload)
              this.$store.state.products.push(res.data)
              this.refreshInShopIds()
              this.showTostMsg("Produit ajouté à votre boutique.", "success", 3000)
            } catch (err) {
              if (err.response?.status === 400) {
                const data = err.response?.data || {}
                const msg = data.details || data.message
                const nonField = Array.isArray(data.non_field_errors) ? data.non_field_errors.join(' ') : ''
                const fullText = [msg, nonField, JSON.stringify(data)].filter(Boolean).join(' ')
                const isAlready = data.code === 'already_in_shop' ||
                  (msg && (String(msg).includes('déjà') || String(msg).includes('already'))) ||
                  /unique|already exists|déjà|must make a unique set/i.test(fullText)
                this.showTostMsg(isAlready ? 'Ce produit est déjà dans votre boutique.' : (msg || nonField || 'Impossible d\'ajouter ce produit.'), 'warning', 4000)
                this.fetchProducts()
                return
              }
              this.errorOrRefresh(err, () => this.toggleInShop(basic))
            }
        },
        openDeleteMode(){
          this.showTostMsg("Glissez un produit vers la gauche pour le gérer ou le retirer de votre boutique.", "primary", 5000)
        },
        async manageShopProduct(basic) {
          const shopProduct = this.getShopProduct(basic.id);
          if (!shopProduct) return;
          
          const actionSheet = await actionSheetController.create({
            header: `Gérer ${basic.name}`,
            buttons: [
              {
                text: 'Changer le Prix de Vente',
                icon: createOutline,
                handler: () => this.openPriceModal(shopProduct)
              },
              {
                text: 'Contrôler le Stock',
                icon: listOutline,
                handler: () => this.openStockControlModal(shopProduct)
              },
              {
                text: 'Annuler',
                role: 'cancel'
              }
            ]
          });
          await actionSheet.present();
        },
        async openPriceModal(shopProduct) {
          const modal = await modalController.create({
            component: ChangeProductPrice,
            componentProps: { productProp: shopProduct }
          });
          await modal.present();
          const { role } = await modal.onDidDismiss();
          if (role === 'confirm') this.fetchProducts();
        },
        async openStockControlModal(shopProduct) {
          const { default: ControlProduct } = await import('../../components/shop/ControlProduct.vue');
          const modal = await modalController.create({
            component: ControlProduct,
            componentProps: { productProp: shopProduct }
          });
          await modal.present();
          const { role } = await modal.onDidDismiss();
          if (role === 'confirm') this.fetchProducts();
        },
        async editProduct(product) {
          if (!this.canManageCatalog) {
            this.showTostMsg("Vous n'avez pas les droits d'édition du catalogue global.", "warning", 3000);
            return;
          }
          const modal = await modalController.create({
            component: BasicProductForm,
            componentProps: { mode: 'edit', product: product }
          });
          await modal.present();
          const { role } = await modal.onDidDismiss();
          if (role === 'confirm') {
            this.fetchBasicProducts();
          }
        },
        async confirmRemoveFromShop(basic) {
          const alert = await alertController.create({
            header: 'Retirer de la boutique ?',
            message: `Voulez-vous retirer "${basic.name}" de votre inventaire local ?`,
            buttons: [
              { text: 'Annuler', role: 'cancel' },
              { 
                text: 'Oui, retirer', 
                role: 'destructive',
                handler: () => this.toggleInShop(basic) // toggleInShop handles the delete logic if already in shop
              }
            ]
          });
          await alert.present();
        },
        async confirmDelete(product) {
           // On garde cette fonction pour le cas où l'utilisateur veut vraiment tout supprimer (Admin)
           // Mais on l'utilise moins en favorisant le retrait.
          const alert = await alertController.create({
            header: 'Suppression DÉFINITIVE ?',
            message: `Voulez-vous vraiment supprimer "${product.name}" du catalogue global ? Cette action est irréversible.`,
            buttons: [
              { text: 'Annuler', role: 'cancel' },
              { 
                text: 'Supprimer Tout', 
                role: 'destructive',
                handler: () => this.deleteBasicProduct(product.id)
              }
            ]
          });
          await alert.present();
        },
        async deleteBasicProduct(productId) {
          try {
            await basicProductsService.deleteBasicProduct(productId);
            this.showTostMsg("Produit supprimé du catalogue global.", "success", 3000);
            this.fetchBasicProducts();
          } catch (err) {
            this.errorOrRefresh(err, () => this.deleteBasicProduct(productId));
          }
        },
        async analyzeDuplicates() {
          this.blurActiveElement();
          const list = this.basicProducts || [];
          if (list.length === 0) return;

          const nameMap = {};
          list.forEach(p => {
            const name = (p.name || '').trim().toLowerCase();
            if (!nameMap[name]) nameMap[name] = [];
            nameMap[name].push(p);
          });

          const duplicates = Object.values(nameMap).filter(group => group.length > 1);

          if (duplicates.length === 0) {
            const alert = await alertController.create({
              header: 'Analyse terminée',
              message: 'Aucun doublon trouvé dans le catalogue.',
              buttons: ['OK']
            });
            await alert.present();
            return;
          }

          const totalDups = duplicates.reduce((acc, curr) => acc + (curr.length - 1), 0);
          
          const alert = await alertController.create({
            header: 'Doublons détectés',
            message: `Il y a ${duplicates.length} noms de produits en double (total de ${totalDups} exemplaires en trop).\n\nSouhaitez-vous les supprimer pour n'en garder qu'un seul par nom ?`,
            buttons: [
              { text: 'Annuler', role: 'cancel' },
              {
                text: 'Nettoyer',
                handler: () => this.performCleanup(duplicates)
              }
            ]
          });
          await alert.present();
        },
        async performCleanup(duplicateGroups) {
          this.blurActiveElement();
          const toDelete = [];
          duplicateGroups.forEach(group => {
            const sorted = [...group].sort((a, b) => a.id - b.id);
            const extras = sorted.slice(1);
            toDelete.push(...extras.map(p => p.id));
          });

          let successCount = 0;
          let errorCount = 0;

          for (const id of toDelete) {
            try {
              await basicProductsService.deleteBasicProduct(id);
              successCount++;
            } catch (err) {
              console.error(`Failed to delete duplicate ${id}:`, err);
              errorCount++;
            }
          }

          this.showTostMsg(`${successCount} doublons supprimés avec succès.${errorCount > 0 ? ` (${errorCount} erreurs)` : ''}`, 'success', 5000);
          this.fetchBasicProducts();
        },
        async createProduct() {
            const modal = await modalController.create({
                initialBreakpoint:1,
                component: CreateProduct,
            });
            modal.present();

            const { data, role } = await modal.onWillDismiss();

            if (role === 'confirm') {
                this.fetchCurrentShop();
                await this.fetchCategories();
                if (this.filterCategoryId) this.onFilterCategoryChange();
            }        
        },
        async supplyProduct(product) {
            const modal = await modalController.create({
                initialBreakpoint:1,
                component: SupplyProduct,
                componentProps:{productProp:product}
            });
            modal.present();

            const { data, role } = await modal.onWillDismiss();

            if (role === 'confirm') {
                this.fetchCurrentShop();
                await this.fetchCategories();
                if (this.filterCategoryId) this.onFilterCategoryChange();
            }        
        },
        async changeProductPrice(product) {
            const modal = await modalController.create({
                initialBreakpoint:1,
                component: ChangeProductPrice,
                componentProps:{productProp:product}
            });
            modal.present();

            const { data, role } = await modal.onWillDismiss();

            if (role === 'confirm') {
                this.fetchCurrentShop();
                await this.fetchCategories();
                if (this.filterCategoryId) this.onFilterCategoryChange();
            }        
        },
        async stockProduct(product) {
            const modal = await modalController.create({
                initialBreakpoint:1,
                component: StockProduct,
                componentProps:{productProp:product}
            });
            modal.present();

            const { data, role } = await modal.onWillDismiss();

            if (role === 'confirm') {
                this.fetchCurrentShop();
                await this.fetchCategories();
                if (this.filterCategoryId) this.onFilterCategoryChange();
            }        
        },
    }
}
</script>
  
  <style lang="scss" scoped>
ion-content {
  --background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
  background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
  font-family: 'Outfit', sans-serif;
}

.header-title-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;

  .main-title {
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
  }

  .header-badges {
    display: flex;
    gap: 8px;
    
    .shop-count-badge {
      font-size: 0.7rem;
      --padding-start: 6px;
      --padding-end: 6px;
      border-radius: 8px;
      color: var(--ion-color-secondary);
      background: white;
      font-weight: 800;
    }
    
    .catalog-count-badge {
      font-size: 0.7rem;
      --padding-start: 6px;
      --padding-end: 6px;
      border-radius: 8px;
      opacity: 0.9;
      font-weight: 800;
    }
  }
}

.filter-row {
  display: flex;
  gap: 12px;
  padding: 16px;
  margin-top: 4px;
  animation: fadeInUp 0.5s ease-out;
}

.filter-item {
  flex: 1;
  --background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  --padding-start: 12px;
  --padding-end: 12px;

  ion-select {
    width: 100%;
    font-weight: 800;
    color: #1e293b;
    font-size: 0.95rem;
  }
}

.products-list-compact {
  background: transparent;
  padding: 0 12px 100px 12px;
  margin: 0;
}

ion-item {
  --background: white;
  --padding-start: 16px;
  --padding-end: 12px;
  --inner-padding-end: 0;
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  margin-bottom: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  --border-style: none;
  animation: fadeInUp 0.4s ease-out both;

  ion-thumbnail {
    width: 64px;
    height: 74px;
    margin-right: 18px;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #f1f5f9;
  }

  ion-label {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    p {
      margin-top: 4px;
      font-size: 0.85rem;
      font-weight: 600;
      color: #64748b;
    }
    .art-cat {
      font-size: 0.8rem;
      color: #64748b;
      font-weight: 700;
      margin-top: 2px;
      display: block;
    }
  }

  ion-button {
    --color: var(--ion-color-secondary);
    --padding-start: 8px;
    --padding-end: 8px;
    margin: 0;
    font-weight: 800;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.custom-searchbar {
  --background: rgba(255, 255, 255, 0.9);
  --border-radius: 12px;
  --placeholder-color: #666;
  --icon-color: #334155;
  padding: 8px 16px;
}

.header-title-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.custom-searchbar {
  --background: rgba(255, 255, 255, 0.9);
  --border-radius: 12px;
  --placeholder-color: #666;
  --icon-color: #334155;
  padding: 8px 16px;
}

.header-title-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.2;
}

.main-title {
  font-weight: 800;
  font-size: 1.1rem;
}

.toolbar-shop-count {
  font-size: 0.7rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.85);
  background: rgba(0, 0, 0, 0.15);
  padding: 1px 10px;
  border-radius: 20px;
  margin-top: 2px;
  letter-spacing: 0.02em;
}

.bottom-bar {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 -10px 25px rgba(0, 0, 0, 0.05);
  
  ion-toolbar {
    --background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    --padding-top: 12px;
    --padding-bottom: 12px;
  }

  .bottom-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
    padding: 0 16px;
  }

  ion-button {
    --color: white;
    --background: #0f172a;
    --border-radius: 14px;
    height: 52px;
    font-weight: 800;
    text-transform: none;
    flex: 1;
    margin: 0;
    --box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2);
    
    ion-label {
      color: white;
      font-weight: 800;
      font-size: 0.95rem;
    }
    
    ion-icon {
      color: white;
      margin-right: 8px;
    }

    &.primary-btn {
      --background: var(--ion-color-secondary);
      --box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    &:active {
      transform: scale(0.98);
    }
  }
}
</style>