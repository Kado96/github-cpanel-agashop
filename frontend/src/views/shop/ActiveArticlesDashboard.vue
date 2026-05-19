<!--
  * @file ActiveArticlesDashboard.vue
  * @description Page pour la gestion de Active Articles Dashboard.
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
            <span>Articles Actifs</span>
          </div>
        </ion-title>
      </ion-toolbar>
      <ion-progress-bar v-if="loading" type="indeterminate" color="success"></ion-progress-bar>
    </ion-header>

    <ion-content class="active-articles-dashboard-content">
      <!-- 1. Header Card: Stock Summary -->
      <div class="summary-box">
        <h2 class="summary-title">Bilan de mon Inventaire</h2>
        <div class="summary-row">
          <span class="summary-label">Valeur Marchande :</span>
          <span class="summary-value blue-text">{{ money(totalValue) }} BIF</span>
        </div>
        <div class="summary-row">
          <span class="summary-label">Coût du Stock :</span>
          <span class="summary-value red-text">{{ money(totalCost) }} BIF</span>
        </div>
        <div class="summary-row">
          <span class="summary-label">Références :</span>
          <span class="summary-value">{{ productsCount }} articles</span>
        </div>
      </div>

      <!-- 2. Action Buttons -->
      <div class="actions-group">
        <ion-button expand="block" fill="outline" color="dark" class="btn-rect" @click="viewHistory">
          Consulter l'inventaire complet
        </ion-button>
      </div>

      <!-- 3. Donut Chart Section: Value by Category -->
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
                   {{ money(segment.value) }}
                 </text>
                 <text :x="segment.labelX" :y="segment.labelY + 3" class="month-text" text-anchor="middle">
                   {{ segment.name }}
                 </text>
               </template>
            </g>

            <text x="50" y="50" class="donut-center-text" text-anchor="middle" dominant-baseline="middle">
              Valeur par Catégorie
            </text>
          </svg>
        </div>

        <!-- Legend -->
        <div class="legend-box">
          <div v-for="(item, index) in categoryStats" :key="index" class="legend-pill">
            <span class="pill-dot" :style="{ backgroundColor: item.color }"></span>
            <span class="pill-name">{{ item.name }}</span>
          </div>
          <span class="pill-name-main">Catégories</span>
        </div>
      </div>

      <!-- 3b. Quantity Map Section (Alternative View) -->
      <div class="chart-area quantity-map-container" v-if="currentView === 'quantities'">
        <div class="top-articles-box">
          <h3 class="box-title">Classement des Articles (Valeur)</h3>
          <div v-for="(art, i) in topArticles" :key="i" class="art-row">
            <span class="art-rank">{{ i + 1 }}.</span>
            <span class="art-name">{{ art.name }}</span>
            <span class="art-val">{{ money(art.value) }} BIF</span>
          </div>
        </div>
      </div>

      <!-- 4. Toggle Pills -->
      <div class="view-toggle-pills">
        <ion-button :color="currentView === 'donut' ? 'success' : 'light'" class="pill-btn-ion" @click="currentView = 'donut'">
          Répartition Valeur
        </ion-button>
        <ion-button :color="currentView === 'quantities' ? 'success' : 'light'" class="pill-btn-ion" @click="currentView = 'quantities'">
          Analyse Articles
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
 * Composant ActiveArticlesDashboard
 * - Gère l'interface et la logique métier de Active Articles Dashboard.
 */
