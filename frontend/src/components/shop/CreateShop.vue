<!--
  * @file CreateShop.vue
  * @description Page pour la gestion de Create Shop.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar class="header-toolbar">
        <ion-buttons slot="start">
          <ion-button id="create-shop-back-btn" name="back-button" class="back-arrow-white" @click="performClose" fill="clear">
            <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title">
            <ion-icon :icon="storefrontOutline" class="header-icon"></ion-icon>
            Nouvelle Boutique
          </div>
        </ion-title>
        <ion-buttons slot="end">
          <ion-button id="create-shop-close-btn" name="close-button" color="light" @click="performClose">
            <ion-icon :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="create-shop-content">
      <ion-grid fixed>
        <ion-row class="ion-justify-content-center">
          <ion-col size="12">

            <!-- Hero illustration -->
            <div class="hero-section">
              <div class="hero-emoji">🏪</div>
              <p class="hero-subtitle">Remplissez les informations ci-dessous pour créer votre boutique</p>
            </div>

            <div class="form-card">
              <form @submit.prevent="perfromCreateDepot">

                <!-- Section: Identité -->
                <div class="section-header">
                  <ion-icon :icon="storefrontOutline" class="section-icon"></ion-icon>
                  <span>Identité de la boutique</span>
                </div>

                <div class="field-group">
                  <label for="shop-name" class="field-label">
                    Nom de la boutique <span class="required">*</span>
                  </label>
                  <div class="input-wrapper" :class="{ 'input-error': errors.name.empty, 'input-focused': focusedField === 'name' }">
                    <ion-icon :icon="storefrontOutline" class="input-icon"></ion-icon>
                    <ion-input 
                      id="shop-name"
                      name="name"
                      v-model="shop.name"
                      placeholder="Ex: Ma Super Boutique" 
                      @ionFocus="focusedField = 'name'"
                      @ionBlur="focusedField = ''"
                      @keydown="initErros"
                      type="text"
                      autocomplete="organization"
                      required>
                    </ion-input>
                  </div>
                  <transition name="fade">
                    <p v-if="errors.name.empty" class="error-msg">
                      <ion-icon :icon="alertCircleOutline"></ion-icon>
                      Veuillez saisir le nom de votre boutique
                    </p>
                  </transition>
                </div>

                <!-- Section: Localisation -->
                <div class="section-header">
                  <ion-icon :icon="locationOutline" class="section-icon"></ion-icon>
                  <span>Localisation</span>
                </div>

                <!-- Province -->
                <div class="field-group">
                  <label for="shop-province" class="field-label">
                    Province <span class="required">*</span>
                  </label>
                  <div class="input-wrapper select-wrapper" :class="{ 'input-error': errors.province.empty }">
                    <ion-icon :icon="mapOutline" class="input-icon"></ion-icon>
                    <ion-select 
                      id="shop-province"
                      name="province"
                      interface="popover"
                      :interface-options="{header: 'Choisir la Province'}" 
                      v-model="shop.province" 
                      placeholder="Sélectionner une province">
                      <ion-select-option 
                        v-for="item in provinces"
                        :key="item"
                        :value="item">{{item}}</ion-select-option>
                    </ion-select>
                  </div>
                  <transition name="fade">
                    <p v-if="errors.province.empty" class="error-msg">
                      <ion-icon :icon="alertCircleOutline"></ion-icon>
                      Veuillez choisir la province
                    </p>
                  </transition>
                </div>

                <!-- Commune -->
                <div class="field-group">
                  <label for="shop-commune" class="field-label">
                    Commune <span class="required">*</span>
                  </label>
                  <div class="input-wrapper select-wrapper" :class="{ 'input-error': errors.commune.empty }">
                    <ion-icon :icon="mapOutline" class="input-icon"></ion-icon>
                    <ion-select 
                      id="shop-commune"
                      name="commune"
                      interface="popover"
                      :interface-options="{header: 'Choisir la Commune'}" 
                      v-model="shop.commune" 
                      placeholder="Sélectionner une commune">
                      <ion-select-option 
                        v-for="item in communes"
                        :key="item"
                        :value="item">{{item}}</ion-select-option>
                    </ion-select>
                  </div>
                  <transition name="fade">
                    <p v-if="errors.commune.empty" class="error-msg">
                      <ion-icon :icon="alertCircleOutline"></ion-icon>
                      Veuillez choisir la commune
                    </p>
                  </transition>
                </div>

                <!-- Quartier -->
                <div class="field-group">
                  <label for="shop-quarter" class="field-label">
                    Quartier / Colline <span class="required">*</span>
                  </label>
                  <div class="input-wrapper" :class="{ 'input-error': errors.quarter.custom, 'input-focused': focusedField === 'quarter' }">
                    <ion-icon :icon="homeOutline" class="input-icon"></ion-icon>
                    <ion-input 
                      id="shop-quarter"
                      name="quarter"
                      v-model="shop.quarter"
                      placeholder="Nom du quartier" 
                      @ionFocus="focusedField = 'quarter'"
                      @ionBlur="focusedField = ''"
                      @keydown="initErros"
                      type="text"
                      autocomplete="address-level3">
                    </ion-input>
                  </div>
                  <transition name="fade">
                    <p v-if="errors.quarter.custom" class="error-msg">
                      <ion-icon :icon="alertCircleOutline"></ion-icon>
                      Veuillez saisir le quartier
                    </p>
                  </transition>
                </div>

                <!-- Adresse -->
                <div class="field-group">
                  <label for="shop-address" class="field-label">
                    Adresse précise / Rue <span class="required">*</span>
                  </label>
                  <div class="input-wrapper" :class="{ 'input-error': errors.address.empty, 'input-focused': focusedField === 'address' }">
                    <ion-icon :icon="navigateOutline" class="input-icon"></ion-icon>
                    <ion-input 
                      id="shop-address"
                      name="address"
                      v-model="shop.address"
                      placeholder="Ex: Avenue de la JRR, n°12" 
                      @ionFocus="focusedField = 'address'"
                      @ionBlur="focusedField = ''"
                      @keydown="initErros"
                      type="text"
                      autocomplete="street-address">
                    </ion-input>
                  </div>
                  <transition name="fade">
                    <p v-if="errors.address.empty" class="error-msg">
                      <ion-icon :icon="alertCircleOutline"></ion-icon>
                      Veuillez saisir l'adresse précise
                    </p>
                  </transition>
                </div>

                <!-- Submit -->
                <div class="submit-section">
                  <button
                    type="submit"
                    class="submit-btn"
                    :class="{ 'btn-loading': loading }"
                    :disabled="loading"
                  >
                    <ion-spinner v-if="loading" name="crescent" class="btn-spinner"></ion-spinner>
                    <ion-icon v-else :icon="checkmarkCircleOutline" class="btn-icon"></ion-icon>
                    <span>{{ loading ? 'Création en cours...' : 'Créer ma Boutique' }}</span>
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
  IonLabel,
  IonText,
  IonContent,
  IonItem,
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
  checkmarkCircleOutline
} from 'ionicons/icons'
import { shopsService, provincesService } from '../../services/api'

