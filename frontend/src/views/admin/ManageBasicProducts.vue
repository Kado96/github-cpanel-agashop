<!--
  * @file ManageBasicProducts.vue
  * @description Page/Composant pour Manage Basic Products.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button @click="goHome">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>

        <ion-title color="light">
          <div class="header-title-container">
            <span>Catalogue</span>
            <span v-if="totalCatalogueCount != null" class="toolbar-shop-count">
              {{ totalCatalogueCount }} produit{{ totalCatalogueCount !== 1 ? 's' : '' }}
            </span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchBasicProducts">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>

      <!-- Barre de recherche globale -->
      <ion-toolbar color="primary" class="search-toolbar">
        <ion-searchbar
          v-model="searchKeyword"
          placeholder="Rechercher un produit..."
          class="custom-searchbar"
          animated
          @ionClear="searchKeyword = ''"
        ></ion-searchbar>
      </ion-toolbar>
    </ion-header>

    <ion-content class="catalog-content">
      <!-- Filtres par catégorie et sous-catégorie -->
      <div class="filter-row ion-margin-horizontal">
        <ion-item lines="none" class="filter-item">
          <ion-select
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

      <!-- Liste des produits : glisser à gauche/droite pour Ajouter ou Supprimer -->
      <ion-list class="catalog-list catalog-list-compact">
        <ion-item-sliding v-for="product in filteredProducts" :key="product.id">
          <ion-item-options side="start">
            <ion-item-option @click="editProduct(product)" color="primary">
              <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
              Modifier
            </ion-item-option>
            <ion-item-option @click="confirmDelete(product)" color="danger">
              <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
              Supprimer
            </ion-item-option>
          </ion-item-options>

          <ion-item button detail="false" class="bp-item" @click="editProduct(product)">
            <ion-thumbnail slot="start">
              <img :src="product.image || '/placeholder.png'" />
            </ion-thumbnail>
            <ion-label>
              <h2 class="bp-title">{{ product.name }}</h2>
              <p class="bp-cat">{{ getCategoryLabel(product) }}</p>
              <p class="bp-subtitle">Glissez pour Modifier / Supprimer</p>
            </ion-label>
          </ion-item>

          <ion-item-options side="end">
            <ion-item-option @click="editProduct(product)" color="primary">
              <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
              Modifier
            </ion-item-option>
            <ion-item-option @click="confirmDelete(product)" color="danger">
              <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
              Supprimer
            </ion-item-option>
          </ion-item-options>
        </ion-item-sliding>

        <ion-item v-if="filteredProducts.length === 0">
          <ion-label>
            <p v-if="basicProducts.length === 0">Aucun produit dans le catalogue.</p>
            <p v-else>Aucun produit ne correspond aux filtres sélectionnés.</p>
            <p v-if="basicProducts.length === 0">Utilisez le bouton + en bas à droite pour ajouter.</p>
          </ion-label>
        </ion-item>
      </ion-list>

      <!-- Bouton flottant Ajouter (visible même liste vide) -->
      <ion-fab v-if="canManageCatalog" slot="fixed" vertical="bottom" horizontal="end" style="bottom: 72px !important; transform: none !important; z-index: 10001 !important;">
        <ion-fab-button color="primary" @click="openCreateModal">
          <ion-icon :icon="addOutline"></ion-icon>
        </ion-fab-button>
      </ion-fab>
    </ion-content>
  </ion-page>
</template>

<script>
import {
  IonHeader,
  IonPage,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonIcon,
  IonContent,
  IonItem,
  IonItemSliding,
  IonItemOptions,
  IonItemOption,
  IonLabel,
  IonThumbnail,
  IonList,
  IonListHeader,
  IonSelect,
  IonSelectOption,
  IonFab,
  IonFabButton,
  IonSearchbar,
  modalController,
  alertController,
  actionSheetController
} from '@ionic/vue';

import {
  arrowBackOutline,
  refreshCircleOutline,
  addOutline,
  removeOutline,
  createOutline,
  trashOutline,
  copyOutline,
  downloadOutline
} from 'ionicons/icons';

import { basicProductsService, productsService, categoriesService, subCategoriesService } from '../../services/api';
import { axiosService } from '../../plugins/axios';
import { defineAsyncComponent } from 'vue';
import * as XLSX from 'xlsx';

