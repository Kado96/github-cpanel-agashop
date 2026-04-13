<!--
  * @file EditShop.vue
  * @description Page pour la gestion de Edit Shop.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar class="header-toolbar">
        <ion-buttons slot="start">
          <ion-button id="edit-shop-back-btn" name="back-button" class="back-arrow-white" @click="performClose" fill="clear">
            <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title">
            <ion-icon :icon="createOutline" class="header-icon"></ion-icon>
            Modifier la Boutique
          </div>
        </ion-title>
        <ion-buttons slot="end">
          <ion-button id="edit-shop-close-btn" name="close-button" color="light" @click="performClose">
            <ion-icon :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="edit-shop-content">
      <ion-grid fixed>
        <ion-row class="ion-justify-content-center">
          <ion-col size="12">

            <!-- Hero section -->
            <div class="hero-section">
              <div class="hero-emoji">✏️</div>
              <p class="hero-subtitle">Mettez à jour les informations de votre point de vente</p>
            </div>

            <div class="form-card">
              <form @submit.prevent="performUpdateShop">

                <!-- Section: Identité -->
                <div class="section-header">
                  <ion-icon :icon="storefrontOutline" class="section-icon"></ion-icon>
                  <span>Identité de la boutique</span>
                </div>

                <div class="field-group">
                  <label for="edit-shop-name" class="field-label">
                    Nom de la boutique <span class="required">*</span>
                  </label>
                  <div class="input-wrapper" :class="{ 'input-error': errors.name.empty, 'input-focused': focusedField === 'name' }">
                    <ion-icon :icon="storefrontOutline" class="input-icon"></ion-icon>
                    <ion-input 
                      id="edit-shop-name"
                      name="shop-name"
                      v-model="editData.name"
                      placeholder="Nom de la boutique" 
                      @ionFocus="focusedField = 'name'"
                      @ionBlur="focusedField = ''"
                      @keydown="initErrors"
                      type="text"
                      autocomplete="organization"
                      required>
                    </ion-input>
                  </div>
                </div>

                <!-- Section: Localisation -->
                <div class="section-header">
                  <ion-icon :icon="locationOutline" class="section-icon"></ion-icon>
                  <span>Localisation</span>
                </div>

                <!-- Province -->
                <div class="field-group">
                  <label for="edit-shop-province" class="field-label">
                    Province <span class="required">*</span>
                  </label>
                  <div class="input-wrapper select-wrapper" :class="{ 'input-error': errors.province.empty }">
                    <ion-icon :icon="mapOutline" class="input-icon"></ion-icon>
                    <ion-select 
                      id="edit-shop-province"
                      name="province"
                      interface="popover"
                      v-model="editData.province" 
                      placeholder="Sélectionner une province">
                      <ion-select-option 
                        v-for="item in provinces"
                        :key="item"
                        :value="item">{{item}}</ion-select-option>
                    </ion-select>
                  </div>
                </div>

                <!-- Commune -->
                <div class="field-group">
                  <label for="edit-shop-commune" class="field-label">
                    Commune <span class="required">*</span>
                  </label>
                  <div class="input-wrapper select-wrapper" :class="{ 'input-error': errors.commune.empty }">
                    <ion-icon :icon="mapOutline" class="input-icon"></ion-icon>
                    <ion-select 
                      id="edit-shop-commune"
                      name="commune"
                      interface="popover"
                      v-model="editData.commune" 
                      placeholder="Sélectionner une commune">
                      <ion-select-option 
                        v-for="item in communes"
                        :key="item"
                        :value="item">{{item}}</ion-select-option>
                    </ion-select>
                  </div>
                </div>

                <!-- Quartier -->
                <div class="field-group">
                  <label for="edit-shop-quarter" class="field-label">
                    Quartier / Colline <span class="required">*</span>
                  </label>
                  <div class="input-wrapper" :class="{ 'input-error': errors.quarter.empty, 'input-focused': focusedField === 'quarter' }">
                    <ion-icon :icon="homeOutline" class="input-icon"></ion-icon>
                    <ion-input 
                      id="edit-shop-quarter"
                      name="quarter"
                      v-model="editData.quarter"
                      placeholder="Quartier" 
                      @ionFocus="focusedField = 'quarter'"
                      @ionBlur="focusedField = ''"
                      @keydown="initErrors"
                      type="text"
                      autocomplete="address-level3">
                    </ion-input>
                  </div>
                </div>

                <!-- Adresse -->
                <div class="field-group">
                  <label for="edit-shop-address" class="field-label">
                    Adresse précise <span class="required">*</span>
                  </label>
                  <div class="input-wrapper" :class="{ 'input-error': errors.address.empty, 'input-focused': focusedField === 'address' }">
                    <ion-icon :icon="navigateOutline" class="input-icon"></ion-icon>
                    <ion-input 
                      id="edit-shop-address"
                      name="address"
                      v-model="editData.address"
                      placeholder="Adresse complète" 
                      @ionFocus="focusedField = 'address'"
                      @ionBlur="focusedField = ''"
                      @keydown="initErrors"
                      type="text"
                      autocomplete="street-address">
                    </ion-input>
                  </div>
                </div>

                <!-- Submit Button -->
                <div class="submit-section">
                  <button
                    type="submit"
                    class="submit-btn"
                    :class="{ 'btn-loading': loading }"
                    :disabled="loading"
                  >
                    <ion-spinner v-if="loading" name="crescent" class="btn-spinner"></ion-spinner>
                    <ion-icon v-else :icon="saveOutline" class="btn-icon"></ion-icon>
                    <span>{{ loading ? 'Mise à jour...' : 'Sauvegarder les modifications' }}</span>
                  </button>
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
  IonTitle,
  IonContent,
  IonButton,
  IonButtons,
  IonIcon,
  IonInput,
  modalController,
  IonSelect,
  IonSelectOption,
  IonSpinner,
  IonGrid,
  IonRow,
  IonCol
} from '@ionic/vue';

