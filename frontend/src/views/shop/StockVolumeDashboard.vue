<!--
  * @file StockVolumeDashboard.vue
  * @description Page pour la gestion de Stock Volume Dashboard.
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
            <span>Volume du Stock</span>
          </div>
        </ion-title>
      </ion-toolbar>
      <ion-progress-bar v-if="loading" type="indeterminate" color="success"></ion-progress-bar>
    </ion-header>

    <ion-content class="stock-volume-dashboard-content">
      <!-- 1. Header Card: Physical Quantity Summary -->
      <div class="summary-box">
        <h2 class="summary-title">Volume Physique Total</h2>
        <div class="summary-row large-stat">
          <span class="summary-value blue-text">{{ totalUnits }}</span>
          <span class="summary-unit">Unités</span>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-row small-stat">
          <span class="summary-label">Valeur totale (Achat) :</span>
          <span class="summary-val blue-text">{{ formatMoney(totalStockValue) }} BIF</span>
        </div>
        <div class="summary-row small-stat">
          <span class="summary-label">Moyenne par article :</span>
          <span class="summary-val">{{ avgUnitsPerProduct.toFixed(1) }} unités</span>
        </div>
        <div class="summary-row small-stat">
          <span class="summary-label">Références en stock :</span>
          <span class="summary-val">{{ productsCount }} articles</span>
        </div>
      </div>

      <!-- 2. Action Buttons -->
      <div class="actions-group">
        <ion-button expand="block" fill="outline" color="dark" class="btn-rect" @click="viewHistory">
          Détail des quantités par article
        </ion-button>
      </div>

      <!-- 3. Donut Chart Section: Volume by Category -->
      <div class="chart-area" v-if="currentView === 'donut'">
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
                 <text :x="segment.labelX" :y="segment.labelY + 3" class="month-text" text-anchor="middle">
                   {{ segment.name }}
                 </text>
               </template>
            </g>

            <text x="50" y="50" class="donut-center-text" text-anchor="middle" dominant-baseline="middle">
              Volume par Catégorie
            </text>
          </svg>
        </div>

        <!-- Legend -->
        <div class="legend-box">
          <div v-for="(item, index) in categoryStats" :key="index" class="legend-pill">
            <span class="pill-dot" :style="{ backgroundColor: item.color }"></span>
            <span class="pill-name">{{ item.name }}</span>
          </div>
        </div>
      </div>

      <!-- 3b. Top Volume Section -->
      <div class="chart-area quantity-map-container" v-if="currentView === 'top'">
        <div class="top-articles-box">
          <h3 class="box-title">Classement des Volumes Physiques</h3>
          <div v-for="(art, i) in topVolumeProducts" :key="i" class="art-row">
            <span class="art-rank">{{ i + 1 }}.</span>
            <span class="art-name">{{ art.name }}</span>
            <span class="art-val">{{ art.value }} unités</span>
          </div>
        </div>
      </div>

      <!-- 4. Toggle Pills -->
      <div class="view-toggle-pills">
        <ion-button :color="currentView === 'donut' ? 'success' : 'light'" class="pill-btn-ion" @click="currentView = 'donut'">
          Volume / Catégorie
        </ion-button>
        <ion-button :color="currentView === 'top' ? 'success' : 'light'" class="pill-btn-ion" @click="currentView = 'top'">
          Vérification Volumes
        </ion-button>
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

const CHART_COLORS = [
  '#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948',
  '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC', '#1565C0', '#D32F2F'
];

/**
 * Composant StockVolumeDashboard
 * - Gère l'interface et la logique métier de Stock Volume Dashboard.
 */