const BasicProductForm = defineAsyncComponent(() => import('../../components/admin/BasicProductForm.vue'));

/**
 * Composant ManageBasicProducts
 * - Gère l'interface et la logique métier.
 */
export default {
  components: {
    IonHeader,
    IonPage,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonIcon,
    IonContent,
    IonItem,
    IonItemSliding,
    IonItemOptions,
    IonItemOption,
    IonLabel,
    IonThumbnail,
    IonList,
    IonListHeader,
    IonSelect,
    IonSelectOption,
    IonFab,
    IonFabButton,
    IonSearchbar
  },
  data() {
    return {
      arrowBackOutline,
      refreshCircleOutline,
      addOutline,
      removeOutline,
      createOutline,
      trashOutline,
      copyOutline,
      downloadOutline,
      basicProducts: [],
      totalCatalogueCount: null,
      shopProductsCount: null,
      categories: [],
      filterSubCategories: [],
      filterCategoryId: null,
      filterSubCategoryId: null,
      searchKeyword: ''
    }
  },
  computed: {
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
      
      // Filtre de recherche
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
    canManageCatalog() {
      const user = this.active_user;
      const groups = user?.groups;
      if (Array.isArray(groups) && groups.length) {
        if (typeof groups[0] === 'string' && typeof this.active_user_is === 'function') {
          return this.active_user_is('admin', 'agent', 'superuser');
        }
        return true;
      }
      return false;
    }
  },
  beforeMount() {
    this.fetchBasicProducts();
    this.fetchShopProductsCount();
    this.fetchCategories();
  },
  ionViewWillEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Catalogue de Référence (Maître)',
      description: 'Ici, vous gérez les produits "standards" disponibles pour toutes les boutiques. Un catalogue bien rempli évite aux commerçants de devoir tout saisir manuellement.',
      elements: [
        { type: 'Navigation', label: 'Filtres', desc: 'Triez les produits par catégorie pour vérifier que tout est bien classé.' },
        { type: 'Action', label: 'Ajouter (+)', desc: 'Créez un nouveau produit modèle (Nom, Catégorie, Image par défaut).' },
        { type: 'Gestion', label: 'Glisser', desc: 'Permet de corriger une erreur sur un nom de produit ou de le supprimer du catalogue global.' }
      ],
      faq: [
        { question: 'Pourquoi ce catalogue ?', answer: 'Lorsqu\'un client crée sa boutique, il peut "piocher" dans ce catalogue pour remplir son stock en un clic au lieu de tout récrire.' },
        { question: 'L\'image est-elle obligatoire ?', answer: 'Non, mais un catalogue avec des images est beaucoup plus professionnel et facile à utiliser pour les clients.' }
      ]
    });
  },
  methods: {
    goHome() {
      const user = this.$store.state.user;
      const groups = user?.groups || [];
      const hasAdmin = groups.some(g => {
        const name = typeof g === 'string' ? g : g.name;
        return name === 'admin' || name === 'superuser';
      });
      if (hasAdmin) {
        this.$router.push('/admin');
      } else {
        this.$router.push('/agent');
      }
    },
    /**
     * Évite l'avertissement Chrome:
     * "Blocked aria-hidden on an element because its descendant retained focus"
     * quand on ouvre un modal depuis un bouton dans l'ion-router-outlet (ex: FAB).
     */
    blurActiveElement() {
      try {
        const el = typeof document !== 'undefined' ? document.activeElement : null;
        if (el && typeof el.blur === 'function') el.blur();
      } catch {
        // no-op
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
      this.loading = true;
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
            // Tri alphabétique global par nom
            this.basicProducts = [...all].sort((a, b) => {
              const na = (a.name || '').toString().toLowerCase();
              const nb = (b.name || '').toString().toLowerCase();
              return na.localeCompare(nb);
            });
            this.totalCatalogueCount = all.length;
            this.loading = false;
          }
        } catch (err) {
          this.loading = false;
          this.errorOrRefresh(err, () => this.fetchBasicProducts());
        }
      };

      fetchPage();
    },
    fetchShopProductsCount() {
      const shop = this.getShopFromLocalStorage?.() ?? this.$store?.state?.shop ?? null;
      const shopId = shop?.id ?? shop;
      if (shopId == null) {
        this.shopProductsCount = null;
        return;
      }
      productsService.getProducts(shopId)
        .then((res) => {
          this.shopProductsCount = res.data.count ?? (res.data.results?.length ?? 0);
        })
        .catch(() => {
          this.shopProductsCount = null;
        });
    },
    async openCreateModal() {
      // Retirer le focus du FAB avant d'ouvrir le modal (sinon aria-hidden warning)
      this.blurActiveElement();
      const modal = await modalController.create({
        component: BasicProductForm,
        componentProps: { mode: 'create' }
      });

      // S'assurer que le focus est retiré juste avant que le modal soit masqué
      modal.addEventListener('ionModalWillDismiss', () => {
        this.blurActiveElement();
      });

      await modal.present();

      const { data, role } = await modal.onDidDismiss();
      if (role === 'confirm') {
        // Si un filtre est actif, il peut masquer le nouveau produit: reset filtres après ajout
        this.filterCategoryId = null;
        this.filterSubCategoryId = null;
        this.filterSubCategories = [];

        // Mise à jour immédiate UI (puis refetch pour être sûr)
        if (data && data.id) {
          const list = this.basicProducts || [];
          const exists = list.some((p) => Number(p.id) === Number(data.id));
          const merged = exists ? list : [...list, data];
          this.basicProducts = [...merged].sort((a, b) => {
            const na = (a.name || '').toString().toLowerCase();
            const nb = (b.name || '').toString().toLowerCase();
            return na.localeCompare(nb);
          });
        }
        // On ne refetch plus immédiatement pour éviter le "flash" où l'API ne renvoie pas encore le produit.
        // L'utilisateur peut toujours rafraîchir manuellement via l'icône refresh.
        this.fetchShopProductsCount();
      }
    },
    getCategoryLabel(product) {
      const sub = product?.sub_category;
      if (sub && typeof sub === 'object') {
        const catName = sub.category?.name || sub.category_name || '';
        return catName ? `${catName} > ${sub.name}` : sub.name;
      }
      return 'Non catégorisé';
    },
    async editProduct(product) {
      // Retirer le focus de l'item cliqué avant d'ouvrir le modal
      this.blurActiveElement();
      const modal = await modalController.create({
        component: BasicProductForm,
        componentProps: { mode: 'edit', product: product }
      });

      // S'assurer que le focus est retiré juste avant que le modal soit masqué
      modal.addEventListener('ionModalWillDismiss', () => {
        this.blurActiveElement();
      });

      await modal.present();

      const { data, role } = await modal.onDidDismiss();
      if (role === 'confirm') {
        // Mise à jour immédiate UI (puis refetch)
        if (data && data.id) {
          const list = this.basicProducts || [];
          const idx = list.findIndex((p) => Number(p.id) === Number(data.id));
          if (idx >= 0) {
            const next = [...list];
            next[idx] = { ...next[idx], ...data };
            this.basicProducts = [...next].sort((a, b) => {
              const na = (a.name || '').toString().toLowerCase();
              const nb = (b.name || '').toString().toLowerCase();
              return na.localeCompare(nb);
            });
          }
        }
        // Idem: pas de refetch immédiat pour ne pas écraser l'UI locale avec une réponse en retard.
        this.fetchShopProductsCount();
      }
    },
    async confirmDelete(product) {
      // Retirer le focus du bouton "Supprimer" (ion-item-option) avant d'afficher l'alert
      this.blurActiveElement();
      const alert = await alertController.create({
        header: 'Confirmer la suppression',
        message: `Êtes-vous sûr de vouloir supprimer "${product.name}" ?`,
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Supprimer',
            role: 'destructive',
            handler: () => {
              this.deleteProduct(product.id);
            }
          }
        ]
      });
      await alert.present();
    },
    async openProductActions(product) {
      // Retirer le focus avant d'afficher l'action sheet
      this.blurActiveElement();
      const sheet = await actionSheetController.create({
        header: product.name || 'Produit',
        buttons: [
          {
            text: 'Modifier',
            icon: createOutline,
            handler: () => this.editProduct(product)
          },
          {
            text: 'Supprimer',
            role: 'destructive',
            icon: trashOutline,
            handler: () => this.confirmDelete(product)
          },
          {
            text: 'Annuler',
            role: 'cancel'
          }
        ]
      });
      await sheet.present();
    },
    deleteProduct(productId) {
      basicProductsService.deleteBasicProduct(productId)
        .then(() => {
          this.blurActiveElement();
          this.showTostMsg('Produit supprimé avec succès.', 'success', 3000);
          this.basicProducts = this.basicProducts.filter(p => Number(p.id) !== Number(productId));
          this.totalCatalogueCount = this.basicProducts.length;
        })
        .catch((err) => {
          if (err.response && err.response.status === 404) {
            this.blurActiveElement();
            this.showTostMsg('Produit supprimé avec succès.', 'success', 3000);
            this.basicProducts = this.basicProducts.filter(p => Number(p.id) !== Number(productId));
            this.totalCatalogueCount = this.basicProducts.length;
          } else {
            this.errorOrRefresh(err, () => this.deleteProduct(productId));
          }
        });
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
        // Garder le premier (généralement le plus ancien ID si trié par ID, mais ici c'est trié par nom)
        // On va trier chaque groupe par ID pour être sûr de garder le plus vieux
        const sorted = [...group].sort((a, b) => a.id - b.id);
        const keeper = sorted[0];
        const extras = sorted.slice(1);
        toDelete.push(...extras.map(p => p.id));
      });

      const alert = await alertController.create({
        header: 'Nettoyage en cours',
        message: `Suppression de ${toDelete.length} copies...`,
        backdropDismiss: false
      });
      // No alert.present() here for better UX, we'll use a toast after

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
    exportToExcel() {
      if (!this.filteredProducts || this.filteredProducts.length === 0) {
        this.showTostMsg("Aucun produit à exporter.", "warning", 3000);
        return;
      }

      const data = this.filteredProducts.map(p => ({
        "ID": p.id,
        "Nom": p.name,
        "Catégorie": this.getCategoryLabel(p),
        "Code Barre": p.barcode || 'N/A',
        "Description": p.description || ''
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Catalogue");
      XLSX.writeFile(wb, `Catalogue_AgaShop_${new Date().toISOString().split('T')[0]}.xlsx`);
      
      this.showTostMsg("Catalogue exporté avec succès.", "success", 2000);
    }
  }
};
</script>

<style lang="scss" scoped>
.catalog-content {
  --background: #f8fafc;
}

.filter-row {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  overflow-x: auto;
  scrollbar-width: none;
  &::-webkit-scrollbar { display: none; }
}

.filter-item {
  flex: 1;
  min-width: 150px;
  --background: white;
  --border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  
  ion-select {
    font-size: 0.9rem;
    font-weight: 500;
  }
}

.catalog-list {
  padding-bottom: 80px;
}

.bp-item {
  --background: white;
  --border-radius: 14px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  border: 1px solid #f1f5f9;
  
  ion-thumbnail {
    width: 48px;
    height: 48px;
    margin-right: 12px;
    img {
      border-radius: 10px;
      object-fit: cover;
    }
  }
}

.bp-title {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
}

.bp-cat {
  font-size: 0.8rem;
  color: var(--ion-color-primary);
  font-weight: 600;
  margin-top: 2px;
}

.bp-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 2px;
}

ion-fab {
  bottom: 72px !important;
  right: 16px !important;
  z-index: 10001 !important;
  
  ion-fab-button {
    --box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  }
}

// Styles du dashboard (pour cohérence avec ShopProducts)
.header-title-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.2;
}

.toolbar-shop-count {
  font-size: 0.75rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
  margin-top: 2px;
  font-weight: normal;
}

.search-toolbar {
  --padding-top: 0;
  --padding-bottom: 8px;
}

.custom-searchbar {
  --background: rgba(255, 255, 255, 0.15);
  --color: white;
  --placeholder-color: rgba(255, 255, 255, 0.6);
  --icon-color: white;
  --clear-button-color: white;
  --border-radius: 12px;
  padding: 0 16px;
  height: 44px;
}
</style>