/**
 * Composant CreateShop
 * - Gère l'interface et la logique métier de Create Shop.
 */
export default {

  name: 'CreateShopView',
  components:{
      IonPage,
      IonHeader,
      IonToolbar,
      IonTitle,
      IonLabel,
      IonText,
      IonContent,
      IonItem,
      IonButton,
      IonButtons,
      IonIcon,
      IonInput,
      IonSelect,
      IonSelectOption,
      IonSpinner,
      IonGrid,
      IonRow,
      IonCol
  },
  created(){
      this.fetchProvinces()
  },
  watch:{
      "shop.province":{
          deep:true,
          handler(new_val){
              if(new_val)
              this.getProvinceCommunes(new_val)
          }
      },
      "communes":{
          deep:true,
          handler(new_val){
              this.communes=new_val
          }
      },
  },
  data() {
    return {
      shop:{
          name:"",
          province:"",
          commune:"",
          quarter:"",
          address:"",
      },
      provinces:[],
      communes:[],
      provinces_communes:[],
      loading:false,
      focusedField: '',
      errors:{
          name:{
              empty:false,
              custom:false
          },
          province:{
              empty:false,
              custom:false
          },
          commune:{
              empty:false,
              custom:false
          },
          quarter:{
              empty:false,
              custom:false
          },
          address:{
              empty:false,
              custom:false
          },
      },
      close,
      arrowBackOutline,
      storefrontOutline,
      locationOutline,
      mapOutline,
      homeOutline,
      navigateOutline,
      alertCircleOutline,
      checkmarkCircleOutline
    };
  },
  methods: {
      initErros(){
          this.errors.name.empty=false
          this.errors.province.empty=false
          this.errors.commune.empty=false
          this.errors.quarter.empty=false
          this.errors.address.empty=false
      },
      performClose() {
        return modalController.dismiss(null, 'cancel');
      },
      validateInputs(){
          this.initErros()
          if(this.shop.name.trim()==""){
              this.errors.name.empty=true
              return false
          }
          if(this.shop.province.trim()==""){
              this.errors.province.empty=true
              return false
          }
          if(this.shop.commune.trim()==""){
              this.errors.commune.empty=true
              return false
          }
          if(this.shop.quarter.trim()==""){
              this.errors.quarter.custom=true
              return false
          }
          if(this.shop.address.trim()==""){
              this.errors.address.empty=true
              return false
          }
          return true
      },
      fetchProvinces(){
          provincesService.getProvinces()
          .then((res)=>{
              this.provinces_communes=res.data
              this.provinces=Object.keys(this.provinces_communes)
          }).catch((err)=>{
              this.loading=false
              this.errorOrRefresh(err, () => this.fetchProvinces())
          })    
      },
      getProvinceCommunes(province){
          if(this.provinces_communes && province)
              this.communes = Object.keys(this.provinces_communes[province])
      },
      perfromCreateDepot(){
          if(this.validateInputs()){
              this.loading=true
              const payload = { ...this.shop }
              if (this.$store.state.user?.account_id) {
                payload.owner = this.$store.state.user.account_id
              }
              shopsService.createShop(payload)
              .then((res)=>{
                  this.loading=false
                  this.$store.state.shops.push(res.data)
                  this.showTostMsg("Votre boutique a été créée avec succès !", "success",5000)
                  modalController.dismiss(null, "confirm")
              }).catch((err)=>{
                  this.loading=false
                  this.errorOrRefresh(err, () => this.perfromCreateDepot())
              })      
          }
      }
  },

};
</script>

