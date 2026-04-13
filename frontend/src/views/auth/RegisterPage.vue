<!--
  * @file RegisterPage.vue
  * @description Page d'inscription (création de compte).
  * Collecte l'email, le username, le téléphone (avec code pays) et le mot de passe.
  * @author Kora Agency
-->
<template>
    <AuthLayout>
        <div class="wrapper">
             <div class="header-title">
                <p>S'enregistrer</p>
            </div>
            <div class="login-container">
              <div class="login-form">
                <div class="form-inputs">
                  <div class="form-group">
                      <ion-icon color="dark" :icon="mail"></ion-icon>
                      <label for="register-email" class="sr-only">E-mail</label>
                      <input
                        id="register-email"
                        name="email"
                        type="email"
                        v-model="register.email"
                        autofocus="true"
                        autocomplete="email"
                        placeholder="Votre e-mail"
                      >
                  </div>
                  <div class="form-group">
                      <ion-icon color="dark" :icon="personCircle"></ion-icon>
                      <label for="register-username" class="sr-only">Nom d'utilisateur</label>
                      <input
                        id="register-username"
                        name="username"
                        type="text"
                        v-model="register.username"
                        autocomplete="username"
                        placeholder="Nom d'utilisateur"
                      >
                  </div>
                  <div class="form-group phone-container">
                      <div class="phone-inputs">
                        <label for="register-country-code" class="sr-only">Code pays</label>
                        <label for="register-phone" class="sr-only">Téléphone</label>
                        <select 
                          id="register-country-code"
                          name="country_code"
                          v-model="register.country_code" 
                          class="country-code-select"
                        >
                          <option v-for="c in countryList" :key="c.code" :value="c.prefix">
                            {{ c.name }} ({{ c.prefix }})
                          </option>
                        </select>
                        <input
                          id="register-phone"
                          name="phone"
                          type="tel"
                          v-model="register.phone_number"
                          autocomplete="tel"
                          placeholder="Téléphone"
                        >
                      </div>
                  </div>
                  <div class="form-group">
                      <ion-icon color="dark" :icon="lockClosed"></ion-icon>
                      <label for="register-password" class="sr-only">Mot de passe</label>
                      <input
                        id="register-password"
                        name="password"
                        type="password"
                        v-model="register.password"
                        autocomplete="new-password"
                        placeholder="Mot de passe"
                      >
                  </div>
                </div>
                
                <div id="register-submit-btn" class="circular-button" :class="{disabledDiv:spinner}" @click="performRegister">
                    <ion-spinner
                        class="spinner"
                        v-if="spinner"
                        name="circular"
                    ></ion-spinner>
                    <ion-icon v-if="!spinner" color="dark" :icon="arrowForwardOutline" ></ion-icon>
                </div>
              </div>

              <div class="footer-actions">
                  <ion-button
                    id="login-redirect-btn"
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
  personCircle, call, mail, lockClosed
} from 'ionicons/icons'
import { authService } from '../../services/api'
import { countries } from '../../services/countries'

/**
 * Composant RegisterPage
 * - Gère l'inscription des utilisateurs.
 * - Inclut le nettoyage du numéro de téléphone avant soumission.
 */
export default {
  data(){
    return {
      register:{
          username:"",
          email:"",
          phone_number:"",
          country_code:"+257",
          password:"",
      },
      spinner:false,
      countryList: countries,
      arrowForwardOutline,
      personCircle, call, mail, lockClosed
    }
  },
  components: {
    IonSpinner,
    IonButton,
    AuthLayout,
    IonIcon,
  },
  methods:{
      formatPhoneNumber(phone){
        // Enlever tous les espaces et caractères non numériques du numéro
        let cleaned = phone.replace(/\D/g, '')
        
        // Retirer le '+' du code pays pour la comparaison
        let codeDigits = this.register.country_code.replace('+', '')
        
        // Si le numéro commence déjà par le code pays sélectionné, on ne le rajoute pas
        if (cleaned.startsWith(codeDigits)) {
          return '+' + cleaned
        }
        
        // Sinon, combiner le code pays choisi avec le numéro nettoyé
        return this.register.country_code + cleaned
      },
      performRegister(){
        if(this.register.email.trim()==""){
          this.showTostMsg("Veuillez remplir votre e-mail","danger",5000)
          this.spinner = false
          return       
        }
        if(!this.register.email.trim().includes("@")){
          this.showTostMsg("Veuillez remplir un email valide !","danger",5000)
          this.spinner = false
          return      
        }
        if(this.register.username.trim()==""){
          this.showTostMsg("Veuillez remplir votre nom d'utilisateur","danger",5000)
          this.spinner = false
          return       
        }
        if(this.register.phone_number.trim()==""){
          this.showTostMsg("Veuillez remplir votre numéro de téléphone !","danger",5000)
          this.spinner = false
          return        
        }
        if(this.register.password.trim()==""){
          this.showTostMsg("Veuillez spécifier votre mot de passe !","danger",5000)
          this.spinner = false
          return         
        }
        if(this.register.password.trim().length < 4){
          this.showTostMsg("Le mot de passe doit contenir au moins 4 caractères !","danger",5000)
          this.spinner = false
          return         
        }
        else{
          this.spinner=true
          
          // Formater le numéro de téléphone
          const formattedPhone = this.formatPhoneNumber(this.register.phone_number)
          
          const registerData = {
            username: this.register.username.trim(),
            email: this.register.email.trim(),
            phone_number: formattedPhone,
            password: this.register.password
          }
          
          authService.register(registerData)
          .then((res)=>{
            this.spinner=false
            this.showTostMsg("Inscription réussie ! Veuillez vous connecter.","success",5000)
            this.$router.push("/login")
          }).catch((err)=>{
            this.spinner=false
            this.errorOrRefresh(err, () => this.performRegister())
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

.form-group input,
.form-group .phone-inputs {
    width: 100%;
    height: 60px;
    border: none;
    background: transparent;
    font-size: 18px;
    padding: 10px 15px 10px 50px;
    outline: none;
}

.phone-container .phone-inputs {
    padding-left: 0;
    display: flex;
}

.country-code-select {
    background: #e0e0e0;
    border: none;
    padding: 0 5px 0 10px;
    font-size: 16px;
    font-weight: bold;
    border-right: 1px solid #ccc;
    outline: none;
    max-width: 150px; /* Limit width for the name */
    text-overflow: ellipsis;
}

.phone-inputs input {
    padding-left: 15px !important;
}

/* Border radius logic for the group */
.form-group:first-child .form-inputs input,
.form-group:first-child {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
.form-group:last-child .form-inputs input,
.form-group:last-child {
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}

.circular-button {
    position: absolute;
    bottom: -30px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: #007bff; /* Blue as in screenshot */
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
    background: #0056b3;
}

.circular-button ion-icon {
    font-size: 30px;
    color: black; /* Changed back to black as in user screenshot */
}

.disabledDiv {
    opacity: 0.7;
    pointer-events: none;
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