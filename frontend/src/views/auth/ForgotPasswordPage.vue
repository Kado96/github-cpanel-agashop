<!--
  * @file ForgotPasswordPage.vue
  * @description Page/Composant pour Forgot Password Page.
  * @author Kora Agency
-->
<template>
    <AuthLayout>
        <div class="wrapper">
             <div class="header-title">
                <p>Mot de passe oublié</p>
            </div>
            <div class="login-container">
              <div class="login-form">
                <div class="form-inputs">
                  <div class="form-group">
                      <ion-icon color="dark" :icon="mail"></ion-icon>
                      <input 
                        id="forgot-email"
                        name="email"
                        type="email" 
                        v-model="email" 
                        autofocus='True' 
                        placeholder="Votre adresse e-mail"
                        autocomplete="email"
                      >
                  </div>
                </div>
                <div class="circular-button" 
                  :class="{disabledDiv:spinner}" 
                  @click="performResetPassword"
                >
                  <ion-spinner
                      class="spinner"
                      v-if="spinner"
                      name="circular"
                    ></ion-spinner>
                  <ion-icon v-if="!spinner" color="dark" :icon="arrowForwardOutline" ></ion-icon>
                </div>
              </div>
              
              <div class="info-message">
                <p>Un nouveau mot de passe sera envoyé à votre adresse e-mail.</p>
              </div>

              <div class="footer-actions">
                  <ion-button
                    expand="block"
                    color="primary"
                    router-link="/login"
                    class="main-nav-btn"
                  >SE CONNECTER
                  </ion-button>
              </div>
            </div>
        </div>
    </AuthLayout>
</template>

<script>
import AuthLayout from "./AuthLayout.vue"
import {
  IonSpinner,IonButton,IonIcon
} from '@ionic/vue';
import {
  arrowForwardOutline,
  mail
} from 'ionicons/icons'
import { authService } from '../../services/api'

/**
 * Composant ForgotPasswordPage
 * - Gère l'interface et la logique métier.
 */
export default {
  data(){
    return {
      email:"",
      spinner:false,
      arrowForwardOutline,
      mail
    }
  },
  components: {
    IonSpinner,
    IonButton,
    AuthLayout,
    IonIcon,
  },
  methods:{
      performResetPassword(){
        if(this.email.trim()==""){
          this.showTostMsg("Veuillez remplir votre adresse e-mail","danger",5000)
          return       
        }
        if(!this.email.trim().includes("@")){
          this.showTostMsg("Veuillez remplir un email valide !","danger",5000)
          return      
        }
        else{
          this.spinner=true
          authService.resetPassword(this.email.trim())
          .then((res)=>{
          this.spinner=false
          const statusMsg = res.data?.status || "Un nouveau mot de passe a été envoyé à votre adresse e-mail."
          const emailSent = res.data?.email_sent

          // Si l'API indique explicitement que l'e-mail n'a pas pu être envoyé,
          // on informe clairement l'utilisateur sans afficher un succès trompeur.
          if (emailSent === false) {
            this.showTostMsg(
              statusMsg ||
              "Le mot de passe a été réinitialisé, mais l'envoi de l'e-mail a échoué. Contactez l'administrateur pour récupérer le nouveau mot de passe.",
              "warning",
              10000
            )
          } else {
            this.showTostMsg(statusMsg, "success", 7000)
            this.$router.push({ name: "forgot-password-success" })
          }
          }).catch((err)=>{
            this.spinner=false
            // Gestion spécifique des erreurs de réinitialisation
            if (err.response) {
              const status = err.response.status
              const data = err.response.data || {}
              
              if (status === 403) {
                // Email incorrect ou compte non trouvé
                this.showTostMsg(
                  "Email incorrect ou aucun compte trouvé avec cet email (utilisateur, agent ou administrateur). Vérifiez votre adresse email ou contactez l'administrateur.",
                  'danger',
                  7000
                )
              } else if (status === 503 || status === 500) {
                // Problème d'envoi d'email (SMTP non configuré en local souvent)
                const errorMsg = data.status || data.detail || data.message || ''
                let userMessage = "Impossible d'envoyer l'email de réinitialisation pour le moment."
                
                if (errorMsg.toLowerCase().includes('smtp') || 
                    errorMsg.toLowerCase().includes('email') ||
                    errorMsg.toLowerCase().includes('envoi')) {
                  userMessage += "\n\nLe serveur d'email n'est peut-être pas configuré. "
                  userMessage += "En développement local, vérifiez les logs du serveur backend (terminal où Django tourne) pour obtenir le nouveau mot de passe généré. "
                  userMessage += "Le mot de passe est affiché même si l'email ne peut pas être envoyé."
                  userMessage += "\n\nSi vous êtes agent ou administrateur, contactez le support technique pour obtenir votre nouveau mot de passe."
                } else {
                  userMessage += "\n\nVérifiez les logs du serveur backend (terminal Django) ou contactez l'administrateur."
                  userMessage += "\n\nPour les agents et administrateurs : le nouveau mot de passe est généré et affiché dans les logs même si l'email échoue."
                }
                
                this.showTostMsg(userMessage, 'warning', 10000)
                
                // Afficher aussi dans la console pour le développeur
                console.warn('[PASSWORD RESET] Erreur serveur:', {
                  status,
                  data,
                  message: 'En développement local, vérifiez les logs du backend Django pour voir le nouveau mot de passe généré.'
                })
              } else {
                // Autres erreurs
                this.errorOrRefresh(err, () => this.performResetPassword())
              }
            } else {
              // Erreur réseau
              this.showTostMsg(
                "Impossible de se connecter au serveur. Vérifiez votre connexion et réessayez.",
                'danger',
                5000
              )
            }
          })
        }
      },
    }
    
};
</script>

<style scoped>
.wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 80vh;
    padding: 20px;
    width: 100%;
}

.header-title {
  margin-bottom: 30px;
  text-align: center;
}

.header-title > p {
  font-size: clamp(30px, 8vw, 50px);
  font-weight: bold;
  margin: 0;
}

.login-container {
    width: 100%;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.login-form {
    width: 100%;
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    position: relative;
    margin-bottom: 20px;
}

.form-inputs {
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
}

.form-group {
    width: 100%;
    position: relative;
    display: flex;
    align-items: center;
    background: #f5f5f5;
    margin-bottom: 2px;
}

.form-group ion-icon {
    position: absolute;
    left: 15px;
    font-size: 24px;
    z-index: 2;
}

.form-group input {
    width: 100%;
    height: 60px;
    border: none;
    background: transparent;
    font-size: 18px;
    padding: 10px 15px 10px 50px;
    outline: none;
}

/* Border radius logic for the group */
.form-group:first-child {
    border-radius: 10px;
}

.circular-button {
    position: absolute;
    bottom: -30px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: var(--ion-color-primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s, background 0.2s;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    z-index: 10;
}

.circular-button:active {
    transform: scale(0.9);
}

.circular-button ion-icon {
    font-size: 30px;
    color: black;
}

.disabledDiv {
    opacity: 0.7;
    pointer-events: none;
}

.info-message {
  text-align: center;
  color: var(--ion-color-medium);
  font-size: 14px;
  padding: 10px 20px;
}

.footer-actions {
    margin-top: 50px;
    width: 100%;
    text-align: center;
}

.main-nav-btn {
    --border-radius: 8px;
    height: 55px;
    font-weight: bold;
    font-size: 16px;
    letter-spacing: 0.5px;
}

/* responsive laptop */
@media (min-width: 992px) {
    .login-container {
        max-width: 450px;
    }
    .header-title > p {
        font-size: 60px;
    }
}
</style>

