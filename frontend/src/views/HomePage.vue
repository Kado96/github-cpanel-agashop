<!--
  * @file HomePage.vue
  * @description Page/Composant pour Home Page.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar class="home-toolbar">
        <ion-title color="light">
          <div class="header-logo">
            <ion-icon :icon="storefrontOutline" class="logo-icon"></ion-icon>
            <span>AgaShop</span>
          </div>
        </ion-title>
        <ion-buttons slot="end">
          <ion-button id="home-popover-trigger" class="menu-btn">
            <ion-icon color="light" size="large" :icon="ellipsisVertical"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-popover trigger="home-popover-trigger" trigger-action="click" :dismiss-on-select="true">
          <ion-content>
            <ion-list lines="none" class="popover-list">
              <ion-item :button="true" :detail="false" @click="openProfil" class="popover-item">
                <ion-icon :icon="personOutline" slot="start" color="primary"></ion-icon>
                <ion-label>Mon Profil</ion-label>
              </ion-item>
              <ion-item :button="true" :detail="false" @click="logOut()" class="popover-item logout-item">
                <ion-icon :icon="exitOutline" slot="start" color="danger"></ion-icon>
                <ion-label>Déconnexion</ion-label>
              </ion-item>
            </ion-list>
          </ion-content>
        </ion-popover>
      </ion-toolbar>
    </ion-header>

    <ion-content class="home-content" :fullscreen="true">
      <!-- Hero Section -->
      <div class="hero-header">
        <div class="hero-text">
          <span class="welcome-label">Bienvenue</span>
          <h1 class="user-name">{{ $store.state.user?.first_name }} {{ $store.state.user?.last_name }}</h1>
          <p class="hero-date">{{ currentFormattedDate }}</p>
        </div>
        <div class="hero-avatar-container" @click="openProfil">
          <div class="avatar-ring"></div>
          <ion-thumbnail class="hero-avatar">
            <img src="../assets/avatar.png" />
          </ion-thumbnail>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="stats-ribbon ion-margin-horizontal">
        <div class="stat-pill">
          <span class="stat-value">{{ $store.state.shops.length }}</span>
          <span class="stat-label">Boutiques</span>
        </div>
        <div class="stat-pill">
          <span class="stat-value">{{ activeShopsCount }}</span>
          <span class="stat-label">Actives</span>
        </div>
      </div>

      <!-- Section Title -->
      <div class="section-container">
        <div class="section-title-wrapper ion-padding-horizontal">
          <ion-icon :icon="businessOutline" class="section-title-icon"></ion-icon>
          <span class="section-title">Mes Boutiques</span>
          <div class="section-line"></div>
        </div>

        <!-- Empty State -->
        <div v-if="$store.state.shops.length === 0" class="premium-empty-state">
          <div class="empty-illustration">
            <div class="blob-bg"></div>
            <ion-icon :icon="fastFoodOutline" class="main-empty-icon"></ion-icon>
            <div class="plus-sparkle">+</div>
          </div>
          <h3>Aucune boutique</h3>
          <p>Commencez par créer votre premier point de vente.</p>
          <ion-button fill="outline" color="secondary" shape="round" @click="createShop" class="empty-action-btn">
            Créer ma Boutique
          </ion-button>
        </div>

        <!-- Shops Grid -->
        <ion-grid v-else class="shops-grid ion-padding-horizontal">
          <ion-row>
            <ion-col v-for="shop in $store.state.shops" :key="shop.id" size="12" size-sm="6" size-md="4" size-lg="3" class="shop-col">
              <div class="premium-shop-card" @click="handleCardClick(shop)" :class="{ 'inactive-card': !shop.is_active }">
                
                <!-- Status Badge + Actions Toggle -->
                <div class="card-header-actions">
                  <div class="card-badge" :class="shop.is_active ? 'badge-active' : 'badge-inactive'">
                    <ion-icon :icon="shop.is_active ? checkmarkCircleOutline : alertCircleOutline" class="badge-icon"></ion-icon>
                    <span>{{ shop.is_active ? 'Actif' : 'En attente' }}</span>
                  </div>
                  
                  <ion-button fill="clear" color="medium" class="action-trigger" @click.stop="presentActionSheet(shop)">
                    <ion-icon slot="icon-only" :icon="ellipsisHorizontalOutline"></ion-icon>
                  </ion-button>
                </div>
                
                <!-- Icon Holder -->
                <div class="card-icon-holder" :style="{ background: getIconBg(shop.id) }">
                  <ion-icon :icon="fastFoodOutline" class="card-icon" :style="{ color: getIconColor(shop.id) }"></ion-icon>
                </div>

                <!-- Info -->
                <div class="card-info">
                  <h2 class="card-name">{{ shop.name }}</h2>
                  <p class="card-location">
                    <ion-icon :icon="locationOutline"></ion-icon>
                    {{ shop.commune || 'Bujumbura' }}
                  </p>
                </div>

                <!-- Footer/Action -->
                <div class="card-footer" :class="{ 'footer-inactive': !shop.is_active }">
                  <span class="footer-text">{{ shop.is_active ? 'Gérer la boutique' : 'Options de gestion' }}</span>
                  <ion-icon :icon="shop.is_active ? chevronForwardOutline : optionsOutline" class="footer-arrow"></ion-icon>
                </div>

                <div class="card-glow"></div>
              </div>
            </ion-col>
          </ion-row>
        </ion-grid>
      </div>

      <ion-fab slot="fixed" vertical="bottom" horizontal="end" class="custom-fab-position">
        <ion-fab-button color="secondary" @click="createShop" class="premium-fab">
          <ion-icon :icon="addOutline"></ion-icon>
        </ion-fab-button>
      </ion-fab>
    </ion-content>
  </ion-page>