import {
  close,
  arrowBackOutline,
  storefrontOutline,
  locationOutline,
  mapOutline,
  homeOutline,
  navigateOutline,
  alertCircleOutline,
  checkmarkCircleOutline,
  createOutline,
  saveOutline
} from 'ionicons/icons'
import { shopsService, provincesService } from '../../services/api'

/**
 * Composant EditShop
 * - Gère l'interface et la logique métier de Edit Shop.
 */
export default {
  name: 'EditShop',
  components: {
    IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
    IonButton, IonButtons, IonIcon, IonInput, IonSelect,
    IonSelectOption, IonSpinner, IonGrid, IonRow, IonCol
  },
  props: {
    shop: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      editData: {
        id: null,
        name: '',
        province: '',
        commune: '',
        quarter: '',
        address: ''
      },
      provinces: [],
      communes: [],
      provinces_communes: [],
      loading: false,
      focusedField: '',
      errors: {
        name: { empty: false },
        province: { empty: false },
        commune: { empty: false },
        quarter: { empty: false },
        address: { empty: false }
      },
      close, arrowBackOutline, storefrontOutline, locationOutline,
      mapOutline, homeOutline, navigateOutline, alertCircleOutline,
      checkmarkCircleOutline, createOutline, saveOutline
    };
  },
  created() {
    if (this.shop) {
      this.editData.id = this.shop.id;
      this.editData.name = this.shop.name || '';
      this.editData.province = this.shop.province || '';
      this.editData.commune = this.shop.commune || '';
      this.editData.quarter = this.shop.quarter || '';
      this.editData.address = this.shop.address || '';
    }
    this.fetchProvinces();
  },
  watch: {
    "editData.province": {
      handler(new_val) {
        if (new_val) this.getProvinceCommunes(new_val);
      }
    }
  },
  methods: {
    initErrors() {
      Object.keys(this.errors).forEach(k => this.errors[k].empty = false);
    },
    performClose() {
      return modalController.dismiss(null, 'cancel');
    },
    validateInputs() {
      this.initErrors();
      let isValid = true;
      if (!this.editData.name.trim()) { this.errors.name.empty = true; isValid = false; }
      if (!this.editData.province.trim()) { this.errors.province.empty = true; isValid = false; }
      if (!this.editData.commune.trim()) { this.errors.commune.empty = true; isValid = false; }
      if (!this.editData.quarter.trim()) { this.errors.quarter.empty = true; isValid = false; }
      if (!this.editData.address.trim()) { this.errors.address.empty = true; isValid = false; }
      return isValid;
    },
    fetchProvinces() {
      provincesService.getProvinces()
        .then((res) => {
          this.provinces_communes = res.data;
          this.provinces = Object.keys(this.provinces_communes);
          if (this.editData.province) this.getProvinceCommunes(this.editData.province);
        })
        .catch((err) => this.errorOrRefresh(err, () => this.fetchProvinces()));
    },
    getProvinceCommunes(province) {
      if (this.provinces_communes && province && this.provinces_communes[province])
        this.communes = Object.keys(this.provinces_communes[province]);
      else
        this.communes = [];
    },
    performUpdateShop() {
      if (this.validateInputs()) {
        this.loading = true;
        shopsService.updateShop(this.editData.id, this.editData)
          .then((res) => {
            this.loading = false;
            this.showTostMsg("Boutique mise à jour avec succès !", "success", 3000);
            modalController.dismiss(res.data, "confirm");
          })
          .catch((err) => {
            this.loading = false;
            this.errorOrRefresh(err, () => this.performUpdateShop());
          });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
/* Copié de CreateShop.vue et adapté */
.header-toolbar {
  --background: linear-gradient(135deg, #455a64 0%, #263238 100%);
  --border-width: 0;
}
.header-title { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 1.1rem; }
.header-icon { font-size: 1.3rem; }
.edit-shop-content { --background: #f8fafc; }
.hero-section { text-align: center; padding: 28px 16px 12px; }
.hero-emoji { font-size: 3.2rem; margin-bottom: 8px; }
.hero-subtitle { color: #64748b; font-size: 0.88rem; margin: 0; line-height: 1.4; }

.form-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 24px 20px 28px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 20px 0 14px;
  padding-bottom: 8px;
  border-bottom: 2px solid #f1f5f9;
  color: #1e293b;
  font-weight: 700;
  font-size: 0.9rem;
}

.field-group { margin-bottom: 16px; }
.field-label { display: block; font-size: 0.82rem; font-weight: 600; color: #64748b; margin-bottom: 6px; }
.required { color: #ef4444; }

.input-wrapper {
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  padding: 0 14px;
  min-height: 50px;
  transition: all 0.2s ease;

  &.input-focused { border-color: #f15a24; background: #ffffff; }
  &.input-error { border-color: #ef4444; background: #fef2f2; }

  ion-input { font-size: 0.95rem; }
  ion-select { width: 100%; font-size: 0.95rem; }
}

.input-icon { color: #94a3b8; font-size: 1.2rem; margin-right: 10px; }
.input-focused .input-icon { color: #f15a24; }

.submit-section { margin-top: 28px; }
.submit-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  border: none;
  border-radius: 16px;
  background: #0f172a;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover:not(:disabled) { background: #1e293b; transform: translateY(-2px); }
  &:disabled { opacity: 0.5; }
}

.btn-spinner { width: 20px; height: 20px; }
</style>
