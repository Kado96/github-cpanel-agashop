<!--
  * @file ShopHome.vue
  * @description Page/Composant pour Shop Home.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button @click="$router.push({name:'home'})" title="Changer de boutique">
            <ion-icon color="light" size="large" :icon="home"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Tableau de bord</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="shop-home-content">
      <!-- BANNIÈRE PREMIUM (Restaurée) -->
      <div v-if="!shop || shop.subscription_plan === 'FREE'" class="premium-banner" @click="$router.push({name: 'payment-methods'})">
        <div class="banner-icon-wrapper">
          <ion-icon :icon="cardOutline"></ion-icon>
        </div>
        <div class="banner-text">
          <span class="banner-title">Passez Premium !</span>
          <p>Débloquez toutes les fonctionnalités illimitées.</p>
        </div>
        <ion-icon :icon="addOutline" class="banner-arrow"></ion-icon>
      </div>

      <div class="welcome-header">
        <span class="shop-name-label">BOUTIQUE</span>
        <h2 class="fluid-shop-name">{{ shop?.name || 'AgaShop' }}</h2>
        <p v-if="!shop" class="no-shop-info">Aucune boutique active détectée.</p>
      </div>

      <ion-grid class="ion-no-padding ion-margin-horizontal">
        <ion-row>
          <ion-col v-for="menu in visibleMenus" :key="menu.name" size="6" size-md="4" class="menu-col">
            <div 
              class="menu-card" 
              :class="{ 'highlight-card': menu.cardColor === 'light', 'logout-card': menu.name === 'Deconnexion' || menu.name === 'Déconnexion' }"
              @click="goTo(menu)"
            >
              <div class="icon-wrapper" :style="{ backgroundColor: (menu.name === 'Deconnexion' || menu.name === 'Déconnexion') ? '#fee2e2' : '#f1f5f9' }">
                <ion-icon :icon="menu.icon" :color="(menu.name === 'Deconnexion' || menu.name === 'Déconnexion') ? 'danger' : menu.color"></ion-icon>
              </div>
              <span class="menu-label">{{ menu.name }}</span>
              <div v-if="menu.badge !== undefined" class="menu-badge" :class="{'badge-visible': menu.badge > 0}">
                {{ menu.badge }}
              </div>
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
  IonButtons,
  IonButton,
  IonIcon,
  IonContent,
  IonGrid,
  IonRow,
  IonCol,
  IonTitle,
  alertController
} from '@ionic/vue';

import {
  listOutline,
  home,
  moveOutline,
  cardOutline,
  statsChartOutline,
  cartOutline,
  addOutline,
  fastFoodOutline,
  logOut as logOutIcon,
  walletOutline,
  cashOutline,
  briefcaseOutline,
  personCircleOutline
} from 'ionicons/icons'
import { shopsService } from '@/services/api'

/**
 * Composant ShopHome
 * - Gère l'interface et la logique métier.
 */
