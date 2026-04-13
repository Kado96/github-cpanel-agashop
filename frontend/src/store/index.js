import { createStore } from 'vuex'

// Plugin pour sauvegarder automatiquement l'utilisateur dans localStorage
const localStoragePlugin = (store) => {
  // Restaurer l'utilisateur depuis localStorage au démarrage
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    try {
      store.state.user = JSON.parse(savedUser)
    } catch (e) {
      console.error('Erreur lors de la restauration de l\'utilisateur:', e)
      localStorage.removeItem('user')
    }
  }

  // Sauvegarder l'utilisateur dans localStorage à chaque changement
  store.subscribe((mutation, state) => {
    if (state.user) {
      localStorage.setItem('user', JSON.stringify(state.user))
    } else {
      localStorage.removeItem('user')
    }
  })
}

export default createStore({
  state: {
    user: null,
    otp_user: null,
    segmentValue: "login",
    shops: [],
    products: [],
    sales: [],
    supplies: [],
    shop: null,
    ion_alert: {
      is_open: false,
      header: '',
      subHeader: '',
      message: '',
      buttons: [
        {
          text: 'Ok',
          cssClass: 'alert-button-confirm',
        }
      ],
      cssClass: "custom-css"
    },
    helpContext: null // { title: '', description: '', actions: [], faqs: [] }
  },
  mutations: {
    SET_HELP_CONTEXT(state, context) {
      state.helpContext = context;
    }
  },
  plugins: [localStoragePlugin]
})