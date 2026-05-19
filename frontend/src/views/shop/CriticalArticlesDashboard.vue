<!--
  * @file CriticalArticlesDashboard.vue
  * @description Page pour la gestion de Critical Articles Dashboard.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-stats" name="back-to-stats" @click="$router.push({ name: 'stats' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Articles Critiques</span>
          </div>
        </ion-title>
      </ion-toolbar>
      <ion-progress-bar v-if="loading" type="indeterminate" color="success"></ion-progress-bar>
    </ion-header>

    <ion-content class="critical-articles-dashboard-content">
      <!-- 1. Alerte Header Card -->
      <div class="summary-box alert-box">
        <h2 class="summary-title" :class="ruptureCount > 0 ? 'red-text' : 'orange-text'">
           {{ ruptureCount > 0 ? 'Alerte Rupture !' : 'Niveau de Stock Bas' }}
        </h2>
        <div class="summary-row">
          <span class="summary-label">En Rupture (0) :</span>
          <span class="summary-value red-text">{{ ruptureCount }} articles</span>
        </div>
        <div class="summary-row">
          <span class="summary-label">Critiques (≤ 5) :</span>
          <span class="summary-value orange-text">{{ criticalCount }} articles</span>
        </div>
      </div>

      <!-- 2. Action Buttons -->
      <div class="actions-group">
        <ion-button expand="block" fill="outline" color="dark" class="btn-rect" @click="viewHistory">
          Gérer les réapprovisionnements
        </ion-button>
      </div>

      <!-- 3. Donut Chart Section: Critical Status -->
      <div class="chart-area" v-if="chartSegments.length > 0">
        <div class="donut-wrapper">
          <svg viewBox="0 0 100 100" class="donut-svg-main">
            <!-- Background track -->
            <circle cx="50" cy="50" r="35" fill="none" stroke="#f2f2f2" stroke-width="28" />
            
            <!-- Segments -->
            <circle v-for="(segment, index) in chartSegments" 
                    :key="index"
                    cx="50" cy="50" r="35" 
                    fill="none" 
                    :stroke="segment.color" 
                    stroke-width="28" 
                    :stroke-dasharray="segment.dashArray" 
                    :stroke-dashoffset="segment.dashOffset"
                    class="donut-ring-segment" />
            
            <!-- Labels (Masqués si trop étroit) -->
            <g v-for="(segment, index) in chartSegments" :key="'label-'+index">
               <template v-if="segment.percent >= 8">
                 <text :x="segment.labelX" :y="segment.labelY - 1" class="val-text" text-anchor="middle">
                   {{ segment.value }}
                 </text>
                 <text :x="segment.labelX" :y="segment.labelY + 3" class="status-name-text" text-anchor="middle">
                   {{ segment.name }}
                 </text>
               </template>
            </g>

            <text x="50" y="50" class="donut-center-text" text-anchor="middle" dominant-baseline="middle">
              État du Stock
            </text>
          </svg>
        </div>

        <!-- Legend -->
        <div class="legend-box">
          <div v-for="(item, index) in statusStats" :key="index" class="legend-pill">
            <span class="pill-dot" :style="{ backgroundColor: item.color }"></span>
            <span class="pill-name">{{ item.name }}</span>
          </div>
        </div>
      </div>

    </ion-content>
  </ion-page>
</template>

<script>
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonButtons,
  IonButton,
  IonTitle,
  IonContent,
  IonIcon,
  IonProgressBar
} from '@ionic/vue';
import { arrowBackOutline } from 'ionicons/icons';
import { productsService } from '../../services/api/products';

/**
 * Composant CriticalArticlesDashboard
 * - Gère l'interface et la logique métier de Critical Articles Dashboard.
 */
export default {
  name: 'CriticalArticlesDashboard',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonButtons,
    IonButton,
    IonTitle,
    IonContent,
    IonIcon,
    IonProgressBar
  },
  data() {
    return {
      arrowBackOutline,
      ruptureCount: 0,
      criticalCount: 0,
      criticalCount: 0,
      okCount: 0,
      allCriticalProducts: [],
      loading: false,
      shop: this.$store.state.shop
    };
  },
  computed: {
    shopId() {
      return this.$store.state.shop?.id || this.shop?.id;
    },
    statusStats() {
      return [
        { name: 'Rupture', value: this.ruptureCount, color: '#D32F2F' },
        { name: 'Critique', value: this.criticalCount, color: '#F28E2B' },
        { name: 'Correct', value: this.okCount, color: '#109618' }
      ].filter(s => s.value > 0);
    },
    chartSegments() {
      const total = this.statusStats.reduce((acc, curr) => acc + curr.value, 0);
      if (total === 0) return [];
      
      let cumulativePercent = 0;
      const radius = 35;
      const circumference = 2 * Math.PI * radius;

      return this.statusStats.map((item) => {
        const percent = (item.value / total) * 100;
        const dashArray = `${(percent * circumference) / 100} ${circumference}`;
        const dashOffset = (cumulativePercent * circumference) / 100;

        const angle = ((cumulativePercent + percent / 2) / 100) * 360 - 90;
        const radian = (angle * Math.PI) / 180;
        const labelR = 40; // Augmenté pour aérer
        const labelX = 50 + labelR * Math.cos(radian);
        const labelY = 50 + labelR * Math.sin(radian);

        const res = {
          ...item,
          percent,
          dashArray,
          dashOffset: -dashOffset,
          labelX,
          labelY
        };
        cumulativePercent += percent;
        return res;
      });
    }
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchCriticalData();
  },
  ionViewWillEnter() {
    this.fetchCriticalData();
  },
  methods: {
    viewHistory() { 
      this.$router.push({ name: 'critical-articles-list' }); 
    },
    async fetchCriticalData() {
      if (!this.shopId) return;
      this.loading = true;

      try {
        const res = await productsService.getProducts(this.shopId, { no_pagination: 'true' });
        const products = res.data.results || res.data || [];
        
        this.ruptureCount = products.filter(p => p.quantity <= 0).length;
        this.criticalCount = products.filter(p => p.quantity > 0 && p.quantity <= 5).length;
        this.okCount = products.filter(p => p.quantity > 5).length;

        // Collecter tous les articles à risque
        this.allCriticalProducts = products
          .filter(p => p.quantity <= 5)
          .map(p => ({
            name: p.product?.name || 'Inconnu',
            quantity: p.quantity
          }))
          .sort((a, b) => a.quantity - b.quantity);

      } catch (err) {
        console.error("[CriticalArticlesDashboard] Erreur:", err);
      } finally {
        this.loading = false;
      }
    },
    getShopFromLocalStorage() {
      try {
        const s = localStorage.getItem('current_shop');
        return s ? JSON.parse(s) : null;
      } catch (e) {
        return null;
      }
    }
  }
};
</script>