<style lang="scss" scoped>

/* ═══ Header ═══ */
.header-toolbar {
  --background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
  --border-width: 0;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 1.1rem;
}

.header-icon {
  font-size: 1.3rem;
}

/* ═══ Content ═══ */
.create-shop-content {
  --background: linear-gradient(180deg, #e3f2fd 0%, #f5f5f5 30%);
}

/* ═══ Hero ═══ */
.hero-section {
  text-align: center;
  padding: 28px 16px 12px;
}

.hero-emoji {
  font-size: 3.2rem;
  margin-bottom: 8px;
  animation: bounceIn 0.6s ease;
}

.hero-subtitle {
  color: #546e7a;
  font-size: 0.88rem;
  margin: 0;
  line-height: 1.4;
}

/* ═══ Card ═══ */
.form-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 24px 20px 28px;
  margin-bottom: 24px;
  box-shadow:
    0 1px 3px rgba(0,0,0,0.06),
    0 8px 24px rgba(30, 136, 229, 0.08);
  border: 1px solid rgba(30, 136, 229, 0.06);
}

/* ═══ Section Headers ═══ */
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 20px 0 14px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e3f2fd;
  color: #1565c0;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.02em;

  &:first-child {
    margin-top: 0;
  }
}

.section-icon {
  font-size: 1.1rem;
  opacity: 0.85;
}

