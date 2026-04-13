<!--
  * @file UserForm.vue
  * @description Page pour la gestion de User Form.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="user-form-back-btn" name="back-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>{{ mode === 'create' ? 'Ajouter un agent' : 'Modifier l\'agent' }}</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button id="user-form-close-btn" name="close-button" @click="performClose">
            <ion-icon color="light" size="large" :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-grid fixed>
        <ion-row class="ion-justify-content-center">
          <ion-col size="12">
            <div class="form-container">
              <ion-list lines="full">
                <ion-item-group>
                  <form>
                    <!-- Mode création ou édition : tous les champs -->
                    <template v-if="mode === 'create' || mode === 'edit'">
                      <!-- Username -->
                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-input
                            id="user-username"
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
                            id="user-email"
                            name="email"
                            label="Email"
                            label-placement="stacked"
                            type="email"
                            v-model="formData.email"
                            placeholder="email@example.com"
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
                        <ion-label for="user-country-code" class="field-label ion-margin-start">Téléphone</ion-label>
                        <div class="phone-container">
                          <div class="phone-inputs">
                            <select 
                              id="user-country-code"
                              name="country_code"
                              v-model="formData.country_code" 
                              class="country-code-select-minimal"
                            >
                              <option v-for="c in countryList" :key="c.code" :value="c.prefix">
                                {{ c.name }} ({{ c.prefix }})
                              </option>
                            </select>
                            <ion-input
                              id="user-phone"
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

                    </template>

                    <!-- Mot de passe (création + édition) -->
                    <div class="ion-margin-vertical password-field">
                      <ion-item>
                        <ion-input
                          id="user-password"
                          name="password"
                          :label="mode === 'create' 
                            ? 'Mot de passe (obligatoire - minimum 4 caractères)' 
                            : 'Nouveau mot de passe (laisser vide = ne pas changer)'"
                          label-placement="stacked"
                          type="text"
                          v-model="formData.password"
                          :placeholder="mode === 'create' 
                            ? 'Entrez le mot de passe (minimum 4 caractères requis)' 
                            : 'Entrez le nouveau mot de passe (minimum 4 caractères)'"
                          :required="mode === 'create'"
                          :minlength="mode === 'create' ? 4 : undefined"
                          @keydown="initErrors"
                          @input="checkPasswordLength"
                          @focus="handlePasswordFocus"
                          clear-on-edit="false"
                          autocomplete="new-password"
                        ></ion-input>
                      </ion-item>
                      <ion-text v-if="mode === 'create'" class="password-hint" color="primary">
                        ⚠️ <span class="font-bold">Exigences du mot de passe :</span> Le mot de passe doit contenir au minimum 4 caractères. 
                      </ion-text>
                      <ion-text v-if="errors.password" class="error" color="danger">
                        * {{ mode === 'create' ? 'Veuillez remplir le mot de passe (minimum 4 caractères)' : 'Le mot de passe doit contenir au moins 4 caractères' }}
                      </ion-text>
                    </div>

                    <!-- Rôle/Groupe + droits (création + édition) -->
                    <template v-if="mode === 'create' || mode === 'edit'">
                      <!-- Rôle/Groupe -->
                      <div class="ion-margin-vertical">
                        <ion-label for="user-role" class="field-label ion-margin-start">Rôle / Rang</ion-label>
                        <ion-item>
                          <ion-select
                            id="user-role"
                            name="role"
                            v-model="formData.role"
                            placeholder="Sélectionner le rang"
                            @ionChange="onRoleChange"
                          >
                            <ion-select-option value="user">Utilisateur normal</ion-select-option>
                            <ion-select-option value="agent">Agent</ion-select-option>
                            <ion-select-option value="admin">Administrateur</ion-select-option>
                          </ion-select>
                        </ion-item>
                      </div>

                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-checkbox id="user-is-staff" name="is_staff" v-model="formData.is_staff"></ion-checkbox>
                          <ion-label for="user-is-staff">Accès à l'administration</ion-label>
                        </ion-item>
                      </div>

                      <div class="ion-margin-vertical">
                        <ion-item>
                          <ion-checkbox id="user-is-superuser" name="is_superuser" v-model="formData.is_superuser" :disabled="formData.role !== 'admin'"></ion-checkbox>
                          <ion-label for="user-is-superuser">Superutilisateur</ion-label>
                        </ion-item>
                      </div>
                    </template>

                    <ion-button
                      color="primary"
                      expand="block"
                      class="submit-btn"
                      :disabled="loading"
                      @click="performSubmit"
                    >
                      <ion-spinner v-if="loading" slot="start"></ion-spinner>
                      <ion-text color="light">{{ mode === 'create' ? 'Créer' : 'Enregistrer' }}</ion-text>
                    </ion-button>
                  </form>
                </ion-item-group>
              </ion-list>
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

