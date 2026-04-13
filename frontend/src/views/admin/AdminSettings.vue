<!--
  * @file AdminSettings.vue
  * @description Page/Composant pour Admin Settings.
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
            <span>Paramètres</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>
  
    <ion-content>
      <ion-list class="ion-margin">
        <ion-list-header>
          <ion-label>Paramètres de l'application</ion-label>
        </ion-list-header>

        <!-- Section Général -->
        <ion-item-group>
          <ion-item-divider>
            <ion-label>Général</ion-label>
          </ion-item-divider>

          <ion-item>
            <ion-icon slot="start" :icon="informationCircleOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>Version de l'application</h2>
              <p>1.0.0</p>
            </ion-label>
          </ion-item>

          <ion-item>
            <ion-icon slot="start" :icon="serverOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>Serveur API</h2>
              <p>{{ apiUrl }}</p>
            </ion-label>
          </ion-item>
        </ion-item-group>

        <!-- Section Compte -->
        <ion-item-group>
          <ion-item-divider>
            <ion-label>Compte</ion-label>
          </ion-item-divider>

          <ion-item button @click="viewProfile">
            <ion-icon slot="start" :icon="personOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>Mon profil</h2>
              <p>Voir et modifier mes informations</p>
            </ion-label>
            <ion-icon slot="end" :icon="chevronForwardOutline"></ion-icon>
          </ion-item>

          <ion-item button @click="changePassword">
            <ion-icon slot="start" :icon="lockClosedOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>Changer le mot de passe</h2>
              <p>Modifier mon mot de passe</p>
            </ion-label>
            <ion-icon slot="end" :icon="chevronForwardOutline"></ion-icon>
          </ion-item>
        </ion-item-group>

        <!-- Section Notifications -->
        <ion-item-group>
          <ion-item-divider>
            <ion-label>Notifications</ion-label>
          </ion-item-divider>

          <ion-item>
            <ion-icon slot="start" :icon="notificationsOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>Notifications push</h2>
              <p>Recevoir des notifications</p>
            </ion-label>
            <ion-toggle v-model="settings.pushNotifications" @ionChange="saveSettings"></ion-toggle>
          </ion-item>

          <ion-item>
            <ion-icon slot="start" :icon="mailOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>Notifications email</h2>
              <p>Recevoir des emails</p>
            </ion-label>
            <ion-toggle v-model="settings.emailNotifications" @ionChange="saveSettings"></ion-toggle>
          </ion-item>
        </ion-item-group>

        <!-- Section Sécurité -->
        <ion-item-group>
          <ion-item-divider>
            <ion-label>Sécurité</ion-label>
          </ion-item-divider>

          <ion-item button @click="clearCache">
            <ion-icon slot="start" :icon="trashOutline" color="warning"></ion-icon>
            <ion-label>
              <h2>Vider le cache</h2>
              <p>Supprimer les données en cache</p>
            </ion-label>
            <ion-icon slot="end" :icon="chevronForwardOutline"></ion-icon>
          </ion-item>

          <ion-item button @click="logout">
            <ion-icon slot="start" :icon="logOutOutline" color="danger"></ion-icon>
            <ion-label>
              <h2>Déconnexion</h2>
              <p>Se déconnecter de l'application</p>
            </ion-label>
            <ion-icon slot="end" :icon="chevronForwardOutline"></ion-icon>
          </ion-item>
        </ion-item-group>

        <!-- Section Aide -->
        <ion-item-group>
          <ion-item-divider>
            <ion-label>Aide</ion-label>
          </ion-item-divider>

          <ion-item button @click="showHelp">
            <ion-icon slot="start" :icon="helpCircleOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>Aide</h2>
              <p>Documentation et support</p>
            </ion-label>
            <ion-icon slot="end" :icon="chevronForwardOutline"></ion-icon>
          </ion-item>

          <ion-item button @click="showAbout">
            <ion-icon slot="start" :icon="informationCircleOutline" color="primary"></ion-icon>
            <ion-label>
              <h2>À propos</h2>
              <p>Informations sur l'application</p>
            </ion-label>
            <ion-icon slot="end" :icon="chevronForwardOutline"></ion-icon>
          </ion-item>
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
  IonTitle,
  IonButtons,
  IonIcon,
  IonContent,
  IonList,
  IonListHeader,
  IonItem,
  IonItemGroup,
  IonItemDivider,
  IonLabel,
  IonToggle,
  IonButton,
  alertController
} from '@ionic/vue';

import {
  arrowBackOutline,
  informationCircleOutline,
  serverOutline,
  personOutline,
  lockClosedOutline,
  notificationsOutline,
  mailOutline,
  trashOutline,
  logOutOutline,
  helpCircleOutline,
  chevronForwardOutline
} from 'ionicons/icons';

import { authService } from '../../services/api';
import { Capacitor } from '@capacitor/core';

/**
 * Composant AdminSettings
 * - Gère l'interface et la logique métier.
 */