<style scoped>
.critical-articles-dashboard-content {
  --background: #cbd5e1;
}

.summary-box {
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 20px;
  padding: 24px 16px;
  margin: 16px 12px;
  text-align: center;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.alert-box {
  border-left: 6px solid #ef4444;
}

.summary-title {
  font-size: 1.3rem;
  font-weight: 800;
  margin-bottom: 20px;
  letter-spacing: -0.02em;
}

.red-text { color: #ef4444; }
.orange-text { color: #f59e0b; }

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 16px;
  background: #f8fafc;
  margin-bottom: 8px;
  border-radius: 12px;
}

.summary-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
}

.summary-value {
  font-size: 1rem;
  font-weight: 800;
}

.actions-group {
  padding: 0 12px;
  margin-bottom: 20px;
}

.btn-rect {
  --background: #fff;
  --border-color: #e2e8f0;
  --border-style: solid;
  --border-width: 1.5px;
  --border-radius: 14px;
  --color: #334155;
  margin: 0;
  height: 54px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);

  &:active {
    --background: #f8fafc;
  }
}

.chart-area {
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 20px;
  padding: 24px 16px;
  margin: 0 12px 30px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
}

.donut-wrapper {
  width: 100%;
  max-width: 280px;
  aspect-ratio: 1/1;
}

.donut-svg-main {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-ring-segment {
  transition: all 0.5s ease;
}

.val-text {
  font-size: 4px;
  font-weight: 800;
  fill: #0f172a;
  transform: rotate(90deg);
  transform-origin: center;
}

.status-name-text {
  font-size: 3px;
  font-weight: 600;
  fill: #fff;
  transform: rotate(90deg);
  transform-origin: center;
}

.donut-center-text {
  font-size: 4.5px;
  fill: #1e293b;
  font-weight: 800;
  transform: rotate(90deg);
  transform-origin: 50% 50%;
}

.legend-box {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
}

.legend-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  padding: 6px 12px;
  border-radius: 10px;
  border: 1px solid #f1f5f9;
}

.pill-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

.pill-name { font-size: 0.8rem; font-weight: 600; color: #475569; }

.footer-action { padding-bottom: 30px; }

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.list-area {
  align-items: stretch;
  padding: 20px 16px;
}

.box-title {
  margin: 0 0 16px 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #1e293b;
  text-align: center;
}

.art-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
}

.art-row:last-child {
  border-bottom: none;
}

.art-info {
  display: flex;
  flex-direction: column;
}

.art-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #334155;
}

.art-status {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.art-val {
  font-size: 0.95rem;
  font-weight: 800;
}
</style>
