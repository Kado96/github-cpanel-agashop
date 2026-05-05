<!--
  * @file BasicProductForm.vue
  * @description Page pour la gestion de Basic Product Form.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="basic-product-form-back-btn" name="back-button" class="back-arrow-white" @click="performClose" fill="clear">
            <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">{{ mode === 'create' ? "Ajout d'un article" : "Modifier l'article" }}</ion-title>
         <ion-buttons slot="end">
          <ion-button id="basic-product-form-close-btn" name="close-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="content ion-padding">
      <ion-grid fixed>
        <ion-row class="ion-justify-content-center">
          <ion-col size="12">
            <div class="container">
              <div class="card">
                <form @submit.prevent="performSubmit" id="basic-product-form">
                  <input
                    type="file"
                    accept="image/*"
                    @change="handleImageChange"
                    style="display: none"
                    ref="fileInput"
                    id="product-image-file"
                    name="image_file"
                  />

                  <div class="image-row">
                    <div class="upload-buttons">
                      <ion-button class="upload-btn" @click="$refs.fileInput.click()" fill="solid" color="primary">
                        <ion-icon slot="start" :icon="imageOutline"></ion-icon>
                        {{ (imagePreview || (product && product.image) || selectedMediaUrl) ? 'Changer' : 'Téléverser' }}
                      </ion-button>
                      
                      <ion-button class="library-btn" @click="openMediaLibrary" fill="outline" color="secondary">
                        <ion-icon slot="start" :icon="imagesOutline"></ion-icon>
                        Bibliothèque
                      </ion-button>
                    </div>

                    <div class="thumb" @click="selectedMediaUrl ? openMediaLibrary() : $refs.fileInput.click()">
                      <img
                        v-if="imagePreview || selectedMediaUrl || (product && product.image)"
                        :src="imagePreview || selectedMediaUrl || product.image"
                        alt="Aperçu"
                      />
                      <div v-else class="thumb-placeholder">
                        <ion-icon :icon="imageOutline"></ion-icon>
                      </div>
                    </div>
                  </div>

                  <!-- Catégorie | Sous-catégorie | Produit | Image -->
                  <div class="field-label-container ion-margin-start">
                    <ion-label for="product-category" color="medium">Catégorie <span class="required">*</span></ion-label>
                  </div>
                  <ion-item class="select-item" lines="none">
                    <ion-select
                      id="product-category"
                      name="category_id"
                      :key="'cat-' + categories.length"
                      v-model="formData.categoryId"
                      placeholder="Choisir une catégorie"
                      interface="alert"
                      @ionChange="onCategoryChange"
                      @click="blurActiveElement"
                      @ionFocus="blurActiveElement"
                    >
                      <ion-select-option
                        v-for="item in categories"
                        :key="String(item.id)"
                        :value="item.id"
                      >
                        {{ item.name }}
                      </ion-select-option>
                    </ion-select>
                  </ion-item>
                  <ion-text v-if="errors.categoryId" class="error" color="danger">
                    * Veuillez choisir une catégorie
                  </ion-text>

                  <div class="field-label-container ion-margin-start">
                    <ion-label for="product-subcategory" color="medium">Sous-catégorie <span class="required">*</span></ion-label>
                  </div>
                  <ion-item class="select-item" lines="none">
                    <ion-select
                      id="product-subcategory"
                      name="sub_category_id"
                      :key="'sub-' + (formData.categoryId || 0) + '-' + subCategories.length"
                      v-model="formData.subCategoryId"
                      placeholder="Choisir une sous-catégorie"
                      interface="alert"
                      @click="blurActiveElement"
                      @ionFocus="blurActiveElement"
                      :disabled="!formData.categoryId"
                    >
                      <ion-select-option
                        v-for="item in subCategories"
                        :key="String(item.id)"
                        :value="item.id"
                      >
                        {{ item.name }}
                      </ion-select-option>
                    </ion-select>
                  </ion-item>
                  <ion-text v-if="errors.subCategoryId" class="error" color="danger">
                    * Veuillez choisir une sous-catégorie
                  </ion-text>

                  <ion-item class="name-item" lines="none">
                    <ion-input
                      id="product-name"
                      name="name"
                      label="Nom du produit"
                      label-placement="stacked"
                      v-model="formData.name"
                      placeholder="Ex: Eau minérale"
                      @keydown="initErrors"
                      autocomplete="name"
                    ></ion-input>
                  </ion-item>
                  <ion-text v-if="errors.name" class="error" color="danger">
                    * Veuillez remplir le nom du produit
                  </ion-text>

                  <ion-button
                    class="submit-btn"
                    color="primary"
                    expand="block"
                    :disabled="loading"
                    type="submit"
                  >
                    <ion-spinner v-if="loading" slot="start"></ion-spinner>
                    <ion-text color="light">Confirmer</ion-text>
                  </ion-button>

                  <!-- Séparateur + Import en masse -->
                  <div class="separator" v-if="isAdminOnly">
                    <span>OU</span>
                  </div>

                  <div v-if="isAdminOnly" class="import-section">
                    <input
                      type="file"
                      accept=".csv,.xlsx,.xls"
                      @change="handleBulkImport"
                      style="display: none"
                      ref="bulkFileInput"
                      id="bulk-import-file"
                      name="bulk_file"
                    />
                    <ion-button
                      class="import-btn"
                      color="secondary"
                      expand="block"
                      :disabled="loading || bulkImporting"
                      @click="$refs.bulkFileInput.click()"
                    >
                      <ion-icon slot="start" :icon="documentTextOutline"></ion-icon>
                      <ion-spinner v-if="bulkImporting" slot="start"></ion-spinner>
                      <ion-text color="light">Importer depuis Excel/CSV</ion-text>
                    </ion-button>
                  </div>
                </form>
              </div>
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
  IonTitle,
  IonButtons,
  IonButton,
  IonIcon,
  IonContent,
  IonItem,
  IonInput,
  IonLabel,
  IonText,
  IonSpinner,
  IonSelect,
  IonSelectOption,
  IonProgressBar,
  modalController
} from '@ionic/vue';

