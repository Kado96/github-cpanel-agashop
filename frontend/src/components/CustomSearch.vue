<!--
  * @file CustomSearch.vue
  * @description Page pour la gestion de Custom Search.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="primary">
          <ion-buttons slot="start">
            <ion-button class="back-arrow-white" @click="performClose" fill="clear">
              <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
            </ion-button>
          </ion-buttons>
          <ion-title color="light">Recherche avancée</ion-title>
          <ion-buttons slot="end">
            <ion-button color="light" @click="performClose">
              <ion-icon :icon="close"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
  
      <ion-content class="ion-padding">
        <p class="ion-text-center ion-margin-bottom">{{ introMessage }}</p>
        <p class="ion-text-center ion-margin-bottom hint-datetime">
          <ion-text color="medium">Choisissez la date de début et la date de fin, puis cliquez sur Valider.</ion-text>
        </p>
        <ion-list lines="full">
          <ion-item-group class="ion-margin-horizontal ion-margin-bottom">
            <form @submit.prevent="perfromSearch">
              <div class="ion-margin-vertical">
                <ion-label class="ion-padding-start">Du (date de début)</ion-label>
                <ion-datetime
                  presentation="date"
                  :min="minDate"
                  :max="maxDate"
                  :value="filters.du || undefined"
                  @ion-change="onDuChange"
                  :show-default-buttons="false"
                  show-default-time-label="false"
                  locale="fr-FR"
                ></ion-datetime>
              </div>
              <div class="ion-margin-vertical">
                <ion-label class="ion-padding-start">Au (date de fin)</ion-label>
                <ion-datetime
                  presentation="date"
                  :min="filters.du || minDate"
                  :max="maxDate"
                  :value="filters.au || undefined"
                  @ion-change="onAuChange"
                  :show-default-buttons="false"
                  show-default-time-label="false"
                  locale="fr-FR"
                ></ion-datetime>
              </div>
              <ion-button
                color="primary"
                expand="block"
                type="submit"
                :disabled="loading || !canSubmit"
              >
                <ion-spinner v-if="loading" slot="start"></ion-spinner>
                <ion-text color="light">Valider</ion-text>
              </ion-button>
            </form>
          </ion-item-group>
        </ion-list>
      </ion-content>
  
    </ion-page>
  </template>
  
  <script>
  import {
    IonButton,
    IonButtons,
    IonContent,
    IonDatetime,
    IonHeader,
    IonIcon,
    IonItemGroup,
    IonLabel,
    IonList,
    IonPage,
    IonSpinner,
    IonText,
    IonTitle,
    IonToolbar,
    modalController
} from '@ionic/vue';

  import {
    close,
    arrowBackOutline
  } from 'ionicons/icons'
  
  /**
 * Composant CustomSearch
 * - Gère l'interface et la logique métier de Custom Search.
 */
export default {
  
    name: 'TransactionsView',
    components:{
        IonPage,
        IonHeader,
        IonToolbar,
        IonTitle,
        IonButtons,
        IonIcon,
        IonContent,
        IonList,
        IonItemGroup,
        IonDatetime,
        IonLabel,
        IonButton,
        IonText,
        IonSpinner
    },
    data() {
      return {
        filters:{
            du:"",
            au:"",
            product:null,
            amount:0,
        },
        loading: false,
        close,
        arrowBackOutline
      };
    },
    props: {
      shopIdProp: { type: [Number, String], default: null },
      initialDu: { type: String, default: '' },
      initialAu: { type: String, default: '' },
      /** Message d’intro selon la page : achats, ventes, statistiques… */
      introMessage: { type: String, default: 'Choisissez la période pour filtrer les achats.' },
    },
    created() {
      if (this.initialDu) this.filters.du = this.initialDu;
      if (this.initialAu) this.filters.au = this.initialAu;
    },
    computed: {
      minDate() {
        return '2000-01-01';
      },
      maxDate() {
        const d = new Date();
        return d.toISOString().slice(0, 10);
      },
      /** Les deux dates doivent être choisies pour activer le filtre */
      canSubmit() {
        const du = (this.filters.du || '').trim();
        const au = (this.filters.au || '').trim();
        return !!du && !!au;
      },
    },
    methods: {
        performClose() {
          return modalController.dismiss(null, 'cancel');
        },
        onDuChange(e) {
          const v = e.detail?.value;
          this.filters.du = v ? String(v).slice(0, 10) : '';
        },
        onAuChange(e) {
          const v = e.detail?.value;
          this.filters.au = v ? String(v).slice(0, 10) : '';
        },
        perfromSearch() {
          if (!this.canSubmit) {
            this.showTostMsg('Veuillez choisir les deux dates (Du et Au), puis cliquez sur Valider.', 'warning', 4000);
            return;
          }
          const du = (this.filters.du || '').trim();
          const au = (this.filters.au || '').trim();
          return modalController.dismiss({ ...this.filters, du, au }, 'confirm');
        },
    },
  
  };
  </script>
  
  <style lang="scss" scoped>
  
  ion-header ion-toolbar {
    --border-radius: 16px 16px 0 0;
  }
  ion-header ion-buttons[slot="start"] ion-button.back-arrow-white,
  ion-header ion-buttons[slot="start"] ion-button.back-arrow-white ion-icon {
    --color: #fff;
    color: #fff;
  }
  .hint-datetime {
    font-size: 0.9rem;
    line-height: 1.3;
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
  