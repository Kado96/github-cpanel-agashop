<!--
  * @file ShopForm.vue
  * @description Page pour la gestion de Shop Form.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="shop-form-back-btn" name="back-button" class="back-arrow-white" @click="performClose" fill="clear">
            <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">{{ mode === 'create' ? 'Ajouter une boutique' : 'Modifier la boutique' }}</ion-title>
         <ion-buttons slot="end">
          <ion-button id="shop-form-close-btn" name="close-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-grid fixed>
        <ion-row class="ion-justify-content-center">
          <ion-col size="12">
            <ion-list lines="none">
              <ion-item-group>
                <form>
                  <!-- Choix : Créer un nouvel utilisateur ou sélectionner un existant -->
                  <div class="ion-margin-vertical" v-if="mode === 'create'">
                    <ion-label for="shop-user-mode" class="field-label ion-margin-start">Mode de sélection du propriétaire</ion-label>
                    <ion-item>
                      <ion-select
                        id="shop-user-mode"
                        name="userSelectionMode"
                        :interface-options="{header: 'Sélectionner une option'}"
                        v-model="formData.userSelectionMode"
                        placeholder="Choisir une option"
                        @ionChange="onUserSelectionModeChange"
                      >
                        <ion-select-option value="new">Créer un nouvel utilisateur</ion-select-option>
                        <ion-select-option value="existing">Sélectionner un utilisateur existant</ion-select-option>
                      </ion-select>
                    </ion-item>
                  </div>

                  <!-- Sélection d'un utilisateur existant -->
                  <div class="ion-margin-vertical" v-if="mode === 'create' && formData.userSelectionMode === 'existing'">
                    <ion-label for="shop-existing-user" class="field-label ion-margin-start">Utilisateur existant</ion-label>
                    <ion-item>
                      <ion-select
                        id="shop-existing-user"
                        name="selectedUserId"
                        :interface-options="{header: 'Sélectionner un utilisateur'}"
                        v-model="formData.selectedUserId"
                        placeholder="Choisir un utilisateur"
                        @ionChange="onUserSelected"
                      >
                        <ion-select-option 
                          v-for="user in availableUsers" 
                          :key="user.id" 
                          :value="user.id"
                        >
                          {{ user.first_name || '' }} {{ user.last_name || '' }} ({{ user.email || user.username }})
                        </ion-select-option>
                      </ion-select>
                    </ion-item>
                    <ion-text v-if="errors.selectedUserId" class="error" color="danger">
                      * Veuillez sélectionner un utilisateur
                    </ion-text>
                  </div>

                  <!-- Informations d'identification du propriétaire -->
                  <template v-if="mode === 'edit' || (mode === 'create' && formData.userSelectionMode === 'new')">
                    <div class="credentials-group">
                      <ion-label class="group-label">Identifiants de connexion</ion-label>
                      
                      <!-- Nom d'utilisateur -->
                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-input
                            id="shop-username"
                            name="username"
                            label="Nom d'utilisateur (obligatoire)"
                            label-placement="stacked"
                            v-model="formData.username"
                            placeholder="Nom d'utilisateur"
                            required
                            @keydown="initErrors"
                          ></ion-input>
                        </ion-item>
                        <ion-text v-if="errors.username" class="error" color="danger">
                          * Veuillez remplir le nom d'utilisateur
                        </ion-text>
                      </div>

                      <!-- Email -->
                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-input
                            id="shop-email"
                            name="email"
                            label="Email"
                            label-placement="stacked"
                            type="email"
                            v-model="formData.email"
                            placeholder="email@exemple.com"
                            @keydown="initErrors"
                            autocomplete="email"
                          ></ion-input>
                        </ion-item>
                        <ion-text v-if="errors.email" class="error" color="danger">
                          * Veuillez remplir un email valide
                        </ion-text>
                      </div>

                      <!-- Téléphone -->
                      <div class="ion-margin-vertical">
                        <ion-label for="shop-country-code" class="field-label ion-margin-start">Téléphone</ion-label>
                        <div class="phone-container">
                          <div class="phone-inputs-minimal">
                            <select 
                              id="shop-country-code"
                              name="country_code"
                              v-model="formData.country_code" 
                              class="country-code-select-minimal"
                            >
                              <option v-for="c in countryList" :key="c.code" :value="c.prefix">
                                {{ c.name }} ({{ c.prefix }})
                              </option>
                            </select>
                            <ion-input
                              id="shop-phone"
                              name="phone"
                              type="tel"
                              v-model="formData.phone_number_only"
                              placeholder="00000000"
                              @keydown="initErrors"
                              class="phone-main-input"
                              autocomplete="tel-national"
                            ></ion-input>
                          </div>
                        </div>
                        <ion-text v-if="errors.phone_number" class="error" color="danger">
                          * Veuillez remplir le numéro de téléphone
                        </ion-text>
                      </div>

                      <!-- Mot de passe -->
                      <div class="ion-margin-vertical password-field">
                        <ion-item>
                          <ion-input
                            id="shop-password"
                            name="password"
                            :label="mode === 'create' 
                              ? 'Mot de passe (obligatoire - minimum 4 caractères)' 
                              : 'Mot de passe (laisser vide = pas de changement)'"
                            label-placement="stacked"
                            type="text"
                            v-model="formData.password"
                            :placeholder="mode === 'create' 
                              ? 'Entrez le mot de passe (min. 4 car.)' 
                              : 'Laissez vide pour garder l\'actuel'"
                            :required="mode === 'create'"
                            @keydown="initErrors"
                            @input="checkPasswordLength"
                            @focus="handlePasswordFocus"
                            clear-on-edit="false"
                            autocomplete="new-password"
                          ></ion-input>
                        </ion-item>
                        <ion-text v-if="errors.password" class="error" color="danger">
                          * {{ mode === 'create' ? 'Veuillez remplir le mot de passe (min. 4 car.)' : 'Le mot de passe doit contenir au moins 4 caractères' }}
                        </ion-text>
                      </div>
                    </div>

                    <!-- Nom de la boutique (Essentiel) -->
                    <div class="ion-margin-vertical">
                      <ion-item>
                        <ion-input
                          id="shop-name"
                          name="shop-name"
                          label="Nom de la boutique"
                          label-placement="stacked"
                          v-model="formData.name"
                          placeholder="Nom de la boutique"
                          @keydown="initErrors"
                        ></ion-input>
                      </ion-item>
                    </div>

                    <!-- Localisation (Province, Commune, Quartier, Adresse) -->
                    <div class="credentials-group">
                      <ion-label class="group-label">Localisation</ion-label>
                      
                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-input
                            id="shop-province"
                            name="province"
                            label="Province"
                            label-placement="stacked"
                            v-model="formData.province"
                            placeholder="Province"
                          ></ion-input>
                        </ion-item>
                      </div>

                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-input
                            id="shop-commune"
                            name="commune"
                            label="Commune"
                            label-placement="stacked"
                            v-model="formData.commune"
                            placeholder="Commune"
                          ></ion-input>
                        </ion-item>
                      </div>

                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-input
                            id="shop-quarter"
                            name="quarter"
                            label="Quartier"
                            label-placement="stacked"
                            v-model="formData.quarter"
                            placeholder="Quartier"
                          ></ion-input>
                        </ion-item>
                      </div>

                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-input
                            id="shop-address"
                            name="address"
                            label="Adresse précise"
                            label-placement="stacked"
                            v-model="formData.address"
                            placeholder="Rue, numéro, etc."
                          ></ion-input>
                        </ion-item>
                      </div>
                    </div>

                    <!-- Sélection de l'Agent responsable -->
                    <div class="ion-margin-vertical" v-if="!isAgent">
                      <ion-item>
                        <ion-select
                          id="shop-agent"
                          name="agentId"
                          label="Agent responsable"
                          label-placement="stacked"
                          v-model="formData.agentId"
                          placeholder="Sélectionner un agent"
                          interface="action-sheet"
                        >
                          <ion-select-option :value="null">Aucun agent</ion-select-option>
                          <ion-select-option 
                            v-for="user in availableUsers" 
                            :key="user.id" 
                            :value="user.id"
                          >
                            {{ user.first_name || '' }} {{ user.last_name || '' }} ({{ user.username }})
                          </ion-select-option>
                        </ion-select>
                      </ion-item>
                    </div>
                  </template>

                  <!-- Abonnement et Essai Gratuit -->
                  <div class="credentials-group">
                    <ion-label class="group-label">Abonnement &amp; Essai</ion-label>
                    
                    <!-- Plan d'abonnement -->
                    <div class="ion-margin-vertical">
                      <ion-item>
                        <ion-select
                          id="shop-subscription-plan"
                          name="subscription_plan"
                          label="Plan d'abonnement"
                          label-placement="stacked"
                          v-model="formData.subscription_plan"
                          placeholder="Choisir un plan"
                          @ionChange="onSubscriptionPlanChange"
                        >
                          <ion-select-option value="FREE">Essai Gratuit {{ isAgent ? '(3 Mois)' : '' }}</ion-select-option>
                          <template v-if="!isAgent">
                              <ion-select-option value="MONTHLY">Mensuel</ion-select-option>
                              <ion-select-option value="3MONTHS">3 Mois</ion-select-option>
                              <ion-select-option value="6MONTHS">6 Mois</ion-select-option>
                              <ion-select-option value="YEARLY">Annuel</ion-select-option>
                          </template>
                        </ion-select>
                      </ion-item>
                    </div>

                    <!-- Dates (visibles pour tous les plans) -->
                    <div class="ion-margin-vertical">
                      <ion-item>
                        <ion-input
                          id="shop-trial-start"
                          name="trial_start_date"
                          label="Date de début"
                          label-placement="stacked"
                          type="date"
                          v-model="formData.trial_start_date"
                        ></ion-input>
                      </ion-item>
                    </div>

                    <div class="ion-margin-vertical">
                      <ion-item>
                        <ion-input
                          id="shop-trial-end"
                          name="trial_end_date"
                          label="Date de fin"
                          label-placement="stacked"
                          type="date"
                          v-model="formData.trial_end_date"
                        ></ion-input>
                      </ion-item>
                    </div>
                  </div>

                  <!-- État d'activation -->
                  <div class="ion-margin-vertical">
                    <ion-item lines="none">
                      <ion-label for="shop-active">Boutique Active</ion-label>
                      <ion-checkbox
                        id="shop-active"
                        name="is_active"
                        slot="end"
                        v-model="formData.is_active"
                      ></ion-checkbox>
                    </ion-item>
                  </div>

                  <!-- Mode de paiement -->
                  <div class="ion-margin-vertical">
                    <ion-item lines="none">
                      <ion-label for="shop-payment-mode">Mode de paiement actif</ion-label>
                      <ion-checkbox
                        id="shop-payment-mode"
                        name="payment_mode_active"
                        slot="end"
                        v-model="formData.payment_mode_active"
                      ></ion-checkbox>
                    </ion-item>
                  </div>

                  <!-- Bouton de validation -->
                  <ion-button
                    color="primary"
                    expand="block"
                    class="submit-btn ion-margin-top"
                    :disabled="loading"
                    @click="performSubmit"
                  >
                    <ion-spinner v-if="loading" slot="start"></ion-spinner>
                    <ion-text color="light">{{ mode === 'create' ? 'Créer' : 'Modifier' }}</ion-text>
                  </ion-button>
                </form>
              </ion-item-group>
            </ion-list>
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
  IonList,
  IonItemGroup,
  IonItem,
  IonInput,
  IonLabel,
  IonText,
  IonSpinner,
  IonCheckbox,
  IonSelect,
  IonSelectOption,
  modalController
} from '@ionic/vue';