export default {
  name: 'StockVolumeDashboard',
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
      currentView: 'donut',
      totalUnits: 0,
      totalStockValue: 0,
      productsCount: 0,
      avgUnitsPerProduct: 0,
      categoryStats: [],
      topVolumeProducts: [],
      loading: false,
      shop: this.$store.state.shop
    };
  },
  computed: {
    shopId() {
      return this.$store.state.shop?.id || this.shop?.id;
    },
    chartSegments() {
      const total = this.categoryStats.reduce((acc, curr) => acc + curr.value, 0);
      if (total === 0) return [];
      
      let cumulativePercent = 0;
      const radius = 35;
      const circumference = 2 * Math.PI * radius;

      return this.categoryStats.map((item) => {
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
    this.fetchVolumeData();
  },
  ionViewWillEnter() {
    this.fetchVolumeData();
  },
  methods: {
    viewHistory() { 
      this.$router.push({ name: 'stock-volume-list', query: { readonly: '1' } }); 
    },
    async fetchVolumeData() {
      if (!this.shopId) return;
      this.loading = true;

      try {
        const res = await productsService.getProducts(this.shopId, { page_size: 5000 });
        const products = res.data.results || res.data || [];
        
        this.productsCount = products.length;
        this.totalUnits = products.reduce((sum, p) => sum + Number(p.quantity || 0), 0);
        this.totalStockValue = products.reduce((sum, p) => {
          const buyPrice = parseFloat(p.buy_price || p.product?.buy_price || 0);
          return sum + (Number(p.quantity || 0) * buyPrice);
        }, 0);
        this.avgUnitsPerProduct = this.productsCount > 0 ? this.totalUnits / this.productsCount : 0;

        // Group by category for donut chart
        const catMap = {};
        products.forEach(p => {
          const bp = p.product || {};
          const sub = bp.sub_category || {};
          const cat = (typeof sub === 'object' ? sub.category?.name : null) || 'Autres';
          
          if (!catMap[cat]) catMap[cat] = 0;
          catMap[cat] += Number(p.quantity || 0);
        });

        this.categoryStats = Object.keys(catMap).map((name, i) => ({
          name,
          value: catMap[name],
          color: CHART_COLORS[i % CHART_COLORS.length]
        })).sort((a, b) => b.value - a.value);

        // Top 5 volume products
        this.topVolumeProducts = products
          .map(p => ({
            name: p.product?.name || 'Inconnu',
            value: Number(p.quantity || 0)
          }))
          .sort((a, b) => b.value - a.value);

      } catch (err) {
        console.error("[StockVolumeDashboard] Erreur:", err);
      } finally {
        this.loading = false;
      }
    },
    formatMoney(val) {
      if (!val) return "0";
      return parseFloat(val).toLocaleString('fr-FR');
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
.stock-volume-dashboard-content {
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
}

.summary-title {
  font-size: 1rem;
  font-weight: 700;
  color: #64748b;
  margin: 0 0 10px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.large-stat {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
  margin-bottom: 20px;
}

.summary-value {
  font-size: 3.5rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.04em;
}

.summary-unit {
  font-size: 1.2rem;
  font-weight: 700;
  color: #94a3b8;
}

.summary-divider {
  height: 1.5px;
  background: #f1f5f9;
  margin: 20px 0;
}

.small-stat {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: #f8fafc;
  margin: 6px 0;
  border-radius: 12px;
}

.summary-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 600;
}

.summary-val {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1e293b;
}

.blue-text { color: var(--ion-color-secondary); }

.actions-group {
  padding: 0 12px;
  margin-bottom: 25px;
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
  margin: 0 12px 25px 12px;
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

.month-text {
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
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
  padding: 0 10px;
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
  border-radius: 50%;
}

.pill-name { font-size: 0.8rem; color: #475569; font-weight: 600; }

.view-toggle-pills {
  display: flex;
  gap: 12px;
  padding: 0 12px;
  margin: 10px 0 30px 0;
}

.pill-btn-ion {
  flex: 1;
  --border-radius: 14px;
  font-weight: 800;
  height: 48px;
  --box-shadow: none;
  --border-width: 1.5px;
}

.top-articles-box {
  width: 100%;
  background: #ffffff;
  padding: 0;
}

.box-title {
  margin: 0 0 20px 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #0f172a;
  text-align: center;
}

.art-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
  font-size: 1rem;
}

.art-row:last-child { border-bottom: none; }

.art-rank { font-weight: 800; color: var(--ion-color-secondary); width: 30px; }
.art-name { flex: 1; color: #475569; font-weight: 600; }
.art-val { font-weight: 800; color: #0f172a; }

.footer-action {
  padding: 0 12px 40px 12px;
}

.btn-archive {
  --background: var(--ion-color-primary);
  --color: #fff;
  --border-radius: 14px;
  height: 56px;
  font-weight: 800;
  --box-shadow: 0 4px 6px -1px rgba(21, 131, 193, 0.3);
}

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
</style>