import {
  close,
  imageOutline,
  imagesOutline,
  arrowBackOutline,
  documentTextOutline
} from 'ionicons/icons';

import { basicProductsService, categoriesService, subCategoriesService } from '../../services/api';
import MediaLibrary from '../common/MediaLibrary.vue';

/**
 * Composant BasicProductForm
 * - Gère l'interface et la logique métier de Basic Product Form.
 */
export default {
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonIcon,
    IonContent,
    IonItem,
    IonInput,
    IonLabel,
    IonText,
    IonSpinner,
    IonSelect,
    IonSelectOption,
    IonProgressBar
  },
  props: {
    mode: {
      type: String,
      default: 'create',
      validator: (value) => ['create', 'edit'].includes(value)
    },
    product: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      close,
      imageOutline,
      imagesOutline,
      arrowBackOutline,
      documentTextOutline,
      loading: false,
      bulkImporting: false,
      bulkProgress: { current: 0, total: 0 },
      categories: [],
      subCategories: [],
      formData: {
        categoryId: null,
        subCategoryId: null,
        name: '',
        image: null,
        media: null
      },
      imagePreview: null,
      selectedMediaUrl: null,
      imageFile: null,
      errors: {
        categoryId: false,
        subCategoryId: false,
        name: false
      }
    };
  },
  created() {
    if (this.mode === 'edit' && this.product) {
      this.formData.name = this.product.name || '';

      // Normaliser sub_category: peut être un ID simple, un objet {id, ...} ou un PK imbriqué
      const rawSub = this.product.sub_category;
      let subId = this.product.sub_category_id;
      if (!subId && rawSub) {
        if (typeof rawSub === 'object') {
          subId = rawSub.id ?? null;
        } else {
          subId = rawSub;
        }
      }
      if (subId) {
        this.formData.subCategoryId = Number(subId);
      }

      // Normaliser category: le backend peut renvoyer sub_category_category_id ou un objet category
      let catId = this.product.sub_category_category_id;
      const subObj = (rawSub && typeof rawSub === 'object') ? rawSub : null;
      const rawCat = subObj && subObj.category;
      if (!catId && rawCat) {
        if (typeof rawCat === 'object') {
          catId = rawCat.id ?? null;
        } else {
          catId = rawCat;
        }
      }
      if (catId) {
        this.formData.categoryId = Number(catId);
      }

      if (this.product.media) {
        this.formData.media = this.product.media;
        this.selectedMediaUrl = this.product.image_url; // image_url returns media file url if present
      }
    }
  },
  mounted() {
    // Charger les catégories (avec leurs sous-catégories) puis compléter
    // categoryId/subCategoryId à partir du produit si besoin.
    this.fetchCategories().then(() => {
      // Si on a déjà la catégorie, on charge simplement ses sous-catégories
      if (this.mode === 'edit' && this.formData.categoryId) {
        this.fetchSubCategoriesByCategory(this.formData.categoryId);
        return;
      }

      // Sinon, si on connaît seulement la sous-catégorie, on déduit la catégorie
      if (this.mode === 'edit' && this.formData.subCategoryId && !this.formData.categoryId) {
        const sid = Number(this.formData.subCategoryId);
        const cat = (this.categories || []).find((c) => {
          const subs = (c && (c.subCategories || c.sub_categories)) || [];
          return Array.isArray(subs) && subs.some((s) => Number(s.id) === sid);
        });
        if (cat) {
          this.formData.categoryId = Number(cat.id);
          this.fetchSubCategoriesByCategory(cat.id);
        }
      }
    });
  },
  computed: {
    isAdminOnly() {
      return typeof this.active_user_is === 'function' && this.active_user_is('admin', 'superuser');
    },
    bulkProgressPercent() {
      const { current, total } = this.bulkProgress;
      return total > 0 ? Math.round((current / total) * 100) : 0;
    }
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
    fetchCategories() {
      // Retourner la Promise pour pouvoir faire this.fetchCategories().then(...)
      return categoriesService.getCategories()
        .then((res) => {
          const raw = res.data.results ?? res.data;
          this.categories = Array.isArray(raw) ? raw : [];
        })
        .catch((err) => {
          this.categories = [];
          console.warn('Erreur chargement catégories:', err);
        });
    },
    fetchSubCategoriesByCategory(categoryId) {
      if (!categoryId) {
        this.subCategories = [];
        return;
      }
      const cid = Number(categoryId);
      const cat = this.categories.find((c) => (c && (c.id === categoryId || c.id === cid)));
      const nested = cat && (cat.subCategories || cat.sub_categories);
      if (Array.isArray(nested)) {
        this.subCategories = nested;
        return;
      }
      subCategoriesService.getSubCategories({ category: categoryId })
        .then((res) => {
          const raw = res.data.results ?? res.data;
          this.subCategories = Array.isArray(raw) ? raw : [];
        })
        .catch((err) => {
          this.subCategories = [];
          console.warn('Erreur chargement sous-catégories:', err);
        });
    },
    onCategoryChange(ev) {
      this.formData.subCategoryId = null;
      const id = ev?.detail?.value ?? this.formData.categoryId;
      this.fetchSubCategoriesByCategory(id);
    },
    /**
     * Trouve l'ID de la sous-catégorie à partir des noms Catégorie et Sous-catégorie
     * (utilisé pour l'import Excel/CSV : même liste que les champs de saisie manuels)
     */
    resolveSubCategoryId(categoryName, subcategoryName) {
      const catName = (categoryName || '').toString().trim().toLowerCase();
      const subName = (subcategoryName || '').toString().trim().toLowerCase();
      if (!catName || !subName) return null;
      const cat = this.categories.find(
        (c) => c && (c.name || '').toString().trim().toLowerCase() === catName
      );
      if (!cat) return null;
      const subs = cat.subCategories || cat.sub_categories;
      if (!Array.isArray(subs)) return null;
      const sub = subs.find(
        (s) => s && (s.name || '').toString().trim().toLowerCase() === subName
      );
      return sub ? sub.id : null;
    },
    /**
     * Trouve ou crée la sous-catégorie à partir des noms (pour l'import Excel/CSV).
     * Crée la catégorie et/ou sous-catégorie si elles n'existent pas.
     */
    async resolveOrCreateSubCategoryId(categoryName, subcategoryName) {
      const catName = (categoryName || '').toString().trim();
      const subName = (subcategoryName || '').toString().trim();
      if (!catName || !subName) return null;

      let subId = this.resolveSubCategoryId(categoryName, subcategoryName);
      if (subId != null) return subId;

      // Créer la catégorie si elle n'existe pas
      let cat = this.categories.find(
        (c) => c && (c.name || '').toString().trim().toLowerCase() === catName.toLowerCase()
      );
      if (!cat) {
        try {
          const res = await categoriesService.createCategory({ name: catName });
          cat = res.data;
          if (!cat.subCategories) cat.subCategories = [];
          if (!cat.sub_categories) cat.sub_categories = [];
          this.categories.push(cat);
        } catch (err) {
          console.error('Erreur création catégorie:', err);
          return null;
        }
      }

      // Créer la sous-catégorie si elle n'existe pas
      const catId = cat.id;
      const subs = cat.subCategories || cat.sub_categories || [];
      let sub = Array.isArray(subs) ? subs.find(
        (s) => s && (s.name || '').toString().trim().toLowerCase() === subName.toLowerCase()
      ) : null;
      if (!sub) {
        try {
          const res = await subCategoriesService.createSubCategory({ name: subName, category: catId });
          sub = res.data;
          if (!cat.subCategories) cat.subCategories = [];
          if (!cat.sub_categories) cat.sub_categories = [];
          (cat.subCategories || cat.sub_categories).push(sub);
          return sub.id;
        } catch (err) {
          console.error('Erreur création sous-catégorie:', err);
          return null;
        }
      }
      return sub.id;
    },
    /** Charge tous les produits de base (pagination) pour l'import */
    async fetchAllBasicProducts() {
      const all = [];
      let page = 1;
      const pageSize = 100;
      while (true) {
        // DRF pagination: page + page_size
        const res = await basicProductsService.getBasicProducts({ page, page_size: pageSize });
        const raw = res.data.results ?? res.data;
        const results = Array.isArray(raw) ? raw : [];
        if (results.length === 0) break;
        all.push(...results);
        if (results.length < pageSize) break;
        page++;
      }
      return all;
    },
    /** Trouve un produit de base existant par nom ; préfère même sous-catégorie, sinon un avec sous-catégorie vide (pour compléter) */
    findExistingBasicProduct(existingList, name, subCategoryId) {
      const nameNorm = (name || '').toString().trim().toLowerCase();
      if (!nameNorm) return null;
      const withSameName = existingList.filter((p) => (p.name || '').toString().trim().toLowerCase() === nameNorm);
      if (withSameName.length === 0) return null;
      const pSubId = (p) => p.sub_category ?? p.sub_category_id ?? null;
      const exact = withSameName.find((p) => Number(pSubId(p)) === Number(subCategoryId != null ? subCategoryId : null));
      if (exact) return exact;
      const emptySub = withSameName.find((p) => pSubId(p) == null || pSubId(p) === '');
      return emptySub || withSameName[0];
    },
    /** Vrai si la ligne d'import est identique à l'existant : même nom, même sous-catégorie, même présence d'image */
    isImportRowIdentical(existing, name, subCategoryId, hasImage) {
      const nameNorm = (name || '').toString().trim().toLowerCase();
      const pName = (existing.name || '').toString().trim().toLowerCase();
      if (pName !== nameNorm) return false;
      const pSub = existing.sub_category ?? existing.sub_category_id ?? null;
      if (Number(pSub) !== Number(subCategoryId != null ? subCategoryId : null)) return false;
      const existingHasImage = !!(existing.image && String(existing.image).trim() !== '');
      return existingHasImage === hasImage;
    },
    handleImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.imageFile = file;
        this.formData.media = null;
        this.selectedMediaUrl = null;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async openMediaLibrary() {
      this.blurActiveElement();
      const modal = await modalController.create({
        component: MediaLibrary,
        cssClass: 'media-library-modal'
      });
      
      modal.onDidDismiss().then((result) => {
        if (result.role === 'confirm' && result.data) {
          const selected = result.data;
          this.formData.media = selected.id;
          this.selectedMediaUrl = selected.file;
          this.imageFile = null;
          this.imagePreview = null;
        }
      });
      
      return modal.present();
    },
    initErrors() {
      this.errors.categoryId = false;
      this.errors.subCategoryId = false;
      this.errors.name = false;
    },
    validateForm() {
      this.initErrors();
      let isValid = true;

      if (!this.formData.categoryId) {
        this.errors.categoryId = true;
        isValid = false;
      }

      if (!this.formData.subCategoryId) {
        this.errors.subCategoryId = true;
        isValid = false;
      }

      if (!this.formData.name || this.formData.name.trim() === '') {
        this.errors.name = true;
        isValid = false;
      }

      return isValid;
    },
    async performSubmit() {
      if (!this.validateForm()) {
        this.showTostMsg('Veuillez remplir tous les champs requis.', 'danger', 3000);
        return;
      }

      this.loading = true;

      try {
        let payload;
        let saved = null;

        // Si on a une image à uploader, on utilise FormData
        if (this.imageFile) {
          payload = new FormData();
          payload.append('name', this.formData.name);
          payload.append('image', this.imageFile);
          payload.append('sub_category', this.formData.subCategoryId);
        } else {
          payload = {
            name: this.formData.name,
            sub_category: this.formData.subCategoryId
          };
          
          if (this.formData.media) {
            payload.media = this.formData.media;
          }
        }

        if (this.mode === 'create') {
          const res = await basicProductsService.createBasicProduct(payload);
          saved = res?.data ?? null;
          this.showTostMsg('Produit créé avec succès !', 'success', 3000);
        } else {
          const res = await basicProductsService.updateBasicProduct(this.product.id, payload);
          saved = res?.data ?? null;
          this.showTostMsg('Produit modifié avec succès !', 'success', 3000);
        }

        // Important: retirer le focus AVANT dismiss pour éviter aria-hidden/focus warning
        this.blurActiveElement();
        modalController.dismiss(saved, 'confirm');
      } catch (err) {
        this.errorOrRefresh(err, () => this.performSubmit());
      } finally {
        this.loading = false;
      }
    },
    async handleBulkImport(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.bulkImporting = true;
      const fileName = file.name.toLowerCase();
      let products = [];

      try {
        if (fileName.endsWith('.csv')) {
          products = await this.parseCSV(file);
        } else if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
          try {
            products = await this.parseExcel(file);
          } catch (excelErr) {
            // Si Excel échoue, informer l'utilisateur
            this.showTostMsg('Erreur lors du traitement du fichier Excel. Vérifiez le format ou utilisez CSV.', 'warning', 5000);
            this.bulkImporting = false;
            return;
          }
        } else {
          this.showTostMsg('Format de fichier non supporté. Utilisez CSV ou Excel.', 'danger', 4000);
          this.bulkImporting = false;
          return;
        }

        if (products.length === 0) {
          this.showTostMsg('Aucun produit trouvé dans le fichier.', 'warning', 4000);
          this.bulkImporting = false;
          return;
        }

        // Charger les catégories (avec sous-catégories) pour faire correspondre les noms du fichier aux IDs
        if (this.categories.length === 0) {
          const catRes = await categoriesService.getCategories();
          const raw = catRes.data.results ?? catRes.data;
          this.categories = Array.isArray(raw) ? raw : [];
        }

        // Charger les produits de base existants pour : créer si absent, compléter si vide/incomplet, ignorer si identique
        const existingProducts = await this.fetchAllBasicProducts();

        this.bulkProgress = { current: 0, total: products.length };

        let createdCount = 0;
        let updatedCount = 0;
        let skippedCount = 0;
        let errorCount = 0;
        const errors = [];

        for (let i = 0; i < products.length; i++) {
          this.bulkProgress = { current: i + 1, total: products.length };
          const product = products[i];
          const subCategoryId = await this.resolveOrCreateSubCategoryId(product.category, product.subcategory);
          const hasImage = !!(product.imageUrl && product.imageUrl.trim());

          try {
            const existing = this.findExistingBasicProduct(existingProducts, product.name, subCategoryId);

            if (!existing) {
              // Absent : créer
              const payload = new FormData();
              payload.append('name', product.name);
              if (subCategoryId != null) payload.append('sub_category', subCategoryId);
              if (hasImage) {
                const imageBlob = await this.urlToBlob(product.imageUrl);
                if (imageBlob) payload.append('image', imageBlob, `product_${i}.jpg`);
              }
              const created = await basicProductsService.createBasicProduct(payload);
              createdCount++;
              const newId = created?.data?.id;
              if (newId) {
                existingProducts.push({ id: newId, name: product.name, sub_category: subCategoryId, sub_category_id: subCategoryId, image: hasImage ? product.imageUrl : null });
              }
              continue;
            }

            if (this.isImportRowIdentical(existing, product.name, subCategoryId, hasImage)) {
              // Identique : passer
              skippedCount++;
              continue;
            }

            // Vide ou incomplet : compléter / remplacer avec les données du fichier
            const needsSub = subCategoryId != null && (existing.sub_category == null || existing.sub_category_id == null);
            const needsImage = hasImage && !existing.image;
            if (!needsSub && !needsImage) {
              skippedCount++;
              continue;
            }

            const payload = new FormData();
            if (needsSub) payload.append('sub_category', subCategoryId);
            if (needsImage) {
              const imageBlob = await this.urlToBlob(product.imageUrl);
              if (imageBlob) payload.append('image', imageBlob, `product_${i}.jpg`);
            }
            await basicProductsService.updateBasicProduct(existing.id, payload);
            updatedCount++;
            if (existing.sub_category == null && needsSub) existing.sub_category = subCategoryId;
            if (!existing.image && needsImage) existing.image = true;
          } catch (err) {
            errorCount++;
            errors.push(`${product.name}: ${err.response?.data?.message || err.message}`);
          }
        }

        const parts = [];
        if (createdCount > 0) parts.push(`${createdCount} créé(s)`);
        if (updatedCount > 0) parts.push(`${updatedCount} mis à jour`);
        if (skippedCount > 0) parts.push(`${skippedCount} identique(s) ou sans changement`);
        if (errorCount > 0) parts.push(`${errorCount} erreur(s)`);
        this.showTostMsg(parts.length ? parts.join('. ') : 'Aucun produit traité.', errorCount > 0 ? 'warning' : 'success', 5000);
        if (errors.length) console.error('Erreurs import:', errors);

        // Fermer le modal et rafraîchir la liste
        modalController.dismiss(null, 'confirm');
      } catch (err) {
        console.error('Erreur lors de l\'import:', err);
        this.showTostMsg('Erreur lors de l\'import du fichier. Vérifiez le format.', 'danger', 5000);
      } finally {
        this.bulkImporting = false;
        this.bulkProgress = { current: 0, total: 0 };
        event.target.value = '';
      }
    },
    async parseCSV(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          try {
            const text = e.target.result;
            const lines = text.split('\n').filter(line => line.trim());
            const products = [];
            const headers = ['catégorie', 'sous-catégorie', 'produit', 'image'];
            const startIndex = lines.length > 0 && headers.some(h => lines[0].toLowerCase().includes(h)) ? 1 : 0;

            for (let i = startIndex; i < lines.length; i++) {
              const line = lines[i].trim();
              if (!line) continue;
              const parts = line.split(/[,;\t]/).map(p => p.trim().replace(/^["']|["']$/g, ''));
              const category = parts[0] || '';
              const subcategory = parts[1] || '';
              const name = parts[2] || '';
              const imageUrl = (parts[3] || '').trim() || null;
              if (name) {
                products.push({ name, imageUrl, category, subcategory });
              }
            }
            resolve(products);
          } catch (err) {
            reject(err);
          }
        };
        reader.onerror = reject;
        reader.readAsText(file);
      });
    },
    async parseExcel(file) {
      let XLSX;
      try {
        const xlsxModule = await import('xlsx');
        XLSX = xlsxModule.default || xlsxModule;
      } catch (err) {
        console.error('Erreur lors du chargement de xlsx:', err);
        throw new Error('Bibliothèque Excel non disponible. Utilisez CSV ou vérifiez l\'installation: npm install xlsx');
      }
      if (!XLSX || typeof XLSX.read !== 'function' || typeof XLSX.utils !== 'object') {
        throw new Error('Bibliothèque Excel non disponible. Utilisez un fichier CSV.');
      }

      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
            const jsonData = XLSX.utils.sheet_to_json(firstSheet, { defval: '' });

            const products = jsonData
              .map(row => {
                const category = row['Catégorie'] ?? row['catégorie'] ?? '';
                const subcategory = row['Sous-catégorie'] ?? row['sous-catégorie'] ?? '';
                const name = (row['Produit'] ?? row['produit'] ?? row['Nom'] ?? row['nom'] ?? '').toString().trim();
                const imageUrl = (row['Image'] ?? row['image'] ?? '').toString().trim() || null;
                return { name, imageUrl, category, subcategory };
              })
              .filter(p => p.name);

            resolve(products);
          } catch (err) {
            reject(err);
          }
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
      });
    },
    async urlToBlob(url) {
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Impossible de télécharger l\'image');
        return await response.blob();
      } catch (err) {
        console.warn('Erreur téléchargement image:', err);
        return null;
      }
    },
    performClose() {
      // Important: retirer le focus AVANT dismiss pour éviter aria-hidden/focus warning
      this.blurActiveElement();
      return modalController.dismiss(null, 'cancel');
    }
  }
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

