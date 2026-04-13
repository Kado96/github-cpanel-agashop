<!--
  * @file AdminHome.vue
  * @description Page/Composant pour Admin Home.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button @click="$router.push({name:'home'})">
            <ion-icon color="light" size="large" :icon="home"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Tableau de bord Admin</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="admin-content">
      <div class="welcome-section">
        <h2>Bienvenue, Administrateur</h2>
        <p>Gérez votre plateforme et vos boutiques</p>
      </div>

      <ion-grid class="ion-no-padding ion-margin-horizontal">
        <ion-row>
          <ion-col v-for="menu in visibleMenus" :key="menu.name" size="6" size-md="4" class="menu-col">
            <div 
              class="menu-card" 
              :class="{ 'logout-card': menu.name === 'Deconnexion' }"
              @click="goTo(menu)"
            >
              <div class="icon-wrapper" :style="{ backgroundColor: menu.name === 'Deconnexion' ? '#fee2e2' : '#f1f5f9' }">
                <ion-icon :icon="menu.icon" :color="menu.name === 'Deconnexion' ? 'danger' : menu.color"></ion-icon>
              </div>
              <span class="menu-label">{{ menu.name }}</span>
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
  home,
  fastFoodOutline,
  logOut as logOutIcon,
  peopleOutline,
  storefrontOutline,
  settingsOutline
} from 'ionicons/icons'

/**
 * Composant AdminHome
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
        {name:"Catalogue", route:"/admin/basic-products", icon:fastFoodOutline, color: "primary"},
        {name:"Agents", route:"/admin/users", icon:peopleOutline, color: "secondary"},
        {name:"Boutiques", route:"/admin/shops", icon:storefrontOutline, color: "tertiary"},
        {name:"Paramètres", route:"/admin/settings", icon:settingsOutline, color: "success"},
        {name:"Déconnexion", route:"/logout", icon:logOutIcon, color: "danger"},
      ],
      home,
    }
  },
  computed: {
    visibleMenus() {
      return this.menus;
    }
  },
  beforeMount(){
    const user = this.active_user;
    const groups = user?.groups;
    const isAdmin = Array.isArray(groups) && groups.length && (
      typeof groups[0] === 'string' ? this.active_user_is('admin', 'agent', 'superuser') : true
    );
    
    if (!isAdmin) {
      this.$router.push("/login");
    }
  },
  ionViewWillEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Tableau de Bord Administrateur',
      description: 'Bienvenue dans la tour de contrôle. Vous avez ici la main sur les fondations de la plateforme AgaShop : Catalogue Maître, Comptes et Boutiques.',
      elements: [
        { type: 'Système', label: 'Boutiques', desc: 'Pilotez l\'ensemble des points de vente, surveillez les essais et gérez les abonnements.' },
        { type: 'Sécurité', label: 'Agents', desc: 'Gérez la liste des agents et des administrateurs ayant accès au système.' },
        { type: 'Référence', label: 'Catalogue', desc: 'Modifiez les produits globaux qui servent de base à tous les nouveaux inventaires.' }
      ],
      faq: [
        { question: 'Comment créer un agent ?', answer: 'Allez dans "Agents" et utilisez le bouton Ajouter. Un agent peut voir ses propres boutiques rattachées.' },
        { question: 'Où changer mon mot de passe ?', answer: 'Accédez aux "Paramètres" pour mettre à jour vos informations de compte.' }
      ]
    });
  },
  methods:{
    goTo(menu){
      if(menu.name === "Déconnexion" || menu.name === "Deconnexion")
        this.exit()
      else
        this.$router.push(menu.route)
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
                localStorage.removeItem('user')
                localStorage.removeItem('current_shop')
                window.location = "/login"
              }
            }
          ],
        });
      await alert.present()
    },
  },
}
</script>

<style lang="scss" scoped>
.admin-content {
  --background: #f1f5f9; // Arrière-plan un peu plus sombre pour faire ressortir les cartes
}

.welcome-section {
  padding: 30px 20px 20px 20px;
  h2 {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
    letter-spacing: -0.02em;
  }
  p {
    font-size: 1rem;
    color: #475569;
    margin: 6px 0 0 0;
    font-weight: 500;
  }
}

.menu-col {
  padding: 10px;
}

.menu-card {
  background: white;
  border-radius: 20px; // Bordures plus jolies et arrondies
  padding: 24px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  
  // Bordure visible et propre
  border: 1.5px solid #e2e8f0;
  
  // Ombre plus qualitative
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
  
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;

  &:active {
    transform: translateY(2px);
    background: #f8fafc;
    border-color: var(--ion-color-primary);
  }

  .icon-wrapper {
    width: 60px;
    height: 60px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 14px;
    box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.05);
    
    ion-icon {
      font-size: 30px;
    }
  }

  .menu-label {
    font-size: 1rem;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.2;
    letter-spacing: -0.01em;
  }
}

.logout-card {
  border-color: #fee2e2;
  .menu-label {
    color: var(--ion-color-danger);
  }
  &:active {
    border-color: var(--ion-color-danger);
  }
}

@media (min-width: 768px) {
  .menu-card {
    padding: 38px 24px;
    .icon-wrapper {
      width: 68px;
      height: 68px;
      ion-icon {
        font-size: 34px;
      }
    }
    .menu-label {
      font-size: 1.15rem;
    }
  }
}
</style>
