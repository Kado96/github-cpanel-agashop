<!--
  * @file AdminShops.vue
  * @description Page/Composant pour Admin Shops.
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
            <span>Gestion Boutiques</span>
          </div>
        </ion-title>

        <ion-buttons slot="end">
          <ion-button @click="exportToExcel">
            <ion-icon color="light" size="large" :icon="downloadOutline"></ion-icon>
          </ion-button>
          <ion-button @click="fetchShops">
            <ion-icon color="light" size="large" :icon="refreshCircleOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>

      <!-- Barre de recherche globale -->
      <ion-toolbar color="primary" class="search-toolbar">
        <ion-searchbar
          v-model="searchKeyword"
          placeholder="Rechercher une boutique, propriétaire ou agent..."
          class="custom-searchbar"
          animated
          @ionClear="searchKeyword = ''"
        ></ion-searchbar>
      </ion-toolbar>
    </ion-header>
  
    <ion-content>
      <ion-list class="ion-margin">
        <ion-list-header>
          <ion-label>{{ isAgent ? 'Mes boutiques' : 'Liste des boutiques' }}</ion-label>
        </ion-list-header>

        <ion-item-sliding v-for="shop in filteredShops" :key="shop.id">
          <ion-item-options side="start">
            <ion-item-option @click="editShop(shop)" color="primary">
              <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
              Modifier
            </ion-item-option>
            <ion-item-option @click="confirmDelete(shop)" color="danger">
              <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
              Supprimer
            </ion-item-option>
          </ion-item-options>

          <ion-item button detail @click="openShopActions(shop)">
            <ion-avatar slot="start">
              <ion-icon :icon="storefrontOutline" size="large"></ion-icon>
            </ion-avatar>
            <ion-label>
              <h2>{{ shop.name }}</h2>
              <p v-if="shop.owner">
                Propriétaire : {{ shop.owner.user?.username || shop.owner.user?.email }}
                <br v-if="shop.agent">
                <span v-if="shop.agent">Agent : {{ shop.agent.user?.username || shop.agent.user?.email }}</span>
              </p>
              <p>
                <ion-badge :color="shop.is_active ? 'success' : 'danger'">
                  {{ shop.is_active ? 'Active' : 'Inactive' }}
                </ion-badge>
                <ion-badge color="tertiary" v-if="shop.subscription_plan">
                  {{ shop.subscription_plan === 'FREE' ? 'Essai' : shop.subscription_plan }}
                </ion-badge>
              </p>
            </ion-label>
          </ion-item>

          <ion-item-options side="end">
            <ion-item-option @click="editShop(shop)" color="primary">
              <ion-icon size="large" slot="top" :icon="createOutline"></ion-icon>
              Modifier
            </ion-item-option>
            <ion-item-option v-if="shop.owner" @click="promptManualOwnerPassword(shop)" color="secondary">
              <ion-icon size="large" slot="top" :icon="refreshCircleOutline"></ion-icon>
              Mot de passe
            </ion-item-option>
            <ion-item-option @click="viewShopDetails(shop)" color="medium">
              <ion-icon size="large" slot="top" :icon="eyeOutline"></ion-icon>
              Détails
            </ion-item-option>
            <ion-item-option @click="confirmDelete(shop)" color="danger">
              <ion-icon size="large" slot="top" :icon="trashOutline"></ion-icon>
              Supprimer
            </ion-item-option>
          </ion-item-options>
        </ion-item-sliding>

        <ion-item v-if="filteredShops.length === 0 && !loading">
          <ion-label>
            <p>{{ isAgent ? 'Vous n\'avez pas encore de boutique. Créez-en une avec le bouton +.' : 'Aucune boutique. Utilisez le bouton Ajouter pour en créer une.' }}</p>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>

    <ion-fab vertical="bottom" horizontal="end" slot="fixed" class="ion-margin shop-fab">
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
  IonNote,
  IonFooter,
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
  storefrontOutline,
  eyeOutline,
  keyOutline,
  logInOutline,
  downloadOutline
} from 'ionicons/icons';

import { axiosService } from '../../plugins/axios';
import { shopsService, usersService } from '../../services/api';
import { accountsService } from '../../services/api/accounts';
import { defineAsyncComponent } from 'vue';
import mixins from '../../composables/mixins';
import * as XLSX from 'xlsx';

const ShopForm = defineAsyncComponent(() => import('../../components/admin/ShopForm.vue'));