export default {
  name: 'ActiveArticlesDashboard',
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
      totalValue: 0,
      totalCost: 0,
      productsCount: 0,
      categoryStats: [],
      topArticles: [],
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
    this.fetchInventoryData();
  },
  ionViewWillEnter() {
    this.fetchInventoryData();
  },
  methods: {
    viewHistory() { 
      this.$router.push({ name: 'active-articles-list' }); 
    },
    async fetchInventoryData() {
      if (!this.shopId) return;
      this.loading = true;

      try {
        const res = await productsService.getProducts(this.shopId, { no_pagination: 'true' });
        const data = res.data;
        const products = data.results || data || [];
        const totals = data.totals || { market_value: 0, cost_value: 0, quantity: 0 };
        
        this.productsCount = data.count || products.length;
        this.totalValue = totals.market_value;
        this.totalCost = totals.cost_value;

        // Group by category for donut chart
        const catMap = {};
        products.forEach(p => {
          const bp = p.product || {};
          const sub = bp.sub_category || {};
          const cat = (typeof sub === 'object' ? sub.category?.name : null) || 'Autres';
          
          if (!catMap[cat]) catMap[cat] = 0;
          catMap[cat] += (p.quantity * p.sale_price);
        });

        this.categoryStats = Object.keys(catMap).map((name, i) => ({
          name,
          value: catMap[name],
          color: CHART_COLORS[i % CHART_COLORS.length]
        })).sort((a, b) => b.value - a.value);

        // Top 5 articles
        this.topArticles = products
          .map(p => ({
            name: p.product?.name || 'Inconnu',
            value: p.quantity * p.sale_price
          }))
          .sort((a, b) => b.value - a.value);

      } catch (err) {
        console.error("[ActiveArticlesDashboard] Erreur:", err);
      } finally {
        this.loading = false;
      }
    },
    money(val) {
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
.active-articles-dashboard-content {
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
  font-size: 1.3rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 16px 0;
  letter-spacing: -0.02em;
}

.summary-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.summary-label {
  font-size: 0.95rem;
  color: #64748b;
  font-weight: 600;
}

.summary-value {
  font-size: 1.1rem;
  font-weight: 800;
}

.blue-text { color: var(--ion-color-secondary); }
.red-text { color: #ef4444; }

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

.footer-action {
  padding: 0 12px 30px 12px;
}

.btn-archive {
  --background: var(--ion-color-primary);
  --color: #fff;
  --border-radius: 14px;
  --box-shadow: 0 4px 6px -1px rgba(21, 131, 193, 0.3);
  font-weight: 800;
  height: 56px;
}

.chart-area {
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 20px;
  padding: 24px 16px;
  margin: 0 12px 20px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
  min-width: 0;
}

.donut-wrapper {
  width: 100%;
  max-width: 300px;
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
  font-size: 3.5px;
  font-weight: 800;
  fill: #0f172a;
  transform: rotate(90deg);
  transform-origin: center;
}

.month-text {
  font-size: 2.8px;
  font-weight: 600;
  fill: #475569;
  transform: rotate(90deg);
  transform-origin: center;
}

.donut-center-text {
  font-size: 4px;
  fill: #1e293b;
  font-weight: 800;
  transform: rotate(90deg);
  transform-origin: 50% 50%;
}

.legend-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
  padding: 0 10px;
}

.legend-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1px solid #f1f5f9;
}

.pill-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

.pill-name { 
  font-size: 0.8rem; 
  color: #475569; 
  font-weight: 600;
}
.pill-name-main { 
  display: block;
  width: 100%;
  text-align: center;
  font-size: 0.85rem; 
  font-weight: 800; 
  color: #1e293b; 
  margin-top: 12px;
}

.view-toggle-pills {
  display: flex;
  gap: 12px;
  padding: 0 12px;
  margin: 10px 0 25px 0;
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
  margin: 0 0 16px 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #1e293b;
  text-align: center;
}

.art-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.95rem;
  align-items: center;
  min-width: 0;
}

.art-row:last-child { border-bottom: none; }

.art-rank { font-weight: 800; color: var(--ion-color-secondary); width: 25px; flex-shrink: 0; }
.art-name { flex: 1; color: #475569; font-weight: 600; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.art-val { font-weight: 800; color: #0f172a; white-space: nowrap; flex-shrink: 0; margin-left: 8px; }

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

@media (max-width: 480px) {
  .summary-box {
    padding: 16px 12px;
    margin: 10px 6px;
  }
  .summary-title {
    font-size: 1.1rem;
    margin-bottom: 12px;
  }
  .summary-label {
    font-size: 0.85rem;
  }
  .summary-value {
    font-size: 0.95rem;
  }
  .btn-rect {
    height: 48px;
    font-size: 0.9rem;
  }
  .actions-group {
    padding: 0 6px;
    margin-bottom: 15px;
  }
  .chart-area {
    padding: 16px 10px;
    margin: 0 6px 15px 6px;
  }
  .box-title {
    font-size: 1rem;
    margin-bottom: 12px;
  }
  .art-row {
    font-size: 0.85rem;
    padding: 10px 0;
  }
  .view-toggle-pills {
    padding: 0 6px;
    margin: 10px 0 20px 0;
  }
  .pill-btn-ion {
    height: 44px;
    font-size: 0.85rem;
  }
}
</style>
