import {
  toastController,alertController
} from '@ionic/vue';
import { axiosService } from '../plugins/axios';



export default {
  methods: {
    async logOut() {
			const alert = await alertController
				.create({
					cssClass: 'custom-alert',
					header: 'Déconnexion',
					message: 'Voulez-vous vous déconnecter ?',
					buttons: [
						{
              text: 'Non',
              role: 'cancel',
            },
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
			await alert.present();
			await alert.onDidDismiss();
		},
    cleanString(str){
      if (!str) return "";
      if(typeof(str)=='object'){
        let string = ""
        for( let [clef, valeur] of Object.entries(str)){
          if(typeof(valeur)=='object'){
            let child = ""
            for( let [key, value] of Object.entries(valeur)){
              child += `${value}. `
            }
            valeur = child;
          }
          string+=`"${clef}": ${valeur}. `
        }
        return string;
      };
      str = str.toString();
      return str.replace( /(<([^>]+)>)/ig, '');
    },
    formatDateTime(x) {
      if(!x) return "-"
      let date = new Date(x);
      return new Intl.DateTimeFormat(
        'en-GB',
        { dateStyle: 'short', timeStyle: 'short' }
      ).format(date)
    },
    retrieveUserFromLS(){
      var user = JSON.parse(localStorage.getItem('user'));
      if(user) {
        this.$store.state.user = user;
      }
    },
    checkCurrentShop(){
      const shopData = localStorage.getItem("current_shop")
      const isNoShopFound = !shopData || shopData === "null" || shopData === "undefined";
      
      // Si aucune boutique et qu'on n'est pas déjà sur l'accueil ou le login, on redirige vers l'accueil
      const currentRoute = this.$route?.name;
      if (isNoShopFound && !['home', 'shop', 'login'].includes(currentRoute)) {
        console.log(`[mixin] Boutique manquante sur '${currentRoute}' -> redirection vers l'accueil`);
        this.$router.push({ name: "home" });
      }
    },
    getShopFromLocalStorage(){
      const shopData = localStorage.getItem("current_shop")
      if(shopData && shopData !== "null" && shopData !== "undefined"){
        try {
          return JSON.parse(shopData)
        } catch (e) {
          console.error("Erreur lors du parsing du shop:", e)
          return null
        }
      }
      return null
    },
    money(x, decimals=0) {
      let cash = parseFloat(x).toFixed(decimals)
      if(isNaN(x) || x == null) return "-";
      return cash.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    },
    errorOrRefresh(error, callback, substitution_error_msg){
      // Gestion du token expiré
      const status = error.response?.status

      // Certains backends renvoient 401 sans "token_not_valid"
      if (status === 401 && error.response?.data?.code !== "token_not_valid") {
        const refresh = this.$store.state.user?.refresh
        if (!refresh) {
          this.$store.state.user = null;
          localStorage.removeItem('user')
          localStorage.removeItem('current_shop')
          this.$router.push('/login')
          this.showTostMsg("Veuillez vous reconnecter.", "danger", 4000)
          return
        }
        this.blurActiveElement(); // Prevent aria-hidden focus warnings
        axiosService.post("/refresh/", {"refresh":refresh})
          .then((response) => {
            this.$store.state.user.access = response.data.access
            localStorage.setItem("user", JSON.stringify(this.$store.state.user))
            if(typeof callback == "function") callback()
          })
          .catch((e) => {
            this.blurActiveElement(); // Prevent aria-hidden focus warnings
            this.$store.state.user = null;
            localStorage.removeItem('user')
            localStorage.removeItem('current_shop')
            this.$router.push('/login')
            console.error(e)
            this.showTostMsg("La session a expiré. Veuillez vous reconnecter.", "danger",5000)
          })
        return
      }

      if(error.response?.data?.code == "token_not_valid"){ 
        let refresh = this.$store.state.user?.refresh
        if(!refresh){
          this.blurActiveElement(); // Prevent aria-hidden focus warnings
          this.$store.state.user = null;
          localStorage.removeItem('user')
          this.$router.push('/login')
          return
        }
        this.blurActiveElement(); // Prevent aria-hidden focus warnings
        axiosService.post("/refresh/", {"refresh":refresh})
        .then((response) => {
          // Mettre à jour le token dans le store et localStorage
          this.$store.state.user.access = response.data.access
          localStorage.setItem("user", JSON.stringify(this.$store.state.user))
          if(typeof callback == "function") callback()
        }).catch((error) => {
          this.blurActiveElement(); // Prevent aria-hidden focus warnings
          this.$store.state.user = null;
          localStorage.removeItem('user')
          localStorage.removeItem('current_shop')
          this.$router.push('/login')
          console.error(error)
          this.showTostMsg("La session a expiré. Veuillez vous reconnecter.", "danger",5000)
        })
      } else {
        // Log debug riche (endpoint + payload + réponse) pour diagnostiquer rapidement les 4xx/5xx
        try {
          const cfg = error?.config || {}
          const resp = error?.response
          const errorData = resp?.data || {}
          
          // Log l'erreur de manière plus visible pour les 500 errors
          if (resp?.status === 500) {
            console.error('🚨 SERVER ERROR (500):', {
              endpoint: `${cfg?.baseURL || ''}${cfg?.url || ''}`,
              method: cfg?.method?.toUpperCase?.() || 'REQUEST',
              errorMessage: error?.message,
              responseData: errorData,
              // Essayer d'extraire le message d'erreur du backend
              backendError: errorData?.detail || errorData?.message || errorData?.error || JSON.stringify(errorData)
            })
          }
          
          console.groupCollapsed?.(
            `[API ERROR] ${cfg?.method?.toUpperCase?.() || 'REQUEST'} ${cfg?.baseURL || ''}${cfg?.url || ''} -> ${resp?.status || 'NO_STATUS'}`
          )
          console.error('AxiosError:', error?.message || error)
          console.log('Request config:', {
            baseURL: cfg?.baseURL,
            url: cfg?.url,
            method: cfg?.method,
            params: cfg?.params,
            data: cfg?.data,
            headers: cfg?.headers
          })
          console.log('Response:', {
            status: resp?.status,
            statusText: resp?.statusText,
            data: resp?.data,
            headers: resp?.headers
          })
          // Afficher le message d'erreur backend de manière plus visible
          if (errorData) {
            console.error('Backend Error Details:', errorData)
            if (errorData.detail) console.error('Error Detail:', errorData.detail)
            if (errorData.message) console.error('Error Message:', errorData.message)
            if (errorData.error) console.error('Error:', errorData.error)
          }
          console.groupEnd?.()
        } catch (e) {
          console.error('Error logging failed:', e)
          console.error('Original error:', error)
        }

        // Récupérer le message brut renvoyé par l'API (DRF utilise souvent "detail")
        const data = error.response?.data
        let raw_error =
          data?.message ||
          data?.detail ||
          data?.error ||
          data?.errors ||
          data ||
          error?.message ||
          "Erreur inconnue"
        let error_text = this.cleanString(raw_error).toString().toLowerCase()

        // Messages utilisateur en français selon les cas les plus fréquents
        let user_message = null

        // Compte déjà existant (inscription / création via admin)
        // On gère les variantes avec ou sans accents pour être robuste
        if (
          error_text.includes("already exists") ||
          error_text.includes("user with this email") ||
          error_text.includes("cet email est deja pris") ||
          error_text.includes("cet email est déjà pris") ||
          error_text.includes("un utilisateur avec cet email existe deja") ||
          error_text.includes("un utilisateur avec cet email existe déjà") ||
          error_text.includes("existe deja") ||
          error_text.includes("existe déjà")
        ) {
          user_message = "Un compte existe déjà avec cet e‑mail (utilisateur, agent ou administrateur). Utilisez une autre adresse ou connectez‑vous avec cet e‑mail."
        }
        // Numéro de téléphone déjà utilisé
        else if (
          error_text.includes("phone") && error_text.includes("already in use") ||
          error_text.includes("ce numéro de teéléphone est déjà utilisé") ||
          error_text.includes("ce numéro de téléphone est déjà utilisé")
        ) {
          user_message = "Ce numéro de téléphone est déjà utilisé par un autre compte. Utilisez un autre numéro ou connectez‑vous."
        }
        // Utilisateur inexistant / compte inactif / identifiants invalides
        else if (
          error_text.includes("no active account found with the given credentials") ||
          error_text.includes("no active account") ||
          error_text.includes("invalid credentials") ||
          error_text.includes("unable to log in") ||
          error_text.includes("not found") ||
          error_text.includes("does not exist")
        ) {
          user_message = "E‑mail ou mot de passe incorrect, ou compte inactif. Vérifiez vos identifiants ou contactez l’administrateur."
        }
        // Erreur de format de mot de passe
        else if (error_text.includes("password") && (error_text.includes("too short") || error_text.includes("common") || error_text.includes("numeric"))) {
          user_message = "Votre mot de passe n’est pas assez sécurisé. Utilisez au moins 8 caractères, avec des lettres et des chiffres."
        }
        // Erreur d'e-mail invalide
        else if (error_text.includes("email") && (error_text.includes("valid") || error_text.includes("invalid"))) {
          user_message = "L’adresse e-mail saisie n’est pas valide. Vérifiez la saisie et réessayez."
        }
        // Mot de passe oublié : email inconnu
        else if (error_text.includes("password reset") && error_text.includes("email")) {
          user_message = "Aucun compte n’est associé à cet e-mail. Vérifiez l’adresse ou créez un nouveau compte."
        }
        // Erreurs 400 génériques (validation, droits insuffisants, etc.)
        else if (error.response?.status === 400) {
          // Si le backend a renvoyé un message lisible (detail/details),
          // on le réutilise pour être plus précis avec l'utilisateur.
          const backendDetail =
            (typeof data?.details === 'string' && data.details) ||
            (typeof data?.detail === 'string' && data.detail)

          if (backendDetail && backendDetail.length < 250) {
            user_message = this.cleanString(backendDetail)
          } else {
            user_message = "Les informations envoyées ne sont pas valides. Vérifiez les champs et réessayez."
          }
        }
        // Erreur serveur
        else if (error.response?.status === 500) {
          // Essayer d'extraire un message d'erreur du backend si disponible
          const backendMsg = data?.detail || data?.message || data?.error
          if (backendMsg && typeof backendMsg === 'string' && backendMsg.length < 200) {
            user_message = `Erreur serveur: ${this.cleanString(backendMsg)}. Veuillez réessayer ou contacter le support.`
          } else {
            user_message = "Une erreur est survenue sur le serveur. Réessayez plus tard ou contactez le support si le problème persiste."
          }
        }

        // Fallback : message brut nettoyé ou message de substitution
        if(!user_message){
          user_message = substitution_error_msg 
            || this.cleanString(raw_error) 
            || "Une erreur inattendue est survenue. Veuillez réessayer dans quelques instants."
        }

        this.showTostMsg(user_message, "danger",5000)
      }
    },
    async showToastMsg(msg, type, duration = 3000) {
        this.blurActiveElement(); // Fix aria-hidden focus warning in production
        const toast = await toastController.create({
            message: msg,
            animated: true,
            duration: duration,
            color: type,
            position: 'bottom'
        })
        toast.present()
    },
    // Alias for backward compatibility
    async showTostMsg(msg, type, duration) {
        return this.showToastMsg(msg, type, duration);
    },
    truncate(value, length) {
      if (value.length > length) {
        return value.substring(0, length) + "...";
      } else {
        return value;
      }
    },
    maskValue(string) {
        return string.slice(0, 3) + ' ****** ' + string.slice(-4);
    },
    getCategoryLabel(item) {
      if (!item) return 'Non catégorisé';
      // Gérer tous les formats de données possibles (produit direct ou imbriqué)
      const bp = item.product?.product ?? item.product; 
      if (!bp) return 'Non catégorisé';

      const sub = bp.sub_category;
      
      // 1. Priorité aux données déjà imbriquées (objets)
      if (sub && typeof sub === 'object' && sub.name) {
        const catName = sub.category?.name || sub.category_name || '';
        return catName ? `${catName} > ${sub.name}` : sub.name;
      }

      // 2. Résolution via la liste locale 'categories' si sub est un ID ou manquant
      if (this.categories && Array.isArray(this.categories)) {
        const subId = bp.sub_category_id ?? (typeof sub === 'number' ? sub : null);
        if (subId) {
          for (const cat of this.categories) {
            const subs = cat.sub_categories || cat.subCategories || [];
            const found = subs.find(s => Number(s.id) === Number(subId));
            if (found) return `${cat.name} > ${found.name}`;
          }
        }
      }

      return 'Non catégorisé';
    },
    active_user_is(...attribs){
      let user_attributions = this.active_user?.groups
      if(!!this.active_user && !!user_attributions){
        for (let attrib of attribs) {
          for(let u_attrib of user_attributions){
            const name = typeof u_attrib === 'string' ? u_attrib : (u_attrib.name || '');
            if(name.toLowerCase() == attrib.toLowerCase())
              return true
            }
          }
      }
      return false
    },
    /**
     * Retourne l'URL de base pour les médias (sans /api)
     */
    getMediaBaseUrl() {
      const base = (axiosService.defaults.baseURL || '').replace(/\/api\/?$/, '');
      if (base) return base;
      return typeof window !== 'undefined' ? window.location.origin : '';
    },

    /**
     * Génère l'URL complète pour une image de produit.
     * Gère les formats imbriqués (shop product) ou directs (basic product).
     */
    productImage(item) {
      if (!item) return '/placeholder.png';
      
      // Extraction robuste de l'image brute
      let raw = null;
      if (typeof item === 'string') {
        raw = item;
      } else {
        // Ordre de priorité pour l'extraction
        raw = item.image || 
              item.product?.image || 
              item.product?.product?.image || 
              item.product?.product?.product?.image || 
              null;
      }
      
      if (!raw || (typeof raw === 'string' && !raw.trim())) return '/placeholder.png';
      if (typeof raw === 'string' && (raw.startsWith('http') || raw.startsWith('data:'))) return raw;
      
      const base = this.getMediaBaseUrl();
      let path = String(raw).startsWith('/') ? raw : `/${raw}`;
      
      // S'assurer que le chemin commence par /media
      // Note: Django stocke souvent 'images/nom.png'
      if (!path.startsWith('/media/')) {
        // Si le chemin contient déjà 'media/', on ajuste
        if (path.includes('/media/')) {
          path = path.substring(path.indexOf('/media/'));
        } else {
          path = `/media${path}`;
        }
      }
      
      return `${base}${path}`;
    },
    /**
     * Évite l'avertissement Chrome:
     * "Blocked aria-hidden on an element because its descendant retained focus"
     * en retirant le focus de l'élément actif avant d'ouvrir un modal/alerte.
     */
    blurActiveElement() {
      try {
        const el = typeof document !== 'undefined' ? document.activeElement : null;
        if (el && typeof el.blur === 'function') el.blur();
      } catch (e) {
        console.warn('blurActiveElement failed:', e);
      }
    },
  },
  computed:{
    active_user(){
      return this.$store.state.user;
    },
    active_fullname(){
      return `${this.active_user?.first_name} ${this.active_user?.last_name}`;
    },
  }
}