/**
 * Composant AdminShops
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
    IonNote,
    IonFooter,
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
      storefrontOutline,
      eyeOutline,
      keyOutline,
      logInOutline,
      shops: [],
      loading: false,
      searchKeyword: '',
      downloadOutline
    }
  },
  computed: {
    isAgent() {
      const user = this.$store.state.user;
      const groups = user?.groups || [];
      const hasAgent = groups.some(g => (typeof g === 'string' ? g : g.name) === 'agent');
      const hasAdmin = groups.some(g => {
        const name = typeof g === 'string' ? g : g.name;
        return name === 'admin' || name === 'superuser';
      });
      return hasAgent && !hasAdmin;
    },
    isAdmin() {
      const user = this.$store.state.user;
      const groups = user?.groups || [];
      return groups.some(g => {
        const name = typeof g === 'string' ? g : g.name;
        return name === 'admin' || name === 'superuser';
      });
    },
    filteredShops() {
      let list = this.shops || [];
      
      // Filtre de base pour les agents
      if (!this.isAdmin) {
        const user = this.$store.state.user;
        const userId = user?.id;
        const accountId = user?.account?.id;
        const username = user?.username;
        
        list = list.filter(shop => {
          if (!shop.agent) return false;
          const agentUserId = shop.agent.user?.id;
          const agentAccountId = shop.agent.id;
          const agentUsername = shop.agent.user?.username;
          return agentUserId === userId || 
                 (accountId && agentAccountId === accountId) || 
                 (username && agentUsername === username);
        });
      }

      // Filtre de recherche
      if (this.searchKeyword && this.searchKeyword.trim() !== '') {
        const kw = this.searchKeyword.trim().toLowerCase();
        list = list.filter(shop => {
          const name = (shop.name || '').toLowerCase();
          const owner = (shop.owner?.user?.username || shop.owner?.user?.email || '').toLowerCase();
          const agent = (shop.agent?.user?.username || shop.agent?.user?.email || '').toLowerCase();
          return name.includes(kw) || owner.includes(kw) || agent.includes(kw);
        });
      }

      return list;
    }
  },
  beforeMount() {
    this.fetchShops();
  },
  ionViewWillEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: this.isAgent ? 'Mes Boutiques' : 'Gestion Globale des Boutiques',
      description: this.isAgent
        ? 'Vous gérez ici les boutiques qui vous sont attribuées. Créez de nouvelles boutiques pour vos clients.'
        : 'Surveillez et gérez l\'ensemble des points de vente AgaShop. Vous voyez ici qui possède quelle boutique et quel est l\'agent responsable.',
      elements: [
        { type: 'Statut', label: 'Active / Inactive', desc: 'Indique si la boutique peut encore vendre. Utile pour suspendre des accès.' },
        { type: 'Abonnement', label: 'Essai / Plan', desc: 'Permet de voir qui est en période gratuite et qui a un abonnement payant.' },
        { type: 'Sécurité', label: 'Mot de passe', desc: 'L\'option "Mot de passe" (glisser à gauche) permet de dépanner un client bloqué en lui créant un code temporaire.' }
      ],
      faq: [
        { question: 'Comment activer une boutique ?', answer: 'Modifiez la boutique et cochez la case "Est Active".' },
        { question: 'À quoi servent les Détails ?', answer: 'Ils affichent les informations techniques (Province, Commune, Dates d\'essai) pour le support client.' }
      ]
    });
  },
  beforeUnmount() {
    this.$store.commit('SET_HELP_CONTEXT', null);
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
    fetchShops() {
      this.loading = true;
      const all = [];
      const fetchPage = async (url) => {
        try {
          const res = url ? await axiosService.get(url) : await shopsService.getShops();
          const data = res.data;
          const results = data.results || (Array.isArray(data) ? data : []);
          all.push(...results);
          if (data.next) {
            return fetchPage(data.next);
          }
          this.shops = all;
          this.loading = false;
        } catch (err) {
          this.loading = false;
          this.errorOrRefresh(err, () => this.fetchShops());
        }
      };
      return fetchPage();
    },
    async openCreateModal() {
      this.blurActiveElement();
      const modal = await modalController.create({
        component: ShopForm,
        componentProps: { mode: 'create' }
      });
      modal.present();

      const { data, role } = await modal.onWillDismiss();
      if (role === 'confirm') {
        this.fetchShops();
      }
    },
    async editShop(shop) {
      this.blurActiveElement();
      const modal = await modalController.create({
        component: ShopForm,
        componentProps: { mode: 'edit', shop: shop }
      });
      modal.present();

      const { data, role } = await modal.onWillDismiss();
      if (role === 'confirm') {
        this.fetchShops();
      }
    },
    async viewShopDetails(shop) {
      const pad = (label, width = 16) => label.padEnd(width, ' ');
      const val = (v) => (v != null && String(v).trim() !== '') ? String(v).trim() : 'N/A';
      
      const user = shop.owner?.user || {};
      const username = val(user.username);
      const email = val(user.email);
      const phone = val(shop.owner?.phone_number || (user.account && user.account.phone_number));
      
      const rows = [
        `IDENTIFIANTS :`,
        `${pad('Nom d\'util.')} : ${username}`,
        `${pad('Email')} : ${email}`,
        `${pad('Téléphone')} : ${phone}`,
        `${pad('Agent')} : ${shop.agent?.user?.username || 'Aucun'}`,
        `----------------`,
        `BOUTIQUE :`,
        `${pad('Province')} : ${val(shop.province)}`,
        `${pad('Commune')} : ${val(shop.commune)}`,
        `${pad('Statut')} : ${shop.is_active ? 'Active' : 'Inactive'}`,
        `${pad('Plan')} : ${shop.subscription_plan || 'N/A'}`,
        `${pad('Début Essai')} : ${val(shop.trial_start_date?.split('T')[0])}`,
        `${pad('Fin Essai')} : ${val(shop.trial_end_date?.split('T')[0])}`
      ];
      const alert = await alertController.create({
        header: shop.name,
        message: `<pre style="font-family: monospace; white-space: pre-wrap; margin: 0;">${rows.join('\n')}</pre>`,
        buttons: ['Fermer']
      });
      await alert.present();
    },
    async openShopActions(shop) {
      const buttons = [
        {
          text: 'Modifier',
          icon: createOutline,
          handler: () => this.editShop(shop)
        }
      ];

      // Mot de passe, suppression et connexion : accessibles à tout utilisateur
      // (la liste filteredShops garantit déjà que l'agent ne voit que ses propres boutiques)
      buttons.push({
        text: 'Modifier mot de passe',
        icon: keyOutline,
        handler: () => this.promptManualOwnerPassword(shop)
      });
      buttons.push({
        text: 'Supprimer',
        role: 'destructive',
        icon: trashOutline,
        handler: () => this.confirmDelete(shop)
      });
      buttons.push({
        text: 'Se connecter comme boutique',
        icon: logInOutline,
        handler: () => this.impersonateShop(shop)
      });

      buttons.push({
        text: 'Annuler',
        role: 'cancel'
      });

      const sheet = await actionSheetController.create({
        header: shop.name || 'Boutique',
        buttons
      });
      await sheet.present();
    },
    impersonateShop(shop) {
      if (!shop || !shop.id) {
        this.showTostMsg("Cette boutique est invalide.", "danger", 3000);
        return;
      }
      
      // Mettre à jour le shop courant dans le storage et le store
      localStorage.setItem('current_shop', JSON.stringify(shop));
      this.$store.state.shop = shop;
      
      // Notifier l'utilisateur
      this.showTostMsg(`Connecté en tant que ${shop.name}`, 'success', 2000);
      
      // Rediriger vers le tableau de bord de la boutique
      this.$router.push('/shop');
    },
    async confirmResetOwnerPassword(shop) {
      if (!shop.owner || !shop.owner.user) {
        this.showTostMsg("Aucun propriétaire associé à cette boutique.", "warning", 4000);
        return;
      }

      const ownerUser = shop.owner.user;
      const ownerLabel = ownerUser.username || ownerUser.email || 'propriétaire';

      const alert = await alertController.create({
        header: 'Réinitialiser le mot de passe',
        message: `Voulez-vous générer un nouveau mot de passe pour l'utilisateur propriétaire "${ownerLabel}" de cette boutique ?\n\nUn nouveau mot de passe sera généré et les anciennes sessions seront déconnectées.`,
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Confirmer',
            handler: () => {
              this.resetPasswordForShopOwner(shop);
            }
          }
        ]
      });

      await alert.present();
    },
    resetPasswordForShopOwner(shop) {
      if (!shop.owner || !shop.owner.id) {
        this.showTostMsg("Aucun compte propriétaire valide associé à cette boutique.", "warning", 4000);
        return;
      }

      const accountId = shop.owner.id;
      const ownerUser = shop.owner.user || {};
      const ownerLabel = ownerUser.username || ownerUser.email || 'propriétaire';

      accountsService.resetPasswordForAccount(accountId)
        .then(async (resp) => {
          const statusMsg = resp.data?.status || "Mot de passe du propriétaire réinitialisé avec succès.";
          const emailSent = resp.data?.email_sent;
          const newPassword = resp.data?.new_password;

          if (emailSent === false) {
            this.showTostMsg(
              statusMsg ||
              "Le mot de passe a été réinitialisé, mais l'envoi de l'e-mail a échoué. Communiquez manuellement le nouveau mot de passe au propriétaire.",
              "warning",
              10000
            );
          } else {
            this.showTostMsg(statusMsg, "success", 7000);
          }

          if (newPassword) {
            const alert = await alertController.create({
              header: 'Nouveau mot de passe généré',
              message: `Le nouveau mot de passe pour le propriétaire de la boutique "${shop.name}" (${ownerLabel}) est :\n\n${newPassword}\n\nTransmettez-lui ce mot de passe de manière sécurisée.`,
              buttons: ['OK']
            });
            await alert.present();
          }
        })
        .catch((err) => {
          this.errorOrRefresh(err, () => this.resetPasswordForShopOwner(shop));
        });
    },
    async promptManualOwnerPassword(shop) {
      if (!shop.owner || !shop.owner.user) {
        this.showTostMsg("Aucun propriétaire associé à cette boutique.", "warning", 4000);
        return;
      }

      const ownerUser = shop.owner.user;
      const ownerLabel = ownerUser.username || ownerUser.email || 'propriétaire';

      const alert = await alertController.create({
        header: 'Mot de passe BOUTIQUE',
        inputs: [
          {
            name: 'password',
            type: 'text',
            placeholder: 'Nouveau mot de passe (min. 4 caractères)'
          }
        ],
        message: `Saisissez un nouveau mot de passe pour le compte de la boutique "${shop.name}".\n\nCe mot de passe sera celui utilisé pour se connecter à cette boutique spécifique.`,
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Confirmer',
            handler: async (data) => {
              const password = (data?.password || '').trim();
              if (!password || password.length < 4) {
                this.showTostMsg('Le mot de passe doit contenir au moins 4 caractères.', 'warning', 4000);
                return false;
              }
              await this.setManualOwnerPassword(shop, password);
              return true;
            }
          }
        ]
      });

      await alert.present();
    },
    async setManualOwnerPassword(shop, password) {
      try {
        if (!shop.owner || !shop.owner.user) {
          this.showTostMsg("Aucun propriétaire valide pour cette boutique.", "warning", 4000);
          return;
        }

        const ownerUserId = shop.owner.user.id;
        await usersService.updateUser(ownerUserId, { password });

        this.showTostMsg('Mot de passe du propriétaire modifié avec succès.', 'success', 3000);

        const ownerLabel = shop.owner.user.username || shop.owner.user.email || 'propriétaire';
        const alert = await alertController.create({
          header: 'Nouveau mot de passe Boutique',
          message: `Le nouveau mot de passe pour la boutique "${shop.name}" est :\n\n${password}\n\nTransmettez-le manuellement au gérant de la boutique.`,
          buttons: ['OK']
        });
        await alert.present();
      } catch (err) {
        this.errorOrRefresh(err, () => this.setManualOwnerPassword(shop, password));
      }
    },
    async confirmDelete(shop) {
      const alert = await alertController.create({
        header: 'Confirmer la suppression',
        message: `Êtes-vous sûr de vouloir supprimer la boutique "${shop.name}" ? Cette action est irréversible.`,
        buttons: [
          {
            text: 'Annuler',
            role: 'cancel'
          },
          {
            text: 'Supprimer',
            role: 'destructive',
            handler: () => {
              this.deleteShop(shop.id);
            }
          }
        ]
      });
      await alert.present();
    },
    deleteShop(shopId) {
      shopsService.deleteShop(shopId)
        .then(() => {
          this.showTostMsg('Boutique supprimée avec succès.', 'success', 3000);
          this.fetchShops();
        })
        .catch((err) => {
          this.errorOrRefresh(err, () => this.deleteShop(shopId));
        });
    },
    exportToExcel() {
      if (!this.filteredShops || this.filteredShops.length === 0) {
        this.showTostMsg("Aucune boutique à exporter.", "warning", 3000);
        return;
      }

      const data = this.filteredShops.map(shop => ({
        "ID": shop.id,
        "Nom": shop.name,
        "Propriétaire": shop.owner?.user?.username || shop.owner?.user?.email || 'N/A',
        "Agent": shop.agent?.user?.username || shop.agent?.user?.email || 'Aucun',
        "Province": shop.province || 'N/A',
        "Commune": shop.commune || 'N/A',
        "Statut": shop.is_active ? 'Active' : 'Inactive',
        "Plan": shop.subscription_plan || 'N/A'
      }));

      const ws = XLSX.utils.json_to_sheet(data);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Boutiques");
      XLSX.writeFile(wb, `Boutiques_AgaShop_${new Date().toISOString().split('T')[0]}.xlsx`);
      
      this.showTostMsg("Liste exportée avec succès.", "success", 2000);
    }
  }
}
</script>

<style lang="scss" scoped>
ion-content {
  --background: #f8fafc;
}

.bottom-bar {
  --border-width: 0;
  box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
  
  .bottom-actions {
    display: flex;
    justify-content: center;
    padding: 8px;
  }
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

ion-fab.shop-fab {
  bottom: 72px;
}
ion-fab {
  margin-bottom: 2px;
  margin-right: 16px;
}

// Styles du dashboard (cohérence)
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