import {
  close,
  arrowBackOutline
} from 'ionicons/icons';

import { usersService, accountsService } from '../../services/api';
import { authService } from '../../services/api';
import { countries } from '../../services/countries';

/**
 * Composant UserForm
 * - Gère l'interface et la logique métier de User Form.
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
    user: {
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
        username: '',
        email: '',
        phone_number: '',
        password: '',
        role: 'agent', // 'user', 'agent', 'admin' - par défaut 'agent' pour la gestion des agents
        is_staff: false,
        is_superuser: false,
        country_code: '+257',
        phone_number_only: ''
      },
      countryList: countries,
      errors: {
        username: false,
        email: false,
        phone_number: false,
        password: false
      }
    };
  },
  created() {
    if (this.mode === 'edit' && this.user) {
      this.formData.username = this.user.username || '';
      this.formData.email = this.user.email || '';
      this.formData.phone_number = this.user.phone_number || (this.user.account && this.user.account.phone_number) || '';
      // Afficher un indicateur que le mot de passe actuel existe (on ne peut pas l'afficher car il est hashé)
      this.formData.password = '******** (mot de passe actuel)'; // Indicateur visuel du mot de passe actuel
      this.formData.is_staff = this.user.is_staff || false;
      this.formData.is_superuser = this.user.is_superuser || false;
      
      // Déterminer le rôle basé sur les groupes ou les flags
      if (this.user.is_superuser) {
        this.formData.role = 'admin';
      } else if (this.user.groups && Array.isArray(this.user.groups)) {
        if (this.user.groups.includes('agent')) {
          this.formData.role = 'agent';
        } else if (this.user.groups.includes('admin')) {
          this.formData.role = 'admin';
        } else {
          this.formData.role = 'user';
        }
      } else {
        this.formData.role = this.user.is_staff ? 'agent' : 'user';
      }

      // Gérer le découpage du numéro de téléphone s'il existe
      const fullPhone = this.formData.phone_number || '';
      if (fullPhone) {
        // Chercher quel code pays correspond
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
  },
  methods: {
    onRoleChange() {
      // Ajuster automatiquement is_staff et is_superuser selon le rôle
      if (this.formData.role === 'admin') {
        this.formData.is_staff = true;
        this.formData.is_superuser = true;
      } else if (this.formData.role === 'agent') {
        this.formData.is_staff = true;
        this.formData.is_superuser = false;
      } else {
        this.formData.is_staff = false;
        this.formData.is_superuser = false;
      }
    },
    initErrors() {
      this.errors.username = false;
      this.errors.email = false;
      this.errors.phone_number = false;
      this.errors.password = false;
    },
    checkPasswordLength() {
      // Réinitialiser l'erreur de mot de passe lors de la saisie
      if (this.formData.password && this.formData.password.length >= 4) {
        this.errors.password = false;
      }
    },
    handlePasswordFocus() {
      // En mode édition, si le champ contient l'indicateur du mot de passe actuel, le vider pour permettre la saisie
      if (this.mode === 'edit' && this.formData.password === '******** (mot de passe actuel)') {
        this.formData.password = '';
      }
    },
    validateForm() {
      this.initErrors();
      let isValid = true;

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

      // Mot de passe obligatoire en création, optionnel en édition (min 4 car. si fourni)
      if (this.mode === 'create') {
        if (!this.formData.password || this.formData.password.length < 4) {
          this.errors.password = true;
          isValid = false;
        }
      } else {
        if (this.formData.password && this.formData.password.length > 0 && this.formData.password !== '******** (mot de passe actuel)' && this.formData.password.length < 4) {
          this.errors.password = true;
          isValid = false;
        }
      }

      return isValid;
    },
    async performSubmit() {
      // Validation stricte avant de continuer
      if (!this.validateForm()) {
        const missingFields = [];
        if (!this.formData.username || this.formData.username.trim() === '') missingFields.push('le nom d\'utilisateur');
        
        if (this.mode === 'create') {
          if (!this.formData.password || this.formData.password.length < 4) missingFields.push('le mot de passe (minimum 4 caractères)');
        } else {
            if (this.formData.password && this.formData.password !== '******** (mot de passe actuel)' && this.formData.password.length < 4) {
                missingFields.push('le mot de passe (minimum 4 caractères)');
            }
        }

        const message = missingFields.length > 0 
          ? `Veuillez remplir correctement : ${missingFields.join(', ')}.`
          : 'Veuillez remplir tous les champs requis.';
        this.showTostMsg(message, 'danger', 4000);
        return;
      }

      this.loading = true;

      try {
        const payload = {
            username: this.formData.username,
            is_staff: this.formData.is_staff,
            is_superuser: this.formData.is_superuser,
            role: this.formData.role
          };
        
        // Inclure email et téléphone seulement s'ils sont remplis
        if (this.formData.email && this.formData.email.trim() !== '') {
          payload.email = this.formData.email;
        }
        const digits = (this.formData.phone_number_only || '').replace(/\D/g, '');
        if (digits) {
          const prefix = this.formData.country_code || '+257';
          payload.phone_number = prefix + digits;
        }

        if (this.mode === 'create') {
          payload.password = this.formData.password;
          await usersService.createUser(payload);
          this.showTostMsg('Agent créé avec succès !', 'success', 3000);
        } else {
          // En mode édition
          const passwordValue = (this.formData.password || '').trim();
          if (passwordValue && passwordValue !== '******** (mot de passe actuel)' && passwordValue.length >= 4) {
            payload.password = passwordValue;
          }
          
          await usersService.updateUser(this.user.id, payload);
          this.showTostMsg('Informations de l’agent modifiées avec succès.', 'success', 3000);
          
          if (payload.password) {
            alert(`Nouveau mot de passe pour l'agent "${this.formData.username}" :\n\n${payload.password}\n\nNotez-le et transmettez-le manuellement à l’agent.`);
          }
        }

        modalController.dismiss(null, 'confirm');
      } catch (err) {
        this.errorOrRefresh(err, () => this.performSubmit());
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
  }
  ion-buttons[slot="start"] ion-button.back-arrow-white,
  ion-buttons[slot="start"] ion-button.back-arrow-white  ion-icon{
  font-size:24px;
  color: var(--ion-color-primary);
  }
}

.phone-container {
  padding: 0 16px;
  margin-bottom: 8px;
}

.phone-inputs {
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

  .field-label {
    display: block;
    font-size: 0.85rem;
    color: var(--ion-color-medium);
    margin-bottom: 4px;
  }

  ion-content {
    ion-list {
      ion-item {
        height: auto;
        min-height: 70px; /* Responsive fix */
      }
    }
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

  .password-hint {
    font-size: 0.75rem !important;
    margin-left: 1rem;
    margin-top: 0.5rem;
    display: block;
    opacity: 0.9;
    line-height: 1.4;
  }

  .password-warning {
    font-size: 0.75rem !important;
    margin-left: 1rem;
    margin-top: 0.5rem;
    display: block;
    font-weight: 500;
  }

  .password-success {
    font-size: 0.75rem !important;
    margin-left: 1rem;
    margin-top: 0.5rem;
    display: block;
    font-weight: 500;
  }

  .password-info {
    font-size: 0.75rem !important;
    margin-left: 1rem;
    margin-top: 0.5rem;
    display: block;
    font-weight: 500;
    opacity: 0.9;
  }

  .font-bold {
    font-weight: bold;
  }
</style>
