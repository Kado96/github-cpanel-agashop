<!--
  * @file AgentHome.vue
  * @description Page/Composant pour Agent Home.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button @click="$router.push({name:'home'})">
            <ion-icon color="light" size="large" :icon="home"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Tableau de bord Agent</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="agent-content">
      <div class="welcome-section">
        <h2>Espace Agent</h2>
        <p>Gérez les boutiques et le catalogue</p>
      </div>

      <ion-grid class="ion-no-padding ion-margin-horizontal">
        <ion-row>
          <ion-col v-for="menu in visibleMenus" :key="menu.name" size="6" size-md="4" class="menu-col">
            <div 
              class="menu-card" 
              :class="{ 'logout-card': menu.name === 'Deconnexion' || menu.name === 'Déconnexion' }"
              @click="goTo(menu)"
            >
              <div class="icon-wrapper" :style="{ backgroundColor: (menu.name === 'Deconnexion' || menu.name === 'Déconnexion') ? '#fee2e2' : '#fff7ed' }">
                <ion-icon :icon="menu.icon" :color="(menu.name === 'Deconnexion' || menu.name === 'Déconnexion') ? 'danger' : 'secondary'"></ion-icon>
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
  storefrontOutline
} from 'ionicons/icons'

/**
 * Composant AgentHome
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
        {name:"Catalogue", route:"/admin/basic-products", icon:fastFoodOutline, color: "secondary"},
        {name:"Boutiques", route:"/admin/shops", icon:storefrontOutline, color: "tertiary"},
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
    const groups = user?.groups || [];
    
    let groupNames = [];
    if (Array.isArray(groups) && groups.length > 0) {
      if (typeof groups[0] === 'string') {
        groupNames = groups;
      } else if (typeof groups[0] === 'object' && groups[0] !== null) {
        groupNames = groups.map(g => g.name || g).filter(Boolean);
      }
    }
    
    const isAgent = groupNames.includes('agent') || groupNames.includes('admin') || groupNames.includes('superuser');
    
    if (!isAgent) {
      console.warn('[AgentHome] Utilisateur non autorisé. Groups:', groupNames, 'User:', user);
      this.$router.push("/login");
    }
  },
  ionViewWillEnter() {
    this.$store.commit('SET_HELP_CONTEXT', {
      title: 'Espace Agent de Terrain',
      description: 'Votre mission est d\'accompagner les commerçants. Vous gérez les boutiques de votre secteur et le catalogue de produits de référence.',
      elements: [
        { type: 'Gestion', label: 'Boutiques', desc: 'Inscrivez de nouveaux commerçants ou modifiez les informations des boutiques existantes.' },
        { type: 'Référence', label: 'Catalogue', desc: 'Consultez la liste des produits universels pour aider vos clients à démarrer.' }
      ],
      faq: [
        { question: 'Comment aider un nouveau client ?', answer: 'Créez sa boutique, puis aidez-le à ajouter ses premiers articles depuis le catalogue.' },
        { question: 'Puis-je voir les bénéfices des clients ?', answer: 'Non, les données financières sont privées. Vous ne gérez que la structure et les accès.' }
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
.agent-content {
  --background: #fdf2f2; // Un peu plus sombre/chaleureux
}

.welcome-section {
  padding: 30px 20px 20px 20px;
  h2 {
    font-size: 1.6rem;
    font-weight: 800;
    color: #431407;
    margin: 0;
    letter-spacing: -0.02em;
  }
  p {
    font-size: 1rem;
    color: #9a3412;
    margin: 6px 0 0 0;
    font-weight: 500;
  }
}

.menu-col {
  padding: 10px;
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
  
  // Bordure visible et harmonieuse
  border: 1.5px solid #fed7aa;
  
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;

  &:active {
    transform: translateY(2px);
    background: #fff7ed;
    border-color: var(--ion-color-secondary);
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
    color: #7c2d12;
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
