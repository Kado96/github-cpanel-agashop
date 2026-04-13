<!--
  * @file AuthLayout.vue
  * @description Page/Composant pour Auth Layout.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-content fullscreen="true">
        <div class="background">
            <div class="circle-top top-left big"></div>
            <div class="circle-top top-left small"></div>
            <div class="circle-bottom bottom-right big"></div>
            <div class="circle-bottom bottom-right small"></div>
        </div>
        <div class="container" >
            <slot></slot>
        </div>
    </ion-content>
  </ion-page>
</template>

<script>
import {
    IonPage,
    IonContent,
    IonGrid,
    IonLabel,
    IonFooter,
    IonRow,
    IonFab,
    IonFabButton,
    IonIcon,
    IonList,
    IonListHeader,
    IonItem,
    IonItemGroup,
    IonInput,
    IonText,
    IonSpinner,
    IonButton
} from '@ionic/vue';

import {
    eyeOutline,
    eyeOffOutline,
    arrowForwardOutline,
    checkbox
} from 'ionicons/icons'
import { authService } from '../../services/api'

/**
 * Composant AuthLayout
 * - Gère l'interface et la logique métier.
 */
export default {
  data(){
    return{
      eyeOutline,
      eyeOffOutline, 
      arrowForwardOutline,  
      type:false,
      loading:false,
      login:{
          username:"",
          password:""
      },
      errors:{
        username:false,
        password:false
      }
    }
  },
  mounted(){
        if(this.$store.state.user)
            this.$router.push("/")
    },
  components:{
    IonPage,
    IonContent,
    IonGrid,
    IonLabel,
    IonFooter,
    IonRow,
    IonFab,
    IonFabButton,
    IonIcon,
    IonList,
    IonListHeader,
    IonItem,
    IonItemGroup,
    IonInput,
    IonText,
    IonSpinner,
    IonButton
  },
  methods:{
    changeType(){
      this.type=!this.type
    },
    initErros(){
      this.errors.password=false
      this.errors.username=false
    },
    validateInputs(){
      this.initErros()
      if(this.login.username.trim()==""){
        this.errors.username=true
        return false
      }
      if(this.login.password.trim()=="" || this.login.password.trim().length<4){
        this.errors.password=true
        return false
      }
      return true
    },
    performLogin(){
      if(this.validateInputs()){
        this.loading=true
        authService.login(this.login.username, this.login.password)
        .then((res)=>{
            this.loading=false
            this.$store.state.user = res.data
            this.$router.push("/")
        }).catch((err)=>{
            this.loading=false
            this.errorOrRefresh(err, () => this.performLogin())
        })
      }
      
    }
  }
}
</script>

<style lang="scss" scoped>
ion-content{
    position:relative;
}
/* Cercles de décoration */
.background {
    position: absolute;
    width: 100vw;
    height:100vh;
    overflow:hidden;
    z-index:-3;
}

.circle-top {
    position: absolute;
    border-radius: 50%;
    background: rgba(0,0,0, 0.3);
    background: var(--ion-color-primary);
    box-shadow: 4px 4px 15px rgba(0,0,0, 0.7);
}

.circle-bottom {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    background: var(--ion-color-primary);
    box-shadow: -4px -4px 15px rgba(0,0,0, 0.7);
}

.big {
    width: 200px;
    height: 200px;
}

.small {
    width: 200px;
    height: 200px;
}

.top-left.big {
    z-index:2;
    top: -100px;
    left: -35px;
}

.top-left.small {
    z-index:1;
    top: 0px;
    left: -100px;
}

.bottom-right.big {
    z-index:2;
    bottom: -120px;
    right: -30px;
}

.bottom-right.small {
    z-index:1;
    bottom: -35px;
    right: -100px;
}

.container {
  display: flex;
  width: 100vw;
  align-items: center;
  justify-content: center; /* Added for better ergonomics on large screens */
  min-height: 100vh;
  flex-wrap: wrap;
}

</style>