<!--
  * @file ForgotPasswordSuccessPage.vue
  * @description Page/Composant pour Forgot Password Success Page.
  * @author Kora Agency
-->
<template>
  <AuthLayout>
    <div class="wrapper">
      <div class="header-title">
        <p>Mot de passe envoyé</p>
      </div>
      <div class="login">
        <div class="info-message">
          <p>
            Un email de récupération de mot de passe a été envoyé à votre adresse.
            Veuillez vérifier votre boîte de réception ainsi que le dossier spam.
          </p>
        </div>
        <ion-button
          expand="full"
          color="primary"
          router-link="/login"
        >
          Retour à la connexion
        </ion-button>
      </div>
    </div>
  </AuthLayout>
</template>

<script>
import AuthLayout from "./AuthLayout.vue";
import { IonButton } from "@ionic/vue";

/**
 * Composant ForgotPasswordSuccessPage
 * - Gère l'interface et la logique métier.
 */
export default {
  components: {
    AuthLayout,
    IonButton,
  },
};
</script>

<style scoped>
.header-title {
  position: relative;
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.header-title > p {
  font-size: 32px;
  font-weight: bold;
}

.login {
  margin-top: 2rem;
  padding: 1rem;
}

.info-message {
  text-align: center;
  color: var(--ion-color-medium);
  font-size: 14px;
  padding: 0 20px 20px 20px;
}

.info-message p {
  margin: 0;
}
</style>