.content {
  --background: #f6f7fb;
}

.container {
  padding: 16px;
}

.card {
  background: #ffffff;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);

  .image-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;

    .upload-buttons {
      display: flex;
      flex-direction: column;
      gap: 8px;
      flex: 1;
    }

    .upload-btn, .library-btn {
      --border-radius: 12px;
      margin: 0;
      height: 48px;
      font-weight: 600;
    }
  }
}

.thumb {
  width: 100%;
  height: 220px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-placeholder ion-icon {
  font-size: 42px;
  opacity: 0.65;
}

.select-item,
.name-item {
  margin-top: 14px;
  --background: #ffffff;
  --border-color: rgba(0, 0, 0, 0.08);
  --border-radius: 12px;
}

.select-item ion-select {
  width: 100%;
  max-width: 100%;
}

.submit-btn {
  margin-top: 16px;
  height: 46px;
  --border-radius: 12px;
  font-weight: 800;
  text-transform: none;
}

.error {
  font-size: 0.75em !important;
  margin-top: 6px;
  margin-left: 6px;
  display: block;
}

.separator {
  display: flex;
  align-items: center;
  margin: 20px 0;
  text-align: center;
}

.separator::before,
.separator::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.separator span {
  padding: 0 12px;
  color: rgba(0, 0, 0, 0.5);
  font-size: 0.9rem;
  font-weight: 500;
}

.import-section {
  margin-top: 8px;
}

.import-btn {
  height: 46px;
  --border-radius: 12px;
  font-weight: 800;
  text-transform: none;
}

.import-progress {
  margin-top: 10px;
}
.import-progress ion-progress-bar {
  height: 8px;
  border-radius: 4px;
}
.import-progress-text {
  display: block;
  margin-top: 4px;
  font-size: 0.8rem;
  text-align: center;
}
.import-hint {
  display: block;
  margin-top: 8px;
  font-size: 0.75rem;
  text-align: center;
  opacity: 0.7;
}
</style>