export default {
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonIcon,
    IonContent,
    IonList,
    IonListHeader,
    IonItem,
    IonItemGroup,
    IonItemDivider,
    IonLabel,
    IonToggle,
    IonButton
  },
  computed: {
    apiUrl() {
      // En mode natif, toujours afficher l'API en ligne
      if (Capacitor.isNativePlatform()) {
        return 'https://api.agashop.bi/api'
      }
      // Sinon, utiliser la variable d'environnement ou localhost par défaut
      return import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
    }
  },
  data() {
    return {
      arrowBackOutline,
      informationCircleOutline,
      serverOutline,
      personOutline,
      lockClosedOutline,
      notificationsOutline,
      mailOutline,
      trashOutline,
      logOutOutline,
      helpCircleOutline,
      chevronForwardOutline,
      settings: {
        pushNotifications: true,
        emailNotifications: true
      }
    }
  },
  beforeMount() {
    this.loadSettings();
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
    loadSettings() {
      const savedSettings = localStorage.getItem('app_settings');
      if (savedSettings) {
        try {
          this.settings = { ...this.settings, ...JSON.parse(savedSettings) };
        } catch (e) {
          console.error('Erreur lors du chargement des paramètres:', e);
        }
      }
    },
    saveSettings() {
      localStorage.setItem('app_settings', JSON.stringify(this.settings));
      this.showTostMsg('Paramètres sauvegardés.', 'success', 2000);
    },
    async viewProfile() {
      const user = this.active_user;
      const fullname = `${user?.first_name || ''} ${user?.last_name || ''}`.trim();
      const email = user?.email || user?.username || 'Non défini';

      const alert = await alertController.create({
        header: 'Mon profil',
        message: `Nom : ${fullname || 'Non défini'}\nEmail : ${email}`,
        buttons: ['OK']
      });
      await alert.present();
    },
    async changePassword() {
      const user = this.active_user;
      const email = user?.email || user?.username || null;

      if (!email) {
        const alert = await alertController.create({
          header: 'Changer le mot de passe',
          message: "Impossible de retrouver votre adresse e‑mail. Contactez un administrateur pour réinitialiser votre mot de passe.",
          buttons: ['OK']
        });
        await alert.present();
        return;
      }

      const alert = await alertController.create({
        header: 'Changer le mot de passe',
        message: `Un nouveau mot de passe va être généré et envoyé à cette adresse :\n\n${email}\n\nVoulez-vous continuer ?`,
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Confirmer',
            handler: () => {
              this.performSelfPasswordReset(email);
            }
          }
        ]
      });
      await alert.present();
    },
    async performSelfPasswordReset(email) {
      try {
        const res = await authService.resetPassword(email.trim());
        const statusMsg = res.data?.status || "Un nouveau mot de passe a été envoyé à votre adresse e‑mail.";
        const emailSent = res.data?.email_sent;

        if (emailSent === false) {
          this.showTostMsg(
            statusMsg ||
            "Le mot de passe a été réinitialisé, mais l'envoi de l'e‑mail a échoué. Contactez l'administrateur pour récupérer le nouveau mot de passe.",
            "warning",
            10000
          );
        } else {
          this.showTostMsg(statusMsg, "success", 7000);
        }
      } catch (err) {
        // En cas d'erreur spécifique, on délègue à la gestion générique
        if (typeof this.errorOrRefresh === 'function') {
          this.errorOrRefresh(err, () => this.performSelfPasswordReset(email));
        } else {
          console.error('Erreur lors de la réinitialisation du mot de passe:', err);
          this.showTostMsg(
            "Impossible de changer le mot de passe pour le moment. Veuillez réessayer plus tard ou contacter l'administrateur.",
            "danger",
            7000
          );
        }
      }
    },
    async clearCache() {
      const alert = await alertController.create({
        header: 'Vider le cache',
        message: 'Êtes-vous sûr de vouloir vider le cache ?',
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Vider',
            role: 'destructive',
            handler: () => {
              localStorage.removeItem('app_settings');
              this.showTostMsg('Cache vidé avec succès.', 'success', 2000);
            }
          }
        ]
      });
      await alert.present();
    },
    async logout() {
      const alert = await alertController.create({
        header: 'Déconnexion',
        message: 'Êtes-vous sûr de vouloir vous déconnecter ?',
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Déconnexion',
            role: 'destructive',
            handler: () => {
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              localStorage.removeItem('current_user');
              localStorage.removeItem('current_shop');
              this.$router.push('/login');
            }
          }
        ]
      });
      await alert.present();
    },
    async showHelp() {
      const alert = await alertController.create({
        header: 'Aide',
        message: 'Pour toute assistance, veuillez contacter le support technique.',
        buttons: ['OK']
      });
      await alert.present();
    },
    async showAbout() {
      const alert = await alertController.create({
        header: 'À propos',
        message: 'AgaShop - Application de gestion de boutique\nVersion 1.0.0\n\n© 2025 AgaShop. Tous droits réservés.',
        buttons: ['OK']
      });
      await alert.present();
    }
  }
}
</script>

<style lang="scss" scoped>
ion-header {
  ion-toolbar {
    --background: white;
  }
}

ion-item {
  ion-label {
    h2 {
      font-size: 1.1rem;
      font-weight: 500;
    }
    p {
      margin-top: 5px;
      font-size: 0.9rem;
      font-weight: normal;
      color: var(--ion-color-medium);
    }
  }
}

ion-item-divider {
  --background: var(--ion-color-light);
  --color: var(--ion-color-dark);
  font-weight: 600;
  margin-top: 1rem;
}
</style>
