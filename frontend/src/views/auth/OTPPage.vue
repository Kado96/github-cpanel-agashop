<!--
  * @file OTPPage.vue
  * @description Page de validation OTP (One-Time Password).
  * L'utilisateur insère le code à 5 chiffres reçu par email pour valider son compte.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button id="otp-back-btn" @click="$router.go(-1)">
            <ion-icon color="light" size="large" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Vérification OTP</span>
          </div>
        </ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content fullscreen="true">
    </ion-content>
    <ion-footer class="ion-no-border">
    
  <ion-list lines="none">
    <ion-list-header class="ion-margin">
      <ion-label>Valider votre Compte</ion-label>
    </ion-list-header>

    <ion-item class="ion-margin" lines="none">
      <ion-label size="small">
        Veuillez ecrire le code envoyé à l'adresse email  <span class="font-italic">{{ otp_user?maskValue(otp_user.email):'******' }} </span>
        <ion-row class="ion-padding-top ion-text-center">
          <ion-col v-for="otp,i in otpString">
            <ion-input 
              autofocus="true"
              required
              maxlength="1"
              :id="'otp-input-'+i"
              :name="'otp_digit_'+i"
              type="tel"
              inputmode="numeric"
              v-model="otpString[i]"
              @keyup="handlerOtp($event, 'otp-input-'+(i-1), 'otp-input-'+(i+1), i)">
            </ion-input>
          </ion-col>
        </ion-row>`
        <ion-text class="error" v-if="errors.otp.empty" color="danger">
            * OTP incomplet
        </ion-text>
        <ion-button
            id="otp-validate-btn"
            color="primary"
            expand="block"
            :disabled="loading"
            @click="validateOtp"
            >
            <ion-spinner v-if="loading" slot="start"></ion-spinner>
            <ion-text >Valider</ion-text>
        </ion-button>
        <ion-text class="error"  color="danger">
           <a id="otp-resend-link" @click="resendOtp">Renvoyer le code</a>
        </ion-text>
      </ion-label>

    </ion-item>
  </ion-list>

</ion-footer>
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
    IonCol,
    IonListHeader,
    IonItem,
    IonItemGroup,
    IonInput,
    IonText,
    IonButton,
    IonSpinner,
    toastController
} from '@ionic/vue';

import {
    arrowBackOutline,
} from 'ionicons/icons'
import { accountsService } from '../../services/api'

/**
 * Composant OTPPage
 * - Gère la vue des 5 cases de saisie OTP.
 * - Auto-focus vers la case suivante.
 * - Appel API pour vérification et redirection vers Home/Dashboard.
 */
export default {
    components:{
        IonPage,
        IonContent,
        IonGrid,
        IonLabel,
        IonFooter,
        IonRow,
        IonCol,
        IonFab,
        IonFabButton,
        IonIcon,
        IonList,
        IonListHeader,
        IonItem,
        IonItemGroup,
        IonInput,
        IonText,
        IonButton,
        IonSpinner,
    },
    data(){
        return{
            otpString:["","","","",""],
            arrowBackOutline,
            loading:false,
            otp_user:null,
            errors:{
                otp:{
                    empty:false,
                    custom:false
                }
            }
        }
    },
    mounted(){
        var otp_user = localStorage.getItem('otp_user');
        if(otp_user) {
            this.$store.state.otp_user = JSON.parse(otp_user);
            this.otp_user = this.$store.state.otp_user
        }else{
            localStorage.removeItem('otp_user')
            this.$router.push("/register")
        }
    },
    methods:{
        handlerOtp(event, prev, next, index) {

            let nextEl = document.getElementById(next)
            let prevEl = document.getElementById(prev)
            const pattern = /[0-9]/;
            let inputChar = String.fromCharCode(event.which ? event.which : event.keyCode);
            if(event.keyCode==8){
                if(prevEl)
                    prevEl.setFocus();
            }
            if(!pattern.test(inputChar)) {
                event.preventDefault();
                this.otpString[index] = '';
                return;
            }
            let value = event.target.value;
            if(value.length > 1) {
                this.otpString[index] = value;
            }
            if(value.length < 1 && prevEl) {
                prevEl.setFocus();
            }
            else if(nextEl && value.length > 0) {
                nextEl.setFocus();
            }
            else {
                if(nextEl == '') {
                    this.validateOtp();
                }
                else return 0;
            }
        },
        validateOtp(){
            this.errors.otp.empty=false
            this.loading=true
            if(this.otpString.join("").length<5){
                this.errors.otp.empty=true
                this.loading=false
                return
            }
            accountsService.verifyOtp(this.otpString.join(""))
            .then((res)=>{
                console.log(res)
                this.loading=false
                // Sauvegarder l'utilisateur dans le store et localStorage (incl. account_id)
                this.$store.state.user = res.data
                if (res.data.account && res.data.account.id != null) {
                  this.$store.state.user.account_id = res.data.account.id
                }
                this.$store.state.shop = res.data.shop
                localStorage.setItem("user", JSON.stringify(this.$store.state.user))
                if (res.data.shop) {
                  localStorage.setItem("current_shop", JSON.stringify(res.data.shop))
                }
                localStorage.removeItem('otp_user')
                
                // Rediriger selon le rôle de l'utilisateur
                const groups = res.data.groups || []
                
                // Normaliser les groupes : extraire les noms si ce sont des objets
                let groupNames = [];
                if (Array.isArray(groups) && groups.length > 0) {
                  if (typeof groups[0] === 'string') {
                    groupNames = groups;
                  } else if (typeof groups[0] === 'object' && groups[0] !== null) {
                    groupNames = groups.map(g => g.name || g).filter(Boolean);
                  }
                }
                
                console.log('[OTPPage] Groups reçus:', groups, 'GroupNames normalisés:', groupNames);
                
                const isAdmin = groupNames.includes('admin') || groupNames.includes('superuser')
                const isAgent = groupNames.includes('agent')
                
                if (isAdmin) {
                  // Admin ou superuser → page admin
                  console.log('[OTPPage] Redirection vers /admin');
                  this.$router.push("/admin")
                } else if (isAgent) {
                  // Agent → page agent
                  console.log('[OTPPage] Redirection vers /agent');
                  this.$router.push("/agent")
                } else {
                  // Utilisateur normal → page boutique
                  console.log('[OTPPage] Redirection vers / (utilisateur normal)');
                  this.$router.push("/")
                }
            }).catch((err)=>{
                this.loading=false
                this.errorOrRefresh(err, () => this.validateOtp())
            })
        },
        resendOtp(){
            accountsService.resendOtp()
            .then(()=>{
                this.showTostMsg("Code OTP renvoyé avec succès","success",5000)
            }).catch((err)=>{
                this.errorOrRefresh(err, () => this.resendOtp())
            })
        },
        
    }
}
</script>

<style lang="scss" scoped>
ion-content {
    --background: var(--ion-color-primary);
}

.font-italic {
    font-style: italic;
}

ion-footer {
    height: 88%;

    ion-list {
        height: 100%;
        border-radius: 20px 20px 0 0;
        ion-list-header {
            ion-label {
                font-weight: bold;
                font-size: 1.8em;
            }
        }
        ion-item {
            ion-label {
                font-size: 1em;
                overflow: visible;
                ion-row {
                    ion-col {
                        ion-input {
                            font-size: 1.5em;
                            --background: var(--ion-color-light);
                            display: inline-block;
                            width: 6.5vh;
                            height: 6.5vh;
                            border-radius: 5px;
                        }
                        
                        .marginLeft {
                            margin-left: 3vh;
                        }
                    }
                }
                .error {
                    font-size: 0.75em !important;
                }
                ion-button{
                    margin-top: 2em;
                    height: 3em;
                    ion-text{
                        font-size: 1.5em;
                        color: white;
                        font-weight: bold;
                    }
                    ion-spinner{
                        margin-right: 0.9em;
                    }
                    }
            }
        }
    }

}
</style>