</template>

<script>
import CreateShop from '../components/shop/CreateShop.vue';
import EditShop from '../components/shop/EditShop.vue';
import {
  IonPage, IonHeader, IonToolbar, IonButtons, IonButton, IonIcon,
  IonContent, IonItem, IonLabel, IonThumbnail, IonRow, IonCol,
  IonTitle, IonFab, IonFabButton, IonList, IonPopover, IonGrid,
  modalController, actionSheetController, alertController
} from '@ionic/vue';

import {
  exitOutline, addOutline, fastFoodOutline, personOutline,
  ellipsisVertical, storefrontOutline, businessOutline,
  locationOutline, checkmarkCircleOutline, alertCircleOutline,
  chevronForwardOutline, arrowBackOutline, ellipsisHorizontalOutline,
  trashOutline, createOutline, optionsOutline
} from 'ionicons/icons'
import ProfilPage from './ProfilPage.vue';
import { shopsService } from '../services/api';

/**
 * Composant HomePage
 * - Gère l'interface et la logique métier.
 */
export default {
  name: 'HomePage',
  components:{
    IonPage, IonHeader, IonToolbar, IonButtons, IonButton, IonIcon,
    IonContent, IonItem, IonLabel, IonThumbnail, IonRow, IonCol,
    IonTitle, IonFab, IonFabButton, IonList, IonPopover, IonGrid
  },
  data(){
    return{
      exitOutline, addOutline, fastFoodOutline, personOutline,
      ellipsisVertical, storefrontOutline, businessOutline,
      locationOutline, checkmarkCircleOutline, alertCircleOutline,
      chevronForwardOutline, arrowBackOutline, ellipsisHorizontalOutline,
      trashOutline, createOutline, optionsOutline
    }
  },
  computed: {
    activeShopsCount() {
      return this.$store.state.shops.filter(s => s.is_active).length;
    },
    currentFormattedDate() {
      const options = { weekday: 'long', day: 'numeric', month: 'long' };
      return new Intl.DateTimeFormat('fr-FR', options).format(new Date());
    }
  },
  mounted(){
    this.fetchShops();
  },
  methods:{
    getIconBg(id) {
      const colors = ['#e3f2fd', '#f3e5f5', '#e8f5e9', '#fff3e0', '#fce4ec'];
      return colors[id % colors.length];
    },
    getIconColor(id) {
      const colors = ['#1e88e5', '#8e24aa', '#43a047', '#fb8c00', '#d81b60'];
      return colors[id % colors.length];
    },
    handleCardClick(shop) {
      if (shop.is_active) {
        this.goToShop(shop);
      } else {
        this.presentActionSheet(shop);
      }
    },
    goToShop(shop){
      this.$store.state.shop = shop;
      localStorage.setItem("current_shop", JSON.stringify(shop));
      this.$router.push("/shop");
    },
    async presentActionSheet(shop) {
      const buttons = [
        {
          text: 'Modifier',
          icon: createOutline,
          handler: () => { this.openEditShop(shop); }
        },
        {
          text: 'Supprimer',
          role: 'destructive',
          icon: trashOutline,
          handler: () => { this.confirmDelete(shop); }
        }
      ];

      // Ajouter l'option "Entrer" même si inactif pour répondre à "activer tous les boutons"
      if (!shop.is_active) {
        buttons.unshift({
          text: 'Entrer (Aperçu)',
          icon: chevronForwardOutline,
          handler: () => { 
            this.showTostMsg("Mode Aperçu : Certaines fonctionnalités peuvent être limitées.", "warning", 3000);
            this.goToShop(shop); 
          }
        });
      }

      buttons.push({
        text: 'Annuler',
        role: 'cancel',
        icon: close
      });

      const actionSheet = await actionSheetController.create({
        header: shop.name,
        subHeader: 'Gestion de boutique',
        cssClass: 'custom-action-sheet',
        buttons: buttons
      });
      await actionSheet.present();
    },
    fetchShops(){
      shopsService.getShops()
        .then((res)=>{
            this.$store.state.shops = res.data.results;
        }).catch((err)=>{
            this.errorOrRefresh(err, () => this.fetchShops());
        }) 
    },
    async createShop() {
      const modal = await modalController.create({
          component: CreateShop,
          cssClass: 'responsive-modal'
        });
        modal.present();
        const { role } = await modal.onWillDismiss();
        if (role === 'confirm') this.fetchShops();
    },
    async openEditShop(shop) {
      const modal = await modalController.create({
        component: EditShop,
        componentProps: { shop },
        cssClass: 'responsive-modal'
      });
      modal.present();
      const { role } = await modal.onWillDismiss();
      if (role === 'confirm') this.fetchShops();
    },
    async confirmDelete(shop) {
      const alert = await alertController.create({
        header: 'Supprimer la boutique ?',
        message: `Voulez-vous vraiment supprimer "${shop.name}" ? Cette action est irréversible.`,
        buttons: [
          { text: 'Annuler', role: 'cancel' },
          {
            text: 'Supprimer',
            role: 'destructive',
            handler: () => { this.deleteShop(shop); }
          }
        ]
      });
      await alert.present();
    },
    deleteShop(shop) {
      shopsService.deleteShop(shop.id)
        .then(() => {
          this.showTostMsg("Boutique supprimée avec succès.", "success", 3000);
          this.fetchShops();
        })
        .catch(err => this.errorOrRefresh(err, () => this.deleteShop(shop)));
    },
    async openProfil() {
      const modal = await modalController.create({
          component: ProfilPage,
          cssClass: 'responsive-modal'
        });
        modal.present();
    },
    logOut() {
      localStorage.clear();
      this.$store.state.user = null;
      this.$store.state.shops = [];
      this.$router.push('/login');
    }
  }
}
</script>

