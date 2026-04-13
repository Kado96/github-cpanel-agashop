<!--
  * @file ShopsList.vue
  * @description Page/Composant pour Shops List.
  * @author Kora Agency
-->
<template>
    <ion-header class="ion-no-border">
    <ion-toolbar  color="primary">
      <ion-title>AgaShop</ion-title>
        <ion-buttons slot="end">
          <ion-button color="dark" fill="clear" routerLink="cart">
            <ion-icon :icon="cartOutline" slot="icon-only"></ion-icon>
  
            <ion-badge color="light">
              <ion-text color="tertiary">55</ion-text>
            </ion-badge>
          </ion-button>
        </ion-buttons>
    </ion-toolbar>
  </ion-header>
  
  <ion-content>
    <ion-item lines="none" class="ion-margin-vertical">
      <ion-label>
        Hello
        <p>
          <ion-text color="dark"> Coding Technyks </ion-text>
        </p>
      </ion-label>
  
      <ion-thumbnail slot="end">
        <img src="../assets/avatar.jpg" />
      </ion-thumbnail>
    </ion-item>
  
    <ion-list-header> Your Insights </ion-list-header>
  
    <ion-row class="ion-margin">
      <ion-col v-for="menu in menus" size="6" class="ion-text-center">
        <ion-card color="light" >
          <ion-thumbnail :style="'background-color:'+menu.bgColor">
            <ion-icon :icon="menu.icon" :color="menu.color"></ion-icon>
          </ion-thumbnail>
  
          <ion-label>{{menu.name}}</ion-label>
        </ion-card>
      </ion-col>
  
    </ion-row>
  
    <!-- <ion-toast
      [isOpen]="isToast"
      [message]="toastData?.message"
      [position]="'bottom'"
      [color]="toastData?.color"
      [duration]="3000"
      (didDismiss)="isToast = false"
    ></ion-toast> -->
  </ion-content>
  </template>
  
  <script>
  import {
    IonHeader,
    IonToolbar,
    IonButtons,
    IonButton,
    IonIcon,
    IonBadge,
    IonText,
    IonContent,
    IonItem,
    IonLabel,
    IonThumbnail,
    IonListHeader,
    IonRow,
    IonCol,
    IonCard,
    IonTitle
  } from '@ionic/vue';
  
  import {
    listOutline,
    moveOutline,
    cardOutline,
    statsChartOutline,
    cartOutline
  } from 'ionicons/icons'
  
  /**
 * Composant ShopsList
 * - Gère l'interface et la logique métier.
 */
export default {
    components:{
      IonHeader,
      IonToolbar,
      IonButtons,
      IonButton,
      IonIcon,
      IonBadge,
      IonText,
      IonContent,
      IonItem,
      IonLabel,
      IonThumbnail,
      IonListHeader,
      IonRow,
      IonCol,
      IonCard
    },
    data(){
      return{
        menus:[
          {name:"Ibidandazwa",route:"/products",icon:listOutline,color: "tertiary" , bgColor:"rgba(240,94,112, 0.2)"},
          {name:"Gukontrola",route:"/controls",icon:moveOutline,color: "warning" , bgColor:"rgba(255,152,0, 0.2)"},
          {name:"Ivyandandajwe",route:"/sales",icon:cardOutline,color: "success" , bgColor:"rgba(76,175,80, 0.2)"},
          {name:"Ibitigiri",route:"/statistics",icon:statsChartOutline,color: "secondary" , bgColor:"rgba(94,155,240, 0.2)"},
        ],
        cartOutline
      }
    }
  }
  </script>
  
  <style lang="scss">
  ion-header {
    ion-toolbar {
      --background: white;
      ion-badge {
        position: absolute;
        top: 0;
        right: 0;
        border-radius: 50%;
        height: 1rem;
        width: 1rem;
        margin: 0 -0.3rem 0 0;
        display: flex;
        align-items: center;
        justify-content: center;
        ion-text {
          font-size: 0.6rem;
          font-weight: bold;
        }
      }
    }
  }
  
  ion-item {
    ion-label {
      font-size: 1.4rem;
      font-weight: bold;
      p {
        margin-top: 5px;
        font-size: 0.9rem;
        font-weight: normal;
      }
    }
    ion-thumbnail {
      img {
        border-radius: 10px;
      }
    }
  }
  
  ion-list-header {
    font-size: 1.1rem;
    font-weight: normal;
  }
  
  ion-card {
    box-shadow: none;
    margin: 10px 5px;
    height: 15vh;
    flex-direction: column;
    ion-thumbnail {
      border-radius: 10px;
      width: 3rem;
      height: 3rem;
      margin-bottom: 1.3vh;
      ion-icon {
        font-size: 2rem;
      }
    }
    ion-label {
      font-size: 1rem;
      font-weight: 500;
    }
  }
  
  ion-card, ion-thumbnail {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  </style>
  
  