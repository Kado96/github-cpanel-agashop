import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'bi.sales.agashop',
  appName: 'AgaShop',
  webDir: 'dist',
  plugins: {
    SplashScreen: {
      launchAutoHide: false,
      backgroundColor: "#ff7200",
      showSpinner: false,
      androidSpinnerStyle: "small",
      iosSpinnerStyle: "small",
      splashFullScreen: true,
      splashImmersive: true,
    },
  },
};

export default config;