export default {
  components:{
    IonPage,
    IonHeader,
    IonToolbar,
    IonButtons,
    IonButton,
    IonIcon,
    IonContent,
    IonGrid,
    IonRow,
    IonCol,
    IonTitle,
  },
  data(){
    return{
      menus:[
        {name:"Produits", route:"/products", routeName:"products", icon:listOutline, color: "tertiary"},
        {name:"Achats", route:"/supplies", routeName:"supplies", icon:cartOutline, color: "secondary"},
        {name:"Ventes", route:"/sales-list", routeName:"sales-list", icon:cardOutline, color: "success"},
        {name:"Contrôle", route:"/controls", routeName:"controls", icon:moveOutline, color: "warning"},
        {name:"Dépenses", route:"/expenses-list", routeName:"expenses-list", icon:cashOutline, color: "danger"},
        {name:"Bénéfices", route:"/profits-list", routeName:"profits-list", icon:cashOutline, color: "success"},
        {name:"Stats", route:"/stats", routeName:"stats", icon:statsChartOutline, color: "tertiary", cardColor:"light"},
        {name:"Paiements", route:"/payment-methods", routeName:"payment-methods", icon:walletOutline, color: "primary"},
        {name:"Catalogue", route:"/admin/basic-products", routeName:"manage-basic-products", icon:fastFoodOutline, color: "primary", requiresAdmin:true},
        {name:"Admin", route:"/admin", routeName:"admin-home", icon:personCircleOutline, color: "dark", requiresAdminOnly:true},
        {name:"Espace Agent", route:"/agent", routeName:"agent-home", icon:briefcaseOutline, color: "secondary", requiresAdmin:true},
        {name:"Déconnexion", route:"/logout", routeName:null, icon:logOutIcon, color: "danger"},
      ],
      shop: this.$store.state.shop,
      home,
      cardOutline,
      addOutline
    }
  },
  computed: {
    visibleMenus() {
      const user = this.active_user;
      const groups = user?.groups;
      let isAdmin = false;
      let isStrictAdmin = false;
      
      if (Array.isArray(groups) && groups.length) {
         if (typeof groups[0] === 'string') {
             isAdmin = this.active_user_is('admin', 'agent', 'superuser');
             isStrictAdmin = this.active_user_is('admin', 'superuser');
         } else {
             isAdmin = true;
             isStrictAdmin = true;
         }
      }
      
      return this.menus.filter(menu => {
        // Filtre Admin / Agent
        if (menu.requiresAdminOnly) {
          if (!isStrictAdmin) return false;
        }
        if (menu.requiresAdmin) {
          if (!isAdmin) return false;
        }

        return true;
      });
    },
    active_user() {
      return this.$store.state.user;
    }
  },
  async beforeMount(){
    this.$store.state.shop = this.getShopFromLocalStorage()
    
    if(!this.$store.state.shop){
      const user = this.$store.state.user;
      if (user && user.access) {
        // Détecter le rôle pour adapter les messages (pas de warning pour admin/agent)
        const groups = user.groups || [];
        const groupNames = Array.isArray(groups) 
          ? groups.map(g => typeof g === 'string' ? g : (g.name || ''))
          : [];
        const isAdminOrAgent = groupNames.includes('admin') || groupNames.includes('superuser') || groupNames.includes('agent');

        try {
          const res = await shopsService.getShops();
          const data = res.data;
          const shops = data.results || (Array.isArray(data) ? data : []);
          
          if (shops.length > 0) {
            this.$store.state.shop = shops[0];
            localStorage.setItem('current_shop', JSON.stringify(shops[0]));
            this.shop = this.$store.state.shop;
            console.log("[ShopHome] Boutique récupérée et activée:", this.shop.name);
          } else if (!isAdminOrAgent) {
            // Redirection vers l'accueil (liste/création) si aucune boutique n'est trouvée
            console.log("[ShopHome] Aucune boutique trouvée. Redirection vers la liste...");
            this.$router.push("/");
          }
        } catch (error) {
          console.error("[ShopHome] Erreur récupération boutique:", error);
        }
      } else {
        this.$store.state.user = null
        this.$router.push("/login")
      }
    }
    this.shop = this.getShopFromLocalStorage()
    this.checkCurrentShop()
  },

  ionViewWillEnter() {
    // Initialiser l'aide contextuelle pour le menu principal
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Menu Principal AgaShop',
      description: 'Bienvenue dans votre espace de gestion. Ce menu est votre point de départ pour toutes les opérations de votre boutique.',
      elements: [
        { type: 'Navigation', label: 'Produits', desc: 'Gérez votre base de données produits (ajout, modification, prix).' },
        { type: 'Action', label: 'Achats', desc: 'Enregistrez les nouveaux arrivages de marchandise pour augmenter votre stock.' },
        { type: 'Commerce', label: 'Ventes', desc: 'Accédez au terminal de vente pour encaisser vos clients.' },
        { type: 'Analyse', label: 'Stats', desc: 'Consultez vos indicateurs de performance et votre rentabilité (Dashboard).' },
        { type: 'Finance', label: 'Dépenses', desc: 'Notez vos frais (loyer, transport) pour calculer votre bénéfice net.' }
      ],
      faq: [
        { question: 'Par quoi dois-je commencer ?', answer: 'Si c\'est votre première utilisation, commencez par créer vos "Produits", puis enregistrez un "Achat" pour avoir du stock à vendre.' },
        { question: 'Comment voir mes gains ?', answer: 'Cliquez sur le bouton "Stats" pour voir votre bénéfice du jour et vos graphiques de performance.' }
      ]
    });
  },
  methods:{
    goTo(menu){
      if(menu.name === "Déconnexion" || menu.name === "Deconnexion"){
        this.exit();
        return;
      }
      if(menu.routeName){
        this.$router.push({ name: menu.routeName });
      } else {
        this.$router.push(menu.route);
      }
    },
    async exit() {
      const alert = await alertController
        .create({
          header: 'Déconnexion',
          message: 'Voulez-vous vous déconnecter ?',
          buttons: [
            { text: 'Non', role: 'cancel' },
            {
              text: 'Oui',
              handler:()=>{
                this.$store.state.user = null
                this.$store.state.shop = null
                localStorage.removeItem('user')
                localStorage.removeItem('current_shop')
                window.location = "/login"
              }
            }
          ],
        });
      await alert.present()
    }
  },
}
</script>

