<!--
  * @file ProfilPage.vue
  * @description Page/Composant pour Profil Page.
  * @author Kora Agency
-->
<template>
    <ion-page>
      <ion-header class="ion-no-border">
        <ion-toolbar color="secondary">
          <ion-title color="light">
            <div class="header-title-container">
              <span>Paramètres / Profil</span>
            </div>
          </ion-title>
          <ion-buttons slot="end">
            <ion-button @click="performClose">
              <ion-icon color="light" size="large" :icon="close"></ion-icon>
            </ion-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
  
      <ion-content >
  
        <ion-footer class="ion-no-border">
            <ion-row>
                <ion-list lines="full">
                <ion-item-group class="ion-margin-horizontal ion-margin-bottom">
                    <form >
                    <div class="ion-margin-vertical">
                        <ion-item>
                            <ion-input 
                                id="profile-username"
                                name="username"
                                label-placement="stacked"
                                v-model="user.username"
                                label="Nom d'utilisateur"
                                type="text"
                                autocomplete="username">
                            </ion-input>
                        </ion-item>
                    </div>
                    <div class="ion-margin-vertical">
                        <ion-item>
                            <ion-input 
                                id="profile-email"
                                name="email"
                                disabled
                                label-placement="stacked"
                                v-model="user.email"
                                label="Email (non modifiable)"
                                type="email"
                                autocomplete="email">
                            </ion-input>
                        </ion-item>
                    </div>
                    <!-- Téléphone -->
                    <div class="ion-margin-vertical">
                        <ion-label class="field-label ion-margin-start" color="medium">Téléphone (obligatoire)</ion-label>
                        <div class="phone-container">
                        <div class="phone-inputs-profile">
                            <select 
                            id="profile-country-code"
                            name="country_code"
                            v-model="user.country_code" 
                            class="country-code-select-minimal"
                            >
                            <option v-for="c in countryList" :key="c.code" :value="c.prefix">
                                {{ c.name }} ({{ c.prefix }})
                            </option>
                            </select>
                            <ion-input
                            id="profile-phone"
                            name="phone"
                            type="tel"
                            v-model="user.phone_number_only"
                            placeholder="00000000"
                            required
                            class="phone-main-input"
                            autocomplete="tel-national"
                            ></ion-input>
                        </div>
                        </div>
                    </div>
                    <div class="ion-margin-vertical password-field">
                        <ion-item>
                            <ion-input 
                                label-placement="stacked"
                                v-model="user.password"
                                label="Mot de passe (laisser vide = pas de changement, ou entrer nouveau mot de passe)"
                                type="text"
                                placeholder="Laissez vide pour garder le même mot de passe, ou entrez un nouveau mot de passe">
                            </ion-input>
                        </ion-item>
                        <ion-text class="password-hint" color="medium">
                            💡 Le mot de passe actuel ne peut pas être affiché (sécurité). Laissez vide pour ne pas le changer, ou entrez un nouveau mot de passe (minimum 4 caractères).
                        </ion-text>
                        <ion-button
                            fill="clear"
                            color="primary"
                            expand="block"
                            @click="requestPasswordReset"
                            class="reset-password-btn"
                        >
                            <ion-icon slot="start" :icon="mailOutline"></ion-icon>
                            Demander une réinitialisation par email
                        </ion-button>
                    </div>
                    <ion-button
                        color="secondary"
                        expand="block"
                        :disabled="loading"
                        @click="updateProfil"
                    >
                        <ion-spinner v-if="loading" slot="start"></ion-spinner>
                        <ion-text color="light" >Valider</ion-text>
                    </ion-button>
                    </form>
                </ion-item-group>
                </ion-list>
            </ion-row>

            </ion-footer>
      </ion-content>
  
    </ion-page>
  </template>
  
  <script>
  import {
    IonButton,
    IonButtons,
    IonContent,
    IonFooter,
    IonHeader,
    IonIcon,
    IonInput,
    IonLabel,
    IonItem,
    IonItemGroup,
    IonList,
    IonPage,
    IonRow,
    IonSpinner,
    IonText,
    IonTitle,
    IonToolbar,
    modalController,
    alertController
} from '@ionic/vue';

  import {
    close,
    mailOutline
  } from 'ionicons/icons'
  import { usersService, authService } from '../services/api'
  import { countries } from '../services/countries';
  
  /**
 * Composant ProfilPage
 * - Gère l'interface et la logique métier.
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
        IonFooter,
        IonRow,
        IonList,
        IonItem,
        IonItemGroup,
        IonInput,
        IonLabel,
        IonButton,
        IonText,
        IonSpinner
    },
    data() {
      return {
        user:{
            username: "",
            email:null,
            password:"",
            country_code: "+257",
            phone_number_only: ""
        },
        countryList: countries,
        loading:false,
        resettingPassword: false,
        close,
        mailOutline
      };
    },
    created(){
        const u = this.$store.state.user;
        this.user.username = u.username || '';
        this.user.email = u.email || u.username;
        
        // Gérer le numéro de téléphone existant
        const fullPhone = u.phone_number || (u.account && u.account.phone_number) || '';
        if (fullPhone) {
            const sortedCountries = [...this.countryList].sort((a, b) => b.prefix.length - a.prefix.length);
            const match = sortedCountries.find(c => fullPhone.startsWith(c.prefix));
            if (match) {
                this.user.country_code = match.prefix;
                this.user.phone_number_only = fullPhone.substring(match.prefix.length).replace(/\D/g, '');
            } else {
                this.user.phone_number_only = fullPhone.replace(/\D/g, '');
            }
        }
    },
    methods: {
        performClose() {
          return modalController.dismiss(null, 'cancel');
        },
        updateProfil(){
            if (!this.user.username || this.user.username.trim() === '') {
                this.showTostMsg('Veuillez remplir le nom d\'utilisateur.', 'danger', 3000);
                return;
            }
            if (!this.user.phone_number_only || this.user.phone_number_only.trim() === '') {
                this.showTostMsg('Veuillez remplir le numéro de téléphone.', 'danger', 3000);
                return;
            }

            this.loading=true
            const updatePayload = {
                username: this.user.username,
                phone_number: this.user.country_code + this.user.phone_number_only.replace(/\D/g, '')
            };
            // Ajouter le mot de passe seulement s'il a été fourni
            if (this.user.password && this.user.password.length >= 4) {
                updatePayload.password = this.user.password;
            } else if (this.user.password && this.user.password.length > 0 && this.user.password.length < 4) {
                this.showTostMsg('Le mot de passe doit contenir au moins 4 caractères.', 'danger', 3000);
                this.loading=false;
                return;
            }
            
            usersService.updateUser(this.$store.state.user.id, updatePayload)
            .then((res)=>{
                // Mettre à jour le store global
                this.$store.state.user.username = this.user.username;
                this.$store.state.user.phone_number = updatePayload.phone_number;
                if (this.$store.state.user.account) {
                    this.$store.state.user.account.phone_number = updatePayload.phone_number;
                }
                
                this.loading = false;
                if (updatePayload.password) {
                    this.showTostMsg('Profil et mot de passe modifiés avec succès !', 'success', 3000);
                } else {
                    this.showTostMsg('Profil modifié avec succès !', 'success', 3000);
                }
                // Fermer le modal et indiquer le succès
                modalController.dismiss(null, "confirm");
            }).catch((err)=>{
                this.loading=false
                this.errorOrRefresh(err, () => this.updateProfil())
            }) 
        },
        async requestPasswordReset() {
            const alert = await alertController.create({
                header: 'Réinitialisation du mot de passe',
                message: `Un nouveau mot de passe sera généré et envoyé à votre adresse email : ${this.user.email}`,
                buttons: [
                    {
                        text: 'Annuler',
                        role: 'cancel'
                    },
                    {
                        text: 'Confirmer',
                        handler: () => {
                            this.performPasswordReset();
                        }
                    }
                ]
            });
            await alert.present();
        },
        performPasswordReset() {
            if (!this.user.email) {
                this.showTostMsg('Email non disponible. Impossible de réinitialiser le mot de passe.', 'danger', 4000);
                return;
            }
            
            this.resettingPassword = true;
            authService.resetPassword(this.user.email)
                .then((res) => {
                    this.resettingPassword = false;
                    this.showTostMsg('Un nouveau mot de passe a été envoyé à votre adresse email. Vérifiez votre boîte de réception.', 'success', 7000);
                })
                .catch((err) => {
                    this.resettingPassword = false;
                    if (err.response && err.response.status === 403) {
                        this.showTostMsg('Email incorrect ou compte non trouvé.', 'danger', 5000);
                    } else {
                        this.errorOrRefresh(err, () => this.performPasswordReset());
                    }
                });
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
  }
  
  ion-content {
      ion-list {
          ion-item{
            min-height: 70px; /* Responsive fix */
          }
      }
  }

  ion-footer {
    ion-row {
        background: transparent;
        display: block;
        ion-fab-button {
            margin-right: 2.5vh;
        }
        ion-list {
            border-radius: 20px 20px 0 0;
            ion-list-header {
                ion-label {
                    font-weight: bold;
                    font-size: 1.8em;
                }
            }
            ion-input, ion-text {
                font-size: 1em;
            }
        
            ion-button{
              height: 2.5em;
              ion-text{
                font-size: 1.3em;
                font-weight: bold;
              }
              ion-spinner{
                margin-right: 0.9em;
              }
            }
            
            .error {
                font-size: 0.75em !important;
            }
        }
    }
}

.password-field {
  display: block !important;
  visibility: visible !important;
}

.field-label {
  display: block;
  font-size: 0.85rem;
  margin-bottom: 4px;
}

.phone-container {
  padding: 0 16px;
  margin-bottom: 8px;
}

.phone-inputs-profile {
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

.password-field ion-item {
  display: block !important;
  visibility: visible !important;
}

.password-hint {
  font-size: 0.75rem !important;
  margin-left: 1rem;
  margin-top: 0.5rem;
  display: block;
  opacity: 0.8;
}

.reset-password-btn {
  margin-top: 0.5rem;
  font-size: 0.85rem;
}
  ion-buttons {
    margin-right: 2em;
      ion-icon{
      font-size:24px;
      color: var(--ion-color-primary);
      }
  }
   
  </style>
  