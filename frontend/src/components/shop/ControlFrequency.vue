<!--
  * @file ControlFrequency.vue
  * @description Page pour la gestion de Control Frequency.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="primary">
          <ion-buttons slot="start">
            <ion-button id="control-freq-back-btn" name="back-button" class="back-arrow-white" @click="performClose" fill="clear">
              <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
            </ion-button>
          </ion-buttons>
          <ion-title color="light">Fréquence de contrôle</ion-title>
          <ion-buttons slot="end">
            <ion-button id="control-freq-close-btn" name="close-button" color="light" @click="performClose">
              <ion-icon :icon="close"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
  
      <ion-content class="ion-padding">
        <p class="ion-text-center ion-margin-bottom">
          Durée pendant laquelle un produit reste dans «&nbsp;Déjà contrôlés&nbsp;». Après ce délai, il passe dans «&nbsp;Non contrôlés&nbsp;». Indiquez uniquement minutes, heures ou jours.
        </p>
        <ion-list lines="full">
                <ion-item-group class="ion-margin-horizontal ion-margin-bottom">
                    <form >                    
                    <div class="ion-margin-vertical">
                        <ion-item>
                            <ion-input 
                                id="control-minutes"
                                name="minutes"
                                label="Minutes : "
                                label-placement="stacked"
                                :disabled="minutesDisabled"
                                v-model.number="control_frequency.minutes"
                                placeholder="Après combien de minutes (ex: 1)"
                                @keydown="initErros"
                                type="number"
                                min="0">
                            </ion-input>
                        </ion-item>
                        <ion-text v-if="errors.minutes.empty" class="error" color="danger">
                            * Minutes négatives non permises
                        </ion-text>
                    </div>

                    <div class="ion-margin-vertical">
                        <ion-item>
                            <ion-input 
                                id="control-hours"
                                name="hours"
                                label="Heures : "
                                label-placement="stacked"
                                :disabled="hoursDisabled"
                                v-model.number="control_frequency.hours"
                                placeholder="Après autant d'heures" 
                                @keydown="initErros"
                                type="number"
                                min="0">
                            </ion-input>
                        </ion-item>
                        <ion-text v-if="errors.hours.empty" class="error" color="danger">
                            * Heures négatives non permises
                        </ion-text>
                    </div>

                    <div class="ion-margin-vertical">
                        <ion-item>
                            <ion-input 
                                id="control-days"
                                name="days"
                                label="Jours : "
                                :disabled="daysDisabled"
                                label-placement="stacked"
                                v-model.number="control_frequency.days"
                                placeholder="Après autant de jours" 
                                @keydown="initErros"
                                type="number"
                                min="0">
                            </ion-input>
                        </ion-item>
                        <ion-text v-if="errors.days.empty" class="error" color="danger">
                            * Jours négatives non permises
                        </ion-text>
                    </div>
                    <ion-button
                        color="secondary"
                        expand="block"
                        :disabled="loading"
                        @click="validateControlFrequency"
                    >
                        <ion-spinner v-if="loading" slot="start"></ion-spinner>
                        <ion-text color="light" >Valider</ion-text>
                    </ion-button>
                    </form>
                </ion-item-group>
        </ion-list>
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
    IonSpinner
  
  } from '@ionic/vue';

  import {
    close,
    arrowBackOutline
  } from 'ionicons/icons'
  import { controlFrequencyService } from '../../services/api'
  
  /**
 * Composant ControlFrequency
 * - Gère l'interface et la logique métier de Control Frequency.
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
        IonSpinner
    },
    props:["productProp"],
    data() {
      return {
        isNew:false,
        controlFrequencyId:null,
        daysDisabled:false,
        hoursDisabled:false,
        minutesDisabled:false,
        control_frequency:{
            minutes:0,
            hours:0,
            days:0,
        },
        loading:false,
        errors:{
            minutes:{ empty:false, custom:false },
            hours:{ empty:false, custom:false },
            days:{ empty:false, custom:false },
        },
        close,
        arrowBackOutline
      };
    },
    created(){
        this.fetchControlFrequency()
    },
    watch:{
        "control_frequency.minutes"(new_val){
            if (new_val > 0) {
                this.control_frequency.hours = 0
                this.control_frequency.days = 0
                this.hoursDisabled = true
                this.daysDisabled = true
            } else {
                this.hoursDisabled = false
                this.daysDisabled = false
            }
        },
        "control_frequency.hours"(new_val){
            if(new_val>0){
                this.control_frequency.minutes = 0
                this.control_frequency.days = 0
                this.minutesDisabled = true
                this.daysDisabled = true
            } else {
                this.minutesDisabled = false
                this.daysDisabled = false
            }
        },
        "control_frequency.days"(new_val){
            if(new_val>0){
                this.control_frequency.minutes = 0
                this.control_frequency.hours = 0
                this.minutesDisabled = true
                this.hoursDisabled = true
            } else {
                this.minutesDisabled = false
                this.hoursDisabled = false
            }
        }
    },
    methods: {
        initErros(){
            this.errors.minutes.empty = false;
            this.errors.hours.empty = false;
            this.errors.days.empty = false;
        },
        performClose() {
          return modalController.dismiss(null, 'cancel');
        },
        validateInputs(){
            this.initErros()
            if (this.control_frequency.minutes < 0) {
                this.errors.minutes.empty = true
                return false
            }
            if (this.control_frequency.days < 0) {
                this.errors.days.empty = true
                return false
            }
            if (this.control_frequency.hours < 0) {
                this.errors.hours.empty = true
                return false
            }
            return true
        },
        validateControlFrequency(){
            if(this.validateInputs()){
                this.loading=true
                let shop = this.getShopFromLocalStorage()
                if(!shop) {
                    this.loading=false
                    this.showTostMsg("Boutique introuvable", "danger", 5000)
                    return
                }
                this.control_frequency.shop = shop.id
                if(this.isNew){
                    controlFrequencyService.createControlFrequency(this.control_frequency)
                    .then(()=>{
                        this.loading=false
                        this.showTostMsg("Fréquence enregistrée.", "success",5000)
                        modalController.dismiss({ updated: true }, "confirm")
                    }).catch((err)=>{
                        this.loading=false
                        this.errorOrRefresh(err, () => this.validateControlFrequency())
                    })
                }else{
                    controlFrequencyService.updateControlFrequency(this.controlFrequencyId, this.control_frequency)
                    .then(()=>{
                        this.loading=false
                        this.showTostMsg("Fréquence mise à jour.", "success",5000)
                        modalController.dismiss({ updated: true }, "confirm")
                    }).catch((err)=>{
                        this.loading=false
                        this.errorOrRefresh(err, () => this.validateControlFrequency())
                    }) 
                }
                      
            }
        },
        fetchControlFrequency(){
            this.loading=true
            let shop = this.getShopFromLocalStorage()
            if(!shop) {
                this.loading=false
                this.showTostMsg("Boutique introuvable", "danger", 5000)
                return
            }
            controlFrequencyService.getControlFrequency(shop.id)
            .then((res)=>{
                this.loading=false
                if(res.data.results.length>0){
                    const f = res.data.results[0]
                    this.controlFrequencyId = f.id
                    this.control_frequency.minutes = f.minutes != null ? f.minutes : 0
                    this.control_frequency.days = f.days
                    this.control_frequency.hours = f.hours
                    if (f.minutes > 0) {
                        this.minutesDisabled = false
                        this.hoursDisabled = true
                        this.daysDisabled = true
                    } else if (f.hours > 0) {
                        this.minutesDisabled = true
                        this.daysDisabled = true
                    } else if (f.days > 0) {
                        this.minutesDisabled = true
                        this.hoursDisabled = true
                    }
                }else{
                    this.isNew = true
                }
            }).catch((err)=>{
                this.loading=false
                this.errorOrRefresh(err, () => this.fetchControlFrequency())
            })  
        }
    },
  
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
  
  ion-content {
    ion-list {
      ion-item {
        --min-height: 56px;
      }
      ion-list-header ion-label {
        font-weight: bold;
        font-size: 1.8em;
      }
      ion-input, ion-text {
        font-size: 1em;
      }
      ion-button {
        height: 2.5em;
        margin-top: 8px;
        ion-text {
          font-size: 1.3em;
          font-weight: bold;
        }
        ion-spinner {
          margin-right: 0.9em;
        }
      }
      .error {
        font-size: 0.75em !important;
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
  