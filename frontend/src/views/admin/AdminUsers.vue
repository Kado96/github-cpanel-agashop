<!--
  * @file AdminUsers.vue
  * @description Page/Composant pour Admin Users.
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
            <span>Gestion des agents</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchUsers">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>

      <!-- Barre de recherche globale -->
      <ion-toolbar color="primary" class="search-toolbar">
        <ion-searchbar
          v-model="searchKeyword"
          placeholder="Rechercher un agent..."
          class="custom-searchbar"
          animated
          @ionClear="searchKeyword = ''"
        ></ion-searchbar>
      </ion-toolbar>
    </ion-header>
  
    <ion-content>
      <ion-list class="ion-margin">
        <ion-list-header>
          <ion-label>Liste des agents</ion-label>
        </ion-list-header>

        <ion-item-sliding v-for="user in filteredUsers" :key="user.id">
          <ion-item-options side="start">
            <ion-item-option @click="editUser(user)" color="primary">
              <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
              Modifier
            </ion-item-option>
            <ion-item-option @click="confirmDelete(user)" color="danger">
              <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
              Supprimer
            </ion-item-option>
          </ion-item-options>

          <ion-item button detail @click="openUserActions(user)">
            <ion-avatar slot="start">
              <ion-icon :icon="personCircleOutline" size="large"></ion-icon>
            </ion-avatar>
            <ion-label>
              <h2>{{ user.id }} - {{ user.username || user.email }}</h2>
              <p v-if="user.first_name || user.last_name">{{ user.first_name }} {{ user.last_name }}</p>
              <p v-if="user.groups && user.groups.length > 0">
                <ion-badge v-for="group in user.groups" :key="group" color="primary">{{ (typeof group === 'string' ? group : group.name) || group }}</ion-badge>
              </p>
              <p v-if="user.is_superuser">
                <ion-badge color="danger">Superuser</ion-badge>
              </p>
              <p v-if="typeof user.shops_count === 'number'">
                <ion-badge color="secondary">{{ user.shops_count }} boutique(s)</ion-badge>
              </p>
            </ion-label>
          </ion-item>

          <ion-item-options side="end">
            <ion-item-option @click="editUser(user)" color="primary">
              <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
              Modifier
            </ion-item-option>
            <ion-item-option @click="viewAccount(user)" color="secondary">
              <ion-icon size="large" slot="top" :icon="personOutline"></ion-icon>
              Compte
            </ion-item-option>
            <ion-item-option @click="confirmDelete(user)" color="danger">
              <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
              Supprimer
            </ion-item-option>
          </ion-item-options>
        </ion-item-sliding>

        <ion-item v-if="filteredUsers.length === 0">
          <ion-label>
            <p>Aucun agent trouvé.</p>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>

    <ion-fab vertical="bottom" horizontal="end" slot="fixed" class="ion-margin users-fab">
      <ion-fab-button @click="openCreateModal" color="primary">
        <ion-icon :icon="addOutline"></ion-icon>
      </ion-fab-button>
    </ion-fab>
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
  IonList,
  IonListHeader,
  IonAvatar,
  IonBadge,
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
  createOutline,
  trashOutline,
  personOutline,
  personCircleOutline,
  downloadOutline
} from 'ionicons/icons';

import { usersService, accountsService } from '../../services/api';
import { defineAsyncComponent } from 'vue';
import mixins from '../../composables/mixins';
import * as XLSX from 'xlsx';
import { saveWorkbook } from '../../utils/exportExcel';

const UserForm = defineAsyncComponent(() => import('../../components/admin/UserForm.vue'));

/**
 * Composant AdminUsers
 * - Gère l'interface et la logique métier.
 */
