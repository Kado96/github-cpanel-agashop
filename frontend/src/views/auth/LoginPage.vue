<!--
  * @file LoginPage.vue
  * @description Page d'authentification principale. Gère la connexion des utilisateurs,
  * la récupération de la boutique associée, et la redirection selons les rôles (Admin, Agent, Client).
  * @author Kora Agency
-->
<template>
    <AuthLayout>
        <div class="wrapper">
             <div class="header-title">
                <p>Connexion</p>
            </div>
            <div class="login-container">
              <form class="login-form" @submit.prevent="perfomLogin">
                <div class="form-inputs">
                  <div class="form-group">
                      <ion-icon color="dark" :icon="personCircle"></ion-icon>
                      <label for="login-username" class="sr-only">Nom d'utilisateur</label>
                      <input
                        id="login-username"
                        name="username"
                        type="text"
                        v-model="username"
                        autofocus="true"
                        autocomplete="username"
                        placeholder="Nom d'utilisateur"
                      >
                  </div>
                  <div class="form-group">
                      <ion-icon color="dark" :icon="lockClosed"></ion-icon>
                      <label for="login-password" class="sr-only">Mot de passe</label>
                      <input
                        id="login-password"
                        name="password"
                        type="password"
                        v-model="password"
                        autocomplete="current-password"
                        placeholder="Mot de passe"
                      >
                  </div>
                </div>
                
                <div id="login-submit-btn" class="circular-button" :class="{disabledDiv:spinner}" @click="perfomLogin">
                    <ion-spinner
                        class="spinner"
                        v-if="spinner"
                        name="circular"
                    ></ion-spinner>
                    <ion-icon v-if="!spinner" color="dark" :icon="arrowForwardOutline" ></ion-icon>
                </div>
              </form>

              <div class="forgot-password-link">
                  <a id="forgot-password-link" @click.prevent="$router.push('/forgot-password')">Mot de passe oublié ?</a>
              </div>

              <div class="footer-actions">
                  <ion-button
                    id="register-redirect-btn"
                    expand="block"
                    color="primary"
                    router-link="/register"
                    class="main-nav-btn"
                  >S'ENREGISTRER
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
  personCircle, lockClosed
} from 'ionicons/icons'
import { authService, shopsService } from '../../services/api'
import { Capacitor } from '@capacitor/core'

/**
 * Composant LoginPage
 * - Gère l'état et l'interface de connexion.
 * - S'appuie sur `authService` pour l'authentification.
 * - Gère la logique complexe de redirection (admin vs agent vs otp vs shop).
 */
export default {
  data(){
    return {
      username:"",
      password:"",
      spinner:false,
      arrowForwardOutline,
      personCircle, lockClosed
    }
  },
  components: {
    IonSpinner,
    IonButton,
    AuthLayout,
    IonIcon,
  },
  methods:{
    /**
     * Récupère la boutique de l'utilisateur s'il n'en a pas dans sa réponse de login
     */
    async fetchAndSetUserShop() {
      // On nettoie d'abord toute trace de boutique précédente pour éviter les fuites de session
      localStorage.removeItem("current_shop");
      this.$store.state.shop = null;

      try {
        console.log("[LoginPage] Tentative de récupération de la boutique...");
        const res = await shopsService.getShops();
        const data = res.data;
        const shops = data.results || (Array.isArray(data) ? data : []);
        
        if (shops.length > 0) {
          const userShop = shops[0];
          console.log("[LoginPage] Boutique trouvée:", userShop.name);
          this.$store.state.shop = userShop;
          localStorage.setItem("current_shop", JSON.stringify(userShop));
        } else {
          console.warn("[LoginPage] Aucune boutique trouvée pour cet utilisateur.");
        }
      } catch (error) {
        console.error("[LoginPage] Erreur récupération boutique:", error);
      }
    },
    perfomLogin(){
        if(this.username.trim()==""){
          this.showTostMsg("Veuillez remplir votre nom d'utilisateur","danger",5000)  
          return       
        }
        if(this.password.trim()==""){
          this.showTostMsg("Veuillez spécifier votre mot de passe !","danger",5000)
          return       
        }
        else{
          this.spinner=true
          const loginId = this.username.trim()
          const pwd = this.password
          authService.login(loginId, pwd)
          .then((res)=>{
            this.spinner=false
            // Sauvegarder l'utilisateur dans le store et localStorage (incl. account_id pour agent)
            this.$store.state.user = res.data
            if (res.data.account && res.data.account.id != null) {
              this.$store.state.user.account_id = res.data.account.id
            }
            this.$store.state.shop = res.data.shop || null
            localStorage.setItem("user", JSON.stringify(this.$store.state.user))
            if (res.data.shop) {
              localStorage.setItem("current_shop", JSON.stringify(res.data.shop))
            } else {
              localStorage.removeItem('current_shop')
            }
            
            const groups = res.data.groups || []
            let groupNames = []
            if (Array.isArray(groups) && groups.length > 0) {
              if (typeof groups[0] === 'string') {
                groupNames = groups
              } else if (typeof groups[0] === 'object' && groups[0] !== null) {
                groupNames = groups.map(g => g.name || g).filter(Boolean)
              }
            }
            const isAdmin = groupNames.includes('admin') || groupNames.includes('superuser')
            const isAgent = groupNames.includes('agent')
            
            // Agent et admin : toujours vers le tableau de bord, même sans boutique
            if (isAdmin) {
              this.blurActiveElement()
              this.$router.push("/admin")
              return
            }
            if (isAgent) {
              this.blurActiveElement()
              this.$router.push("/agent")
              return
            }
            // Utilisateur normal : OTP si compte incomplet, sinon accueil
            if (res.data.account && !res.data.account.complete) {
              localStorage.setItem("otp_user", JSON.stringify({ email: res.data.username, otp: res.data.access }))
              this.$store.state.otp_user = { email: res.data.username, otp: res.data.access }
              this.blurActiveElement()
              this.$router.push("/otp")
            } else {
              // Si pas de boutique dans la réponse login, la chercher via l'API
              if (!res.data.shop) {
                this.fetchAndSetUserShop().then(() => {
                  this.blurActiveElement()
                  // Smart redirection :
                  // 1. Exactement une boutique -> Dashboard
                  // 2. Sinon (0 ou plusieurs) -> Liste (home)
                  if (this.$store.state.shops.length === 1) {
                    const userShop = this.$store.state.shops[0]
                    this.$store.state.shop = userShop
                    localStorage.setItem("current_shop", JSON.stringify(userShop))
                    this.$router.push("/shop")
                  } else {
                    this.$router.push("/")
                  }
                })
              } else {
                this.blurActiveElement()
                this.$router.push("/shop")
              }
            }
          }).catch((err)=>{
            this.spinner=false
            console.error('Erreur de connexion:', err);
            
            if (err.response && err.response.status === 401) {
              this.showTostMsg('Identifiants incorrects.', 'danger', 5000);
            } else {
              this.showTostMsg('Une erreur est survenue lors de la connexion.', 'danger', 5000);
              this.errorOrRefresh(err, () => this.perfomLogin());
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

.form-group:first-child {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
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

.forgot-password-link {
    margin-top: 10px;
    width: 100%;
    text-align: right;
}

.forgot-password-link a {
    text-decoration: none;
    font-size: 14px;
    color: var(--ion-color-medium);
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

@media (min-width: 992px) {
    .login-container {
        max-width: 450px;
    }
    .header-title > p {
        font-size: 60px;
    }
}
</style>