import { close, arrowBackOutline } from 'ionicons/icons';
import { shopsService, usersService, accountsService } from '../../services/api';
import { countries } from '../../services/countries';

/**
 * Composant ShopForm
 * - Gère l'interface et la logique métier de Shop Form.
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
    IonList,
    IonItemGroup,
    IonItem,
    IonInput,
    IonLabel,
    IonText,
    IonSpinner,
    IonCheckbox,
    IonSelect,
    IonSelectOption
  },
  props: {
    mode: {
      type: String,
      default: 'create',
      validator: (value) => ['create', 'edit'].includes(value)
    },
    shop: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      close,
      arrowBackOutline,
      loading: false,
      formData: {
        userSelectionMode: 'new', // 'new' ou 'existing'
        selectedUserId: null,
        username: '',
        email: '',
        phone_number: '',
        first_name: '',
        last_name: '',
        password: '',
        name: '',
        province: '',
        commune: '',
        quarter: '',
        address: '',
        is_active: true,
        country_code: '+257',
        phone_number_only: '',
        subscription_plan: 'FREE',
        trial_start_date: '',
        trial_end_date: '',
        agentId: null,
        payment_mode_active: true
      },
      countryList: countries,
      availableUsers: [],
      errors: {
        selectedUserId: false,
        username: false,
        email: false,
        phone_number: false,
        first_name: false,
        last_name: false,
        password: false,
        name: false
      }
    };
  },
  created() {
    // Charger la liste des utilisateurs disponibles pour la sélection (pour owner et agent)
    this.loadAvailableUsers();

    if (this.mode === 'create') {
      // Par défaut pour une nouvelle boutique
      this.setDefaultTrialDates();
    }

    if (this.mode === 'edit' && this.shop) {
      // Récupérer les données de l'utilisateur propriétaire
      // Avec depth=2 sur le backend, shop.owner est un objet Account avec un objet User
      const owner = this.shop.owner || {};
      const user = owner.user || {};

      this.formData.username = user.username || '';
      this.formData.email = user.email || '';
      this.formData.phone_number = owner.phone_number || '';
      this.formData.first_name = user.first_name || '';
      this.formData.last_name = user.last_name || '';
      // Afficher un indicateur que le mot de passe actuel existe
      this.formData.password = '•••••••• (mot de passe actuel)';

      // Données de la boutique
      this.formData.name = this.shop.name || '';
      this.formData.province = this.shop.province || '';
      this.formData.commune = this.shop.commune || '';
      this.formData.quarter = this.shop.quarter || '';
      this.formData.address = this.shop.address || '';
      this.formData.is_active = this.shop.is_active !== undefined ? this.shop.is_active : true;
      this.formData.payment_mode_active = this.shop.payment_mode_active !== undefined ? this.shop.payment_mode_active : true;
      this.formData.subscription_plan = this.shop.subscription_plan || 'FREE';
      
      // Pré-remplir l'agent si existant
      if (this.shop.agent && this.shop.agent.user) {
        this.formData.agentId = this.shop.agent.user.id;
      }
      
      // Formatage des dates pour l'input type="date" (YYYY-MM-DD)
      if (this.shop.trial_start_date) {
        this.formData.trial_start_date = this.shop.trial_start_date.split('T')[0];
      }
      if (this.shop.trial_end_date) {
        this.formData.trial_end_date = this.shop.trial_end_date.split('T')[0];
      }

      // Découper le numéro de téléphone existant
      const fullPhone = this.formData.phone_number || '';
      if (fullPhone) {
        const sortedCountries = [...this.countryList].sort((a, b) => b.prefix.length - a.prefix.length);
        const match = sortedCountries.find(c => fullPhone.startsWith(c.prefix));
        if (match) {
          this.formData.country_code = match.prefix;
          this.formData.phone_number_only = fullPhone.substring(match.prefix.length).replace(/\D/g, '');
        } else {
          this.formData.phone_number_only = fullPhone.replace(/\D/g, '');
        }
      }
    }
    
    // Définir le contexte d'aide
    this.$store.commit('SET_HELP_CONTEXT', {
      title: this.mode === 'create' ? 'Ajout de Boutique' : 'Modification de Boutique',
      description: "Ce formulaire vous permet de gérer les informations d'une boutique. Vous pouvez associer un propriétaire (nouveau ou existant), définir les détails de la boutique (Nom, Adresse) et choisir un plan d'abonnement.",
      actions: [
        "Créer un nouvel utilisateur propriétaire",
        "Associer à un utilisateur existant",
        "Choisir un plan d'abonnement (Gratuit/Premium)",
        "Définir les périodes d'essai"
      ],
      faqs: [
        { question: "essais", answer: "L'essai gratuit est de 1 mois par défaut, ou 3 mois si créé par un Agent." },
        { question: "mot de passe", answer: "Le mot de passe sert au propriétaire pour se connecter à l'application mobile." },
        { question: "agent", answer: "L'agent responsable reçoit les commissions sur cette boutique." }
      ]
    });
  },
  beforeUnmount() {
    this.$store.commit('SET_HELP_CONTEXT', null);
  },
  computed: {
    isAgent() {
        const user = this.$store.state.user;
        const groups = user?.groups || [];
        // Vérifie si l'utilisateur est un agent (et pas un admin/superuser qui ont tous les droits)
        const isAgent = groups.some(g => (typeof g === 'string' ? g : g.name) === 'agent');
        const isAdmin = groups.some(g => (typeof g === 'string' ? g : g.name) === 'admin' || (typeof g === 'string' ? g : g.name) === 'superuser');
        return isAgent && !isAdmin;
    }
  },
  methods: {
    setDefaultTrialDates(months = 1) {
        // Pour les agents, c'est toujours 3 mois s'ils choisissent FREE
        if (this.isAgent && this.formData.subscription_plan === 'FREE') {
            months = 3;
        } else if (this.formData.subscription_plan === 'FREE') {
             months = 1; // Default for admin if not specified logic
        }

        const now = new Date();
        const nextDate = new Date();
        // Ajouter le nombre de mois
        nextDate.setMonth(now.getMonth() + months);
        
        this.formData.trial_start_date = now.toISOString().split('T')[0];
        this.formData.trial_end_date = nextDate.toISOString().split('T')[0];
    },
    onSubscriptionPlanChange() {
      // Calculer automatiquement les dates en fonction du plan
      let monthsToAdd = 0;
      
      switch (this.formData.subscription_plan) {
        case 'FREE':
        case 'MONTHLY':
          monthsToAdd = 1;
          break;
        case '3MONTHS':
          monthsToAdd = 3;
          break;
        case '6MONTHS':
          monthsToAdd = 6;
          break;
        case 'YEARLY':
          monthsToAdd = 12;
          break;
        default:
          monthsToAdd = 0;
      }

      if (monthsToAdd > 0) {
        this.setDefaultTrialDates(monthsToAdd);
      }
    },
    async loadAvailableUsers() {
      try {
        const response = await usersService.getAllUsers();
        this.availableUsers = response.data.results || response.data || [];
      } catch (err) {
        console.error('Erreur lors du chargement des utilisateurs:', err);
        this.availableUsers = [];
      }
    },
    onUserSelectionModeChange() {
      // Réinitialiser les champs quand on change de mode
      if (this.formData.userSelectionMode === 'existing') {
        this.formData.selectedUserId = null;
        // Vider les champs de création
        this.formData.username = '';
        this.formData.email = '';
        this.formData.phone_number = '';
        this.formData.first_name = '';
        this.formData.last_name = '';
        this.formData.password = '';
      } else {
        this.formData.selectedUserId = null;
      }
      this.initErrors();
    },
    onUserSelected() {
      // Remplir automatiquement les champs avec les données de l'utilisateur sélectionné
      if (this.formData.selectedUserId) {
        const selectedUser = this.availableUsers.find(u => u.id === this.formData.selectedUserId);
        if (selectedUser) {
          this.formData.username = selectedUser.username || '';
          this.formData.email = selectedUser.email || '';
          this.formData.phone_number = selectedUser.phone_number || (selectedUser.account && selectedUser.account.phone_number) || '';
          this.formData.first_name = selectedUser.first_name || '';
          this.formData.last_name = selectedUser.last_name || '';
          // Pas de mot de passe pour un utilisateur existant
          this.formData.password = '';
        }
      }
      this.initErrors();
    },
    initErrors() {
      this.errors.selectedUserId = false;
      this.errors.username = false;
      this.errors.email = false;
      this.errors.phone_number = false;
      this.errors.first_name = false;
      this.errors.last_name = false;
      this.errors.password = false;
      this.errors.name = false;
    },
    checkPasswordLength() {
      // Réinitialiser l'erreur de mot de passe lors de la saisie
      if (this.formData.password && this.formData.password.length >= 4) {
        this.errors.password = false;
      }
    },
    handlePasswordFocus() {
      // En mode édition, si le champ contient l'indicateur du mot de passe actuel, le vider pour permettre la saisie
      if (this.mode === 'edit' && this.formData.password === '•••••••• (mot de passe actuel)') {
        this.formData.password = '';
      }
    },
    validateForm() {
      this.initErrors();
      let isValid = true;

      // Si on est en mode création et qu'on sélectionne un utilisateur existant
      if (this.mode === 'create' && this.formData.userSelectionMode === 'existing') {
        if (!this.formData.selectedUserId) {
          this.errors.selectedUserId = true;
          isValid = false;
        }
      } else {
        // Validation des champs utilisateur
        // Seul le nom d'utilisateur est obligatoire
        if (!this.formData.username || this.formData.username.trim() === '') {
          this.errors.username = true;
          isValid = false;
        }

        // Email : optionnel, mais si rempli, doit contenir @
        if (this.formData.email && this.formData.email.trim() !== '' && !this.formData.email.includes('@')) {
          this.errors.email = true;
          isValid = false;
        }

        // Validation du mot de passe : requis en création d'un nouvel utilisateur
        if (this.mode === 'create' && this.formData.userSelectionMode === 'new') {
          if (!this.formData.password || this.formData.password.length < 4) {
            this.errors.password = true;
            isValid = false;
          }
        } else if (this.mode === 'edit') {
          if (this.formData.password && 
              this.formData.password !== '•••••••• (mot de passe actuel)' && 
              this.formData.password.length > 0 && 
              this.formData.password.length < 4) {
            this.errors.password = true;
            isValid = false;
          }
        }
      }

      return isValid;
    },
    async performSubmit() {
      this.blurActiveElement();
      // Validation stricte avant de continuer
      if (!this.validateForm()) {
        // Afficher un message d'erreur spécifique pour chaque champ manquant
        const missingFields = [];
        if (this.mode === 'create' && this.formData.userSelectionMode === 'existing') {
          if (!this.formData.selectedUserId) {
            missingFields.push('un utilisateur');
          }
        } else {
          if (!this.formData.username || this.formData.username.trim() === '') {
            missingFields.push('le nom d\'utilisateur');
          }
          if (!this.formData.email || this.formData.email.trim() === '' || !this.formData.email.includes('@')) {
            missingFields.push('l\'email');
          }
          if (!this.formData.phone_number_only || this.formData.phone_number_only.trim() === '') {
            missingFields.push('le téléphone');
          }
          if (this.mode === 'create' && this.formData.userSelectionMode === 'new') {
            if (!this.formData.password || this.formData.password.length < 4) {
              missingFields.push('le mot de passe (minimum 4 caractères)');
            }
          }
        }
        if (!this.formData.name || this.formData.name.trim() === '') {
          missingFields.push('le nom de la boutique');
        }

        const message = missingFields.length > 0 
          ? `Veuillez remplir : ${missingFields.join(', ')}.`
          : 'Veuillez remplir tous les champs requis.';
        this.showTostMsg(message, 'danger', 4000);
        return;
      }

      this.loading = true;

      try {
        let accountId = null;

        if (this.mode === 'create') {
          if (this.formData.userSelectionMode === 'existing' && this.formData.selectedUserId) {
            // Utiliser un utilisateur existant
            const selectedUser = this.availableUsers.find(u => u.id === this.formData.selectedUserId);
            if (!selectedUser) {
              throw new Error('Utilisateur sélectionné introuvable');
            }

            // Récupérer l'account de l'utilisateur sélectionné
            const userDetails = await usersService.getUser(selectedUser.id);
            if (userDetails.data.account && userDetails.data.account.id) {
              accountId = userDetails.data.account.id;
            } else {
              // Si l'account n'est pas dans la réponse, chercher dans la liste des accounts
              const accountsResponse = await accountsService.getAllAccounts();
              const accounts = accountsResponse.data.results || accountsResponse.data || [];
              const account = accounts.find(acc => acc.user === selectedUser.id || acc.user?.id === selectedUser.id);
              if (account) {
                accountId = account.id;
              }
            }

            if (!accountId) {
              throw new Error('Impossible de récupérer le compte de l\'utilisateur sélectionné');
            }
          } else {
            // Créer un nouvel utilisateur et son compte
            const userPayload = {
              username: this.formData.username,
              password: this.formData.password,
              role: 'user'
            };

            // Email : envoyer seulement si rempli, sinon générer un placeholder
            const emailVal = (this.formData.email || '').trim();
            userPayload.email = emailVal || `${this.formData.username}@placeholder.local`;

            // Téléphone : envoyer seulement si rempli
            const phoneDigits = (this.formData.phone_number_only || '').replace(/\D/g, '');
            if (phoneDigits) {
              userPayload.phone_number = (this.formData.country_code || '+257') + phoneDigits;
            }

            const userResponse = await usersService.createUser(userPayload);
            const createdUser = userResponse.data;

            // Récupérer l'account associé à l'utilisateur créé
            // Le backend crée automatiquement un Account lors de la création d'un User
            // On doit récupérer l'utilisateur pour obtenir l'account
            const userDetails = await usersService.getUser(createdUser.id);
            if (userDetails.data.account && userDetails.data.account.id) {
              accountId = userDetails.data.account.id;
            } else {
              // Si l'account n'est pas dans la réponse, chercher dans la liste des accounts
              const accountsResponse = await accountsService.getAllAccounts();
              const accounts = accountsResponse.data.results || accountsResponse.data || [];
              const account = accounts.find(acc => acc.user === createdUser.id || acc.user?.id === createdUser.id);
              if (account) {
                accountId = account.id;
              }
            }

            if (!accountId) {
              throw new Error('Impossible de récupérer le compte créé pour l\'utilisateur');
            }
          }
        } else {
          // Mode édition : mettre à jour l'utilisateur existant
          if (this.shop.owner && this.shop.owner.user) {
            const userId = this.shop.owner.user.id;
            const updatePayload = {
              username: this.formData.username,
            };

            // Email : envoyer seulement si rempli
            const emailVal = (this.formData.email || '').trim();
            if (emailVal) {
              updatePayload.email = emailVal;
            }

            // Téléphone : envoyer seulement si rempli
            const phoneDigits = (this.formData.phone_number_only || '').replace(/\D/g, '');
            if (phoneDigits) {
              updatePayload.phone_number = (this.formData.country_code || '+257') + phoneDigits;
            }

            // Ajouter le mot de passe seulement s'il a été modifié
            const passwordValue = (this.formData.password || '').trim();
            const isPasswordChanged = passwordValue && 
                                      passwordValue !== '•••••••• (mot de passe actuel)' && 
                                      passwordValue.length >= 4;
            
            if (isPasswordChanged) {
              updatePayload.password = passwordValue;
            }

            await usersService.updateUser(userId, updatePayload);
            accountId = this.shop.owner.id;
          } else {
            throw new Error('Impossible de trouver le propriétaire de la boutique');
          }
        }

        // Créer ou mettre à jour la boutique
        const shopPayload = {
          name: (this.formData.name || '').trim() || `Boutique de ${this.formData.username}`,
          province: this.formData.province || null,
          commune: this.formData.commune || null,
          quarter: this.formData.quarter || null,
          address: this.formData.address || null,
          is_active: !!this.formData.is_active,
          owner: accountId,
          subscription_plan: this.formData.subscription_plan,
          trial_start_date: this.formData.trial_start_date ? this.formData.trial_start_date : null,
          trial_end_date: this.formData.trial_end_date ? this.formData.trial_end_date : null,
        };

        // Gérer l'agent
        if (this.formData.agentId) {
            // Trouver l'account ID de l'agent
            // On essaie de le trouver dans la liste des utilisateurs chargés si possible, ou on fait un appel
            let agentAccountId = null;
            
            // Note: availableUsers contient des objets User, pas forcement l'Account ID direct
            // On doit récupérer l'account ID
             try {
                const agentUserDetails = await usersService.getUser(this.formData.agentId);
                if (agentUserDetails.data.account && agentUserDetails.data.account.id) {
                    agentAccountId = agentUserDetails.data.account.id;
                } else {
                     // Fallback: chercher dans tous les comptes (couteux mais sûr)
                    const accountsResponse = await accountsService.getAllAccounts();
                    const accounts = accountsResponse.data.results || accountsResponse.data || [];
                    const account = accounts.find(acc => acc.user === this.formData.agentId || acc.user?.id === this.formData.agentId);
                    if (account) {
                        agentAccountId = account.id;
                    }
                }
             } catch (e) {
                 console.error("Erreur récupération compte agent", e);
             }

             if (agentAccountId) {
                 shopPayload.agent = agentAccountId;
             }
        } else {
        }

        // Si c'est un agent, on force l'assignation à lui-même s'il crée la boutique
        if (this.isAgent) {
             const currentUser = this.$store.state.user;
             let agentAccId = null;

             // 1. Chercher dans le store
             if (currentUser.account && currentUser.account.id) {
                 agentAccId = currentUser.account.id;
             }

             // 2. Fallback : récupérer via l'API users
             if (!agentAccId) {
                 try {
                   const meDetails = await usersService.getUser(currentUser.id);
                   if (meDetails.data.account && meDetails.data.account.id) {
                     agentAccId = meDetails.data.account.id;
                     // Persister dans le store pour les prochains appels
                     this.$store.state.user.account = meDetails.data.account;
                     localStorage.setItem('user', JSON.stringify(this.$store.state.user));
                   }
                 } catch (e) {
                   console.error("Erreur récupération Account agent courant", e);
                 }
             }

             // 3. Dernier fallback : chercher parmi tous les comptes
             if (!agentAccId) {
                 try {
                   const accountsResponse = await accountsService.getAllAccounts();
                   const accounts = accountsResponse.data.results || accountsResponse.data || [];
                   const found = accounts.find(acc => acc.user === currentUser.id || acc.user?.id === currentUser.id);
                   if (found) {
                     agentAccId = found.id;
                   }
                 } catch (e) {
                   console.error("Erreur fallback accounts", e);
                 }
             }

             if (agentAccId) {
                 shopPayload.agent = agentAccId;
             } else {
                 console.warn("Agent Account ID introuvable, la boutique sera créée sans agent assigné");
             }
        }

        if (this.mode === 'create') {
          await shopsService.createShop(shopPayload);
          this.showTostMsg('Boutique et utilisateur créés avec succès !', 'success', 3000);
        } else {
          await shopsService.updateShop(this.shop.id, shopPayload);
          this.showTostMsg('Boutique et utilisateur modifiés avec succès !', 'success', 3000);
        }

        modalController.dismiss(null, 'confirm');
      } catch (err) {
        // Intercepter l'erreur de nom d'utilisateur déjà pris (500 ou 400 selon le backend)
        const errorData = err.response?.data || {};
        const errorMsg = (errorData.detail || errorData.message || JSON.stringify(errorData)).toLowerCase();
        
        if (errorMsg.includes('unique constraint') && errorMsg.includes('auth_user.username')) {
          this.showTostMsg('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.', 'danger', 5000);
        } else {
          this.errorOrRefresh(err, () => this.performSubmit());
        }
      } finally {
        this.loading = false;
      }
    },
    performClose() {
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

ion-content {
  ion-list {
    ion-item {
      height: auto;
      min-height: 70px; /* Responsive fix */
    }
  }
}