export default {
  mixins: [mixins],
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
    IonList,
    IonListHeader,
    IonAvatar,
    IonBadge,
    IonFab,
    IonFabButton,
    IonSearchbar
  },
  data() {
    return {
      arrowBackOutline,
      refreshCircleOutline,
      addOutline,
      createOutline,
      trashOutline,
      personOutline,
      personCircleOutline,
      downloadOutline,
      users: [],
      searchKeyword: ''
    }
  },
  computed: {
    filteredUsers() {
      let list = this.users || [];
      if (this.searchKeyword && this.searchKeyword.trim() !== '') {
        const kw = this.searchKeyword.trim().toLowerCase();
        list = list.filter(u => {
          const name = `${u.first_name || ''} ${u.last_name || ''}`.toLowerCase();
          const email = (u.email || '').toLowerCase();
          const username = (u.username || '').toLowerCase();
          return name.includes(kw) || email.includes(kw) || username.includes(kw);
        });
      }
      return list;
    }
  },
  beforeMount() {
    this.fetchUsers();
  },
  ionViewWillEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Gestion des Collaborateurs',
      description: 'Cet écran est dédié à la gestion des comptes Agents et Administrateurs. Vous pouvez contrôler qui a accès aux fonctions avancées de la plateforme AgaShop.',
      elements: [
        { type: 'Identité', label: 'Badge Group', desc: 'Indique le niveau d\'accès (Agent, Admin ou Superuser).' },
        { type: 'Activité', label: 'Boutique(s)', desc: 'Affiche le nombre de boutiques rattachées à cet agent.' },
        { type: 'Option', label: 'Actions', desc: 'Glissez un utilisateur pour le modifier, voir son compte ou supprimer son accès.' }
      ],
      faq: [
        { question: 'Comment réinitialiser un mot de passe ?', answer: 'Cliquez sur l\'agent, puis choisissez "Compte" pour accéder à la gestion de ses identifiants.' },
        { question: 'Quelle est la différence entre Agent et Admin ?', answer: 'Un Agent gère les boutiques de terrain. Un Admin peut en plus modifier le catalogue maître et gérer d\'autres utilisateurs.' }
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
    fetchUsers() {
      usersService.getAllUsers()
        .then((res) => {
          this.users = res.data.results || res.data || [];
        })
        .catch((err) => {
          this.errorOrRefresh(err, () => this.fetchUsers());
        });
    },
    async openCreateModal() {
      const modal = await modalController.create({
        component: UserForm,
        componentProps: { mode: 'create' }
      });
      modal.present();

      const { data, role } = await modal.onWillDismiss();
      if (role === 'confirm') {
        this.fetchUsers();
      }
    },
    async editUser(user) {
      const modal = await modalController.create({
        component: UserForm,
        componentProps: { mode: 'edit', user: user }
      });
      modal.present();

      const { data, role } = await modal.onWillDismiss();
      if (role === 'confirm') {
        this.fetchUsers();
      }
    },
    async openUserActions(user) {
      const sheet = await actionSheetController.create({
        header: user.email || user.username || 'Utilisateur',
        buttons: [
          {
            text: 'Modifier',
            icon: createOutline,
            handler: () => this.editUser(user)
          },
          {
            text: 'Supprimer',
            role: 'destructive',
            icon: trashOutline,
            handler: () => this.confirmDelete(user)
          },
          {
            text: 'Annuler',
            role: 'cancel'
          }
        ]
      });
      await sheet.present();
    },
    async viewAccount(user) {
      // Récupérer le compte associé à cet utilisateur
      accountsService.getAllAccounts()
        .then((res) => {
          const accounts = res.data.results || res.data || [];
          const account = accounts.find(acc => acc.user === user.id);
          if (account) {
            this.$router.push({ name: 'admin-accounts', query: { accountId: account.id } });
          } else {
            this.showTostMsg("Aucun compte associé à cet utilisateur.", "warning", 3000);
          }
        })
        .catch((err) => {
          this.errorOrRefresh(err);
        });
    },
    async confirmDelete(user) {
      const alert = await alertController.create({
        header: 'Confirmer la suppression',
        message: `Êtes-vous sûr de vouloir supprimer l'utilisateur "${user.username}" ? Cette action est irréversible.`,
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Supprimer',
            role: 'destructive',
            handler: () => {
              this.deleteUser(user.id);
            }
          }
        ]
      });
      await alert.present();
    },
    async confirmResetPassword(user) {
      const alert = await alertController.create({
        header: 'Réinitialiser le mot de passe',
        message: `Voulez-vous générer un nouveau mot de passe pour l'utilisateur "${user.username}" ? Un e-mail lui sera envoyé avec le nouveau mot de passe.`,
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Confirmer',
            handler: () => {
              this.resetPasswordForUser(user);
            }
          }
        ]
      });
      await alert.present();
    },
    resetPasswordForUser(user) {
      // Récupérer le compte associé à cet utilisateur
      accountsService.getAllAccounts()
        .then((res) => {
          const accounts = res.data.results || res.data || [];
          const account = accounts.find(acc => acc.user === user.id);

          if (!account) {
            this.showTostMsg("Aucun compte associé à cet utilisateur.", "warning", 3000);
            return;
          }

          accountsService.resetPasswordForAccount(account.id)
            .then((resp) => {
              const statusMsg = resp.data?.status || "Mot de passe réinitialisé avec succès.";
              const emailSent = resp.data?.email_sent;
              const newPassword = resp.data?.new_password;

              if (emailSent === false) {
                this.showTostMsg(
                  statusMsg ||
                  "Le mot de passe a été réinitialisé, mais l'envoi de l'e-mail a échoué. Contactez l'administrateur pour transmettre le nouveau mot de passe à l'utilisateur.",
                  "warning",
                  10000
                );
              } else {
                this.showTostMsg(statusMsg, "success", 7000);
              }

              // Afficher le nouveau mot de passe dans une alerte réservée à l'admin/agent
              if (newPassword) {
                alertController.create({
                  header: 'Nouveau mot de passe généré',
                  message: `Le nouveau mot de passe pour l'utilisateur "${user.username}" est :\n\n${newPassword}\n\nTransmettez-lui ce mot de passe de manière sécurisée.`,
                  buttons: ['OK']
                }).then(alert => alert.present());
              }
            })
            .catch((err) => {
              this.errorOrRefresh(err, () => this.resetPasswordForUser(user));
            });
        })
        .catch((err) => {
          this.errorOrRefresh(err);
        });
    },
    deleteUser(userId) {
      usersService.deleteUser(userId)
        .then(() => {
          this.showTostMsg('Utilisateur supprimé avec succès.', 'success', 3000);
          this.fetchUsers();
        })
        .catch((err) => {
          this.errorOrRefresh(err, () => this.deleteUser(userId));
        });
    },
    async exportToExcel() {
      if (!this.filteredUsers || this.filteredUsers.length === 0) {
        this.showTostMsg("Aucun agent à exporter.", "warning", 3000);
        return;
      }

      const data = this.filteredUsers.map(u => ({
        "ID": u.id,
        "Nom Prénom": `${u.first_name || ''} ${u.last_name || ''}`.trim(),
        "Email": u.email || 'N/A',
        "Nom d'utilisateur": u.username || 'N/A',
        "Rôle": (u.groups || []).map(g => typeof g === 'string' ? g : g.name).join(', ') || 'N/A',
        "Superviseur": u.is_superuser ? 'Oui' : 'Non',
        "Boutiques gérées": u.shops_count || 0
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Agents");
      await saveWorkbook(wb, `Agents_AgaShop_${new Date().toISOString().split('T')[0]}.xlsx`);

      this.showTostMsg("Liste exportée avec succès.", "success", 2000);
    }
  }
}
</script>

<style lang="scss" scoped>
ion-content {
  --background: #f8fafc;
}

ion-avatar {
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ion-color-primary);
}

ion-badge {
  margin-right: 6px;
  margin-top: 4px;
}

ion-fab.users-fab {
  bottom: 72px;
}

// Styles du dashboard (pour cohérence avec ShopProducts)
.header-title-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 1.2;
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