<style lang="scss" scoped>
.shop-home-content {
  --background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
  background: linear-gradient(180deg, #f5f0ff 0%, #e8d5ff 50%, #d4b3ff 100%);
}

.welcome-header {
  padding: 24px 20px 16px 20px;
  text-align: center;

  .shop-name-label {
    font-size: 0.8rem;
    color: #475569;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    display: block;
    margin-bottom: 4px;
  }

  .fluid-shop-name {
    font-size: clamp(1.5rem, 6vw, 2.2rem);
    font-weight: 800;
    color: #0f172a;
    margin: 0;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }
}

.premium-banner {
  margin: 16px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 20px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 10px 15px -3px rgba(217, 119, 6, 0.3);
  color: white;
  animation: fadeInUp 0.5s ease-out;
  
  .banner-icon-wrapper {
    width: 48px;
    height: 48px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    ion-icon {
      font-size: 24px;
    }
  }
  
  .banner-text {
    flex: 1;
    .banner-title {
      font-size: 1.1rem;
      font-weight: 800;
      display: block;
      margin-bottom: 2px;
    }
    p {
      margin: 0;
      font-size: 0.85rem;
      opacity: 0.9;
      line-height: 1.2;
    }
  }

  .banner-arrow {
    font-size: 20px;
    opacity: 0.8;
  }
}

.menu-col {
  padding: 8px;
  animation: fadeInUp 0.5s ease-out both;

  @for $i from 1 through 12 {
    &:nth-child(#{$i}) {
      animation-delay: #{$i * 0.05}s;
    }
  }
}

.menu-card {
  background: white;
  border-radius: 20px;
  padding: 24px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  height: 100%;

  &:active {
    transform: scale(0.95);
    background: #f8fafc;
  }

  .icon-wrapper {
    width: 60px;
    height: 60px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 14px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
    
    ion-icon {
      font-size: 30px;
    }
  }

  .menu-label {
    font-size: clamp(0.9rem, 2.5vw, 1rem);
    font-weight: 800;
    color: #1e293b;
    line-height: 1.1;
    letter-spacing: -0.01em;
  }

  .menu-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: var(--ion-color-secondary);
    color: white;
    font-size: 0.75rem;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    opacity: 0;
    transform: scale(0.5);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    
    &.badge-visible {
      opacity: 1;
      transform: scale(1);
    }
  }
}

.highlight-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(8px);
  border: 1px solid var(--ion-color-primary);
}

.logout-card {
  .menu-label {
    color: var(--ion-color-danger);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (min-width: 768px) {
  .menu-card {
    padding: 40px 24px;
    .icon-wrapper {
      width: 72px;
      height: 72px;
      ion-icon {
        font-size: 36px;
      }
    }
    .menu-label {
      font-size: 1.2rem;
    }
  }
}
</style>