.credentials-group {
  width: 100%;
  border: 1px solid #eee;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.group-label {
  font-weight: bold;
  font-size: 0.9rem;
  color: var(--ion-color-primary);
  display: block;
  margin-bottom: 10px;
}

.field-label {
  display: block;
  font-size: 0.85rem;
  color: var(--ion-color-medium);
  margin-bottom: 4px;
}

.phone-container {
  padding: 0 16px;
  margin-bottom: 8px;
}

.phone-inputs-minimal {
  display: flex;
  align-items: center;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  min-height: 70px; /* Responsive fix */
}

.country-code-select-minimal {
  background: #e0e0e0;
  border: none;
  padding: 0 5px 0 10px;
  font-size: 14px;
  font-weight: bold;
  height: 100%;
  outline: none;
  max-width: 150px;
  border-right: 1px solid #ccc;
}

.phone-main-input {
  --padding-start: 12px;
  font-size: 16px;
}

.error {
  font-size: 0.75em !important;
  margin-left: 1rem;
  display: block;
}

ion-button {
  margin-top: 1rem;
}

.password-field {
  display: block !important;
  visibility: visible !important;
}

.password-field ion-item {
  display: block !important;
  visibility: visible !important;
}

.password-hint, .password-info, .password-warning, .password-success {
  font-size: 0.75rem !important;
  margin-left: 1rem;
  margin-top: 0.5rem;
  display: block;
  opacity: 0.9;
  line-height: 1.4;
}

.password-warning {
  color: var(--ion-color-warning);
}
</style>