/* ═══ Fields ═══ */
.field-group {
  margin-bottom: 16px;
}

.field-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #455a64;
  margin-bottom: 6px;
  margin-left: 2px;
}

.required {
  color: #ef5350;
  font-weight: 700;
}

/* ═══ Input Wrapper ═══ */
.input-wrapper {
  display: flex;
  align-items: center;
  background: #f8fafb;
  border: 1.5px solid #e0e7ee;
  border-radius: 14px;
  padding: 0 14px;
  min-height: 50px;
  transition: all 0.25s cubic-bezier(.4,0,.2,1);

  &:hover {
    border-color: #90caf9;
    background: #fafcff;
  }

  &.input-focused {
    border-color: #1e88e5;
    background: #ffffff;
    box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1);
  }

  &.input-error {
    border-color: #ef5350;
    background: #fff5f5;
    box-shadow: 0 0 0 3px rgba(239, 83, 80, 0.08);
  }

  ion-input {
    --padding-start: 0;
    --padding-end: 0;
    font-size: 0.95rem;
    --placeholder-color: #b0bec5;
    --color: #263238;
  }

  ion-select {
    width: 100%;
    --placeholder-color: #b0bec5;
    font-size: 0.95rem;
    padding: 0;
  }
}

.select-wrapper {
  padding-right: 4px;
}

.input-icon {
  color: #90a4ae;
  font-size: 1.15rem;
  margin-right: 10px;
  flex-shrink: 0;
  transition: color 0.2s ease;
}

.input-focused .input-icon {
  color: #1e88e5;
}

.input-error .input-icon {
  color: #ef5350;
}

/* ═══ Error Message ═══ */
.error-msg {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #ef5350;
  font-size: 0.75rem;
  font-weight: 600;
  margin: 6px 0 0 4px;
  
  ion-icon {
    font-size: 0.85rem;
    flex-shrink: 0;
  }
}

/* ═══ Submit ═══ */
.submit-section {
  margin-top: 28px;
}

.submit-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, #fb8c00 0%, #f57c00 50%, #ef6c00 100%);
  color: #ffffff;
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(.4,0,.2,1);
  box-shadow:
    0 4px 12px rgba(251, 140, 0, 0.35),
    0 1px 3px rgba(0,0,0,0.1);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    transition: left 0.5s ease;
  }

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow:
      0 6px 20px rgba(251, 140, 0, 0.4),
      0 2px 6px rgba(0,0,0,0.1);
    
    &::before {
      left: 100%;
    }
  }

  &:active:not(:disabled) {
    transform: translateY(0);
    box-shadow:
      0 2px 8px rgba(251, 140, 0, 0.3);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  &.btn-loading {
    background: linear-gradient(135deg, #ffb74d 0%, #ffa726 100%);
  }
}

.btn-icon {
  font-size: 1.3rem;
}

.btn-spinner {
  width: 22px;
  height: 22px;
  color: #ffffff;
}

/* ═══ Transitions ═══ */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* ═══ Animations ═══ */
@keyframes bounceIn {
  0% { transform: scale(0.3); opacity: 0; }
  50% { transform: scale(1.05); }
  70% { transform: scale(0.95); }
  100% { transform: scale(1); opacity: 1; }
}

/* ═══ Responsive ═══ */
@media (min-width: 768px) {
  .form-card {
    padding: 36px 32px 40px;
    margin-top: 8px;
  }
  .hero-section {
    padding: 40px 16px 16px;
  }
  .hero-emoji {
    font-size: 4rem;
  }
}

ion-buttons {
  margin-right: 0.5em;
}

</style>