<style lang="scss" scoped>
.home-toolbar {
  --background: #f15a24;
  --border-width: 0;
  --padding-top: 8px;
  --padding-bottom: 8px;
}
.header-logo { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.25rem; }
.logo-icon { font-size: 1.4rem; }

.home-content { --background: #f8fafc; }

.hero-header {
  background: linear-gradient(135deg, #f15a24 0%, #ff8c00 100%);
  padding: 32px 24px 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 0 0 32px 32px;
  box-shadow: 0 10px 30px rgba(241, 90, 36, 0.15);
  margin-bottom: -32px;
}

.hero-text {
  color: white;
  .welcome-label { text-transform: uppercase; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; opacity: 0.9; }
  .user-name { margin: 4px 0 0; font-size: 1.7rem; font-weight: 800; letter-spacing: -0.02em; }
  .hero-date { margin: 4px 0 0; font-size: 0.85rem; font-weight: 500; opacity: 0.85; text-transform: capitalize; }
}

.hero-avatar {
  width: 60px; height: 60px; border-radius: 50%; border: 3px solid white; box-shadow: 0 8px 16px rgba(0,0,0,0.15);
  img { object-fit: cover; }
}

.stats-ribbon {
  background: white; border-radius: 20px; padding: 16px; display: flex; justify-content: space-around;
  box-shadow: 0 10px 25px rgba(0,0,0,0.06); position: relative; z-index: 10; border: 1px solid rgba(0,0,0,0.03);
}

.stat-pill {
  display: flex; flex-direction: column; align-items: center;
  .stat-value { font-size: 1.25rem; font-weight: 800; color: #0f172a; }
  .stat-label { font-size: 0.72rem; font-weight: 600; color: #64748b; text-transform: uppercase; }
  &:not(:last-child) { border-right: 1px solid #f1f5f9; padding-right: 30px; }
}

.section-container { margin-top: 48px; }
.section-title-wrapper { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.section-title-icon { font-size: 1.3rem; color: #f15a24; }
.section-title { font-size: 1.15rem; font-weight: 800; color: #1e293b; }
.section-line { height: 2px; background: #e2e8f0; flex-grow: 1; margin-left: 10px; border-radius: 2px; }

.premium-shop-card {
  background: white; border-radius: 24px; padding: 20px; display: flex; flex-direction: column; align-items: center;
  position: relative; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #f1f5f9;
  height: 100%; transition: all 0.3s cubic-bezier(.4,0,.2,1); cursor: pointer;

  &:hover { transform: translateY(-8px); box-shadow: 0 12px 25px rgba(0,0,0,0.08); }
  &:active { transform: scale(0.96); }
  &.inactive-card { opacity: 0.9; background: #fafafa; }
}

.card-header-actions {
  width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; z-index: 5;
}

.card-badge {
  display: flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 100px; font-size: 0.68rem; font-weight: 700;
  &.badge-active { background: #dcfce7; color: #166534; }
  &.badge-inactive { background: #fee2e2; color: #991b1b; }
}

.action-trigger { --padding-start: 0; --padding-end: 0; margin-right: -8px; }

.card-icon-holder {
  width: 76px; height: 76px; border-radius: 22px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
  .card-icon { font-size: 34px; }
}

.card-info {
  text-align: center; margin-bottom: 24px; flex-grow: 1;
  .card-name { margin: 0; font-size: 1.15rem; font-weight: 800; color: #0f172a; }
  .card-location { margin: 6px 0 0; font-size: 0.82rem; color: #64748b; display: flex; align-items: center; justify-content: center; gap: 4px; }
}

.card-footer {
  width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 0; border-radius: 14px;
  background: #f15a24; color: white; transition: all 0.2s ease;
  .footer-text { font-size: 0.85rem; font-weight: 700; }
  &.footer-inactive { background: #64748b; }
}

.premium-empty-state {
  display: flex; flex-direction: column; align-items: center; padding: 60px 24px; text-align: center;
}

.custom-fab-position { bottom: 80px !important; right: 20px !important; }
.premium-fab { --background: #f15a24; --box-shadow: 0 12px 24px rgba(241, 90, 36, 0.4); }

.shops-grid { padding-top: 10px; padding-bottom: 100px; }
</style>