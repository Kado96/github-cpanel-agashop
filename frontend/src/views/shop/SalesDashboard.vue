<!--
  * @file SalesDashboard.vue
  * @description Page pour la gestion de Sales Dashboard.
  * @author Kora Agency
-->
<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="secondary">
        <ion-buttons slot="start">
          <ion-button id="back-to-shop" name="back-to-shop" @click="$router.push({ name: 'shop' })">
            <ion-icon color="light" size="large" :icon="arrowBackOutline || 'arrow-back-outline'"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title color="light">
          <div class="header-title-container">
            <span>Ventes</span>
          </div>
        </ion-title>
      </ion-toolbar>
      <ion-progress-bar v-if="loading" type="indeterminate" color="success"></ion-progress-bar>
    </ion-header>

    <ion-content class="sales-dashboard-content">
      <!-- 1. Header Card: Totals -->
      <div class="summary-box">
        <h2 class="summary-title">Mes Ventes effectuées</h2>
        <div class="summary-row">
          <span class="summary-label">Cette Semaine :</span>
          <span class="summary-value red-text">{{ money(weeklyTotal) }} BIF</span>
        </div>
        <div class="summary-row">
          <span class="summary-label">Année {{ currentYear }} :</span>
          <span class="summary-value red-text">{{ money(yearlyTotal) }} BIF</span>
        </div>
      </div>

      <!-- 2. Action Buttons (DESIGN ORIGINAL RESTAURÉ) -->
      <div class="actions-group">
        <ion-button expand="block" fill="outline" color="dark" class="btn-rect" @click="viewHistory">
          Historiques
        </ion-button>
      </div>

      <!-- 3. Donut Chart Section -->
      <div class="chart-area" v-if="currentView === 'donut'">
        <div class="donut-wrapper">
          <svg viewBox="0 0 100 100" class="donut-svg-main">
            <!-- Background track (very light) -->
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
            
            <!-- Label Text on Segments (Masqué si trop étroit pour éviter les superpositions) -->
            <g v-for="(segment, index) in chartSegments" :key="'label-'+index">
               <template v-if="(segment.value / totalValue) >= 0.08">
                 <!-- Value -->
                 <text :x="segment.labelX" :y="segment.labelY - 1" class="val-text" text-anchor="middle">
                   {{ money(segment.value) }}
                 </text>
                 <!-- Month -->
                 <text :x="segment.labelX" :y="segment.labelY + 3" class="month-text" text-anchor="middle">
                   {{ segment.month }}
                 </text>
               </template>
            </g>

            <!-- Center Text -->
            <text x="50" y="50" class="donut-center-text" text-anchor="middle" dominant-baseline="middle">
              Ventes par Catégorie
            </text>
          </svg>
        </div>

        <!-- Legend -->
        <div class="legend-box">
          <div v-for="(item, index) in sortedSalesData" :key="index" class="legend-pill">
            <span class="pill-dot" :style="{ backgroundColor: item.color }"></span>
            <span class="pill-name">{{ item.month }}</span>
          </div>
          <span class="pill-name-main">Catégories</span>
        </div>
      </div>

      <!-- 3b. Evolution Curve Section -->
      <div class="chart-area curve-chart-container" v-if="currentView === 'curve'">
        <div class="curve-wrapper">
          <svg viewBox="0 0 200 175" class="curve-svg">
            <!-- Axes -->
            <line x1="32" y1="10" x2="32" y2="130" stroke="#ccc" stroke-width="0.5" />
            <line x1="32" y1="130" x2="190" y2="130" stroke="#ccc" stroke-width="0.5" />

            <!-- Y-axis Labels -->
            <g class="y-labels">
              <text v-for="(tick, i) in curveYLabels" :key="i" x="29" :y="130 - (i * 13.33)" text-anchor="end" class="chart-tick-text">
                {{ formatSmallMoney(tick) }}
              </text>
            </g>

            <!-- X-axis Labels -->
            <g class="x-labels">
              <text v-for="(lbl, i) in curveXLabels" :key="i" :x="lbl.x" y="145" text-anchor="middle" class="chart-tick-text">
                {{ lbl.label }}
              </text>
            </g>

            <!-- The Curve (Smooth Path) -->
            <path :d="curvePath" fill="none" stroke="#2B00E1" stroke-width="1.5" stroke-linecap="round" />

            <!-- Legend for Curve -->
            <g transform="translate(32, 162)">
              <rect width="6" height="6" fill="#2B00E1" />
              <text x="10" y="5.5" class="curve-legend-text">Courbe d'évolution des ventes réalisées en {{ currentYear }}</text>
            </g>
            
            <text x="190" y="125" text-anchor="end" class="curve-sub-title">Ventes mensuelles</text>
          </svg>
        </div>
      </div>

      <!-- 4. Toggle Pills -->
      <div class="view-toggle-pills">
        <ion-button :color="currentView === 'donut' ? 'success' : 'light'" class="pill-btn-ion" @click="currentView = 'donut'">
          Diagramme Circulaire
        </ion-button>
        <ion-button :color="currentView === 'curve' ? 'success' : 'light'" class="pill-btn-ion" @click="currentView = 'curve'">
          Courbe évolution
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
  IonProgressBar,
  IonBackButton,
  IonRow,
  IonCol,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle
} from '@ionic/vue';
import { arrowBackOutline, chevronForwardOutline, cartOutline } from 'ionicons/icons';
import { salesService } from '../../services/api/sales';

const MONTH_NAMES = [
  'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
];

const MONTH_COLORS = [
  '#E55F55', '#D26B7B', '#109618', '#00E5FF', '#7EAB9F', '#B088FF',
  '#FF9800', '#795548', '#607D8B', '#9C27B0', '#3F51B5', '#F44336'
];

/**
 * Composant SalesDashboard
 * - Gère l'interface et la logique métier de Sales Dashboard.
 */
export default {
  name: 'SalesDashboard',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonButtons,
    IonButton,
    IonTitle,
    IonContent,
    IonIcon,
    IonProgressBar,
    IonBackButton,
    IonRow,
    IonCol,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle
  },
  data() {
    return {
      arrowBackOutline,
      chevronForwardOutline,
      cartOutline,
      currentView: 'donut',
      weeklyTotal: 0,
      yearlyTotal: 0,
      salesData: [],
      monthlyEvolutionData: [],
      loading: false,
      currentYear: new Date().getFullYear(),
      shop: this.$store.state.shop
    };
  },
  computed: {
    shopId() {
      return this.$store.state.shop?.id || this.shop?.id;
    },
    totalValue() {
      return this.salesData.reduce((acc, curr) => acc + curr.value, 0);
    },
    sortedSalesData() {
      return [...this.salesData].reverse();
    },
    chartSegments() {
      if (this.totalValue === 0) return [];
      let cumulativePercent = 0;
      const radius = 35;
      const circumference = 2 * Math.PI * radius;

      return this.salesData.map((item) => {
        const percent = (item.value / this.totalValue) * 100;
        const dashArray = `${(percent * circumference) / 100} ${circumference}`;
        const dashOffset = (cumulativePercent * circumference) / 100;

        const angle = ((cumulativePercent + percent / 2) / 100) * 360 - 90;
        const radian = (angle * Math.PI) / 180;
        const labelR = 40; // Augmenté pour éloigner les étiquettes du centre
        const labelX = 50 + labelR * Math.cos(radian);
        const labelY = 50 + labelR * Math.sin(radian);

        cumulativePercent += percent;

        return {
          ...item,
          dashArray,
          dashOffset: -dashOffset,
          labelX,
          labelY
        };
      });
    },
    curveYLabels() {
      const maxVal = this.curveMaxY;
      if (maxVal === 0) return [0];
      const labels = [];
      const step = maxVal / 9;
      for (let i = 0; i <= 9; i++) {
        labels.push(Math.round(i * step));
      }
      return labels;
    },
    curveMaxY() {
      if (this.monthlyEvolutionData.length === 0) return 0;
      const max = Math.max(...this.monthlyEvolutionData.map(d => d.value));
      return max > 0 ? max * 1.15 : 1; 
    },
    curvePath() {
      if (this.monthlyEvolutionData.length === 0) return '';
      const maxY = this.curveMaxY;
      const count = this.monthlyEvolutionData.length;
      const xStep = count > 1 ? 150 / (count - 1) : 150;

      const dataPoints = this.monthlyEvolutionData.map((item, i) => ({
        x: 32 + (i * xStep),
        y: item.value
      }));

      const points = dataPoints.map(p => ({
        x: p.x,
        y: 130 - (p.y / maxY) * 120
      }));

      let d = `M ${points[0].x},${points[0].y}`;
      for (let i = 0; i < points.length - 1; i++) {
        const p0 = points[i];
        const p1 = points[i + 1];
        const cp1x = p0.x + (p1.x - p0.x) / 2;
        const cp2x = p0.x + (p1.x - p0.x) / 2;
        d += ` C ${cp1x},${p0.y} ${cp2x},${p1.y} ${p1.x},${p1.y}`;
      }
      return d;
    },
    curveXLabels() {
      return this.monthlyEvolutionData.map((d, i) => ({
        x: 32 + (i * (this.monthlyEvolutionData.length > 1 ? 150 / (this.monthlyEvolutionData.length - 1) : 150)),
        label: d.label.substring(0, 3) 
      }));
    }
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchDashboardData();
  },
  ionViewWillEnter() {
    // Garder ionViewWillEnter pour le rafraîchissement au retour, mais le coeur est dans beforeMount
    this.fetchDashboardData();
  },
  methods: {
    formatSmallMoney(val) {
      if (val === 0) return '0';
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    },
    viewHistory() { 
      this.$router.push({ name: 'sales-list', query: { readonly: '1' } }); 
    },

    async fetchDashboardData() {
      if (!this.shopId) return;
      this.loading = true;

      const toLocalISO = (date) => {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
      };

      try {
        const now = new Date();
        const year = now.getFullYear();
        this.currentYear = year;

        // 1. Fetch ALL sales for the current year
        const yearStart = `${year}-01-01`;
        const yearEnd = toLocalISO(now);
        const res = await salesService.getSales(this.shopId, {
          created_at__gte: yearStart,
          created_at__lte: yearEnd,
          limit: 1000 
        });
        const allSales = res.data.results || res.data || [];

        // 2. Totals
        const weekAgo = new Date(now);
        weekAgo.setDate(now.getDate() - 7);
        const thisWeekSales = allSales.filter(s => new Date(s.created_at) >= weekAgo);
        
        this.weeklyTotal = thisWeekSales.reduce((sum, s) => sum + (parseFloat(s.amount) || 0), 0);
        this.yearlyTotal = allSales.reduce((sum, s) => sum + (parseFloat(s.amount) || 0), 0);

        // 3. Breakdown by CATEGORY (for Donut)
        const catMap = {};
        allSales.forEach(s => {
          // Attempt to find category name in nested items
          let catName = "Autres";
          if (s.items && s.items.length > 0) {
            catName = s.items[0].product?.sub_category?.category?.name || s.items[0].product?.category?.name || "Autres";
          }
          if (!catMap[catName]) catMap[catName] = 0;
          catMap[catName] += parseFloat(s.amount) || 0;
        });

        this.salesData = Object.keys(catMap).map((label, i) => ({
          month: label, 
          value: catMap[label],
          color: MONTH_COLORS[i % MONTH_COLORS.length]
        })).sort((a,b) => b.value - a.value);

        // 4. Monthly Evolution (for Curve)
        const monthlyEv = [];
        for (let i = 5; i >= 0; i--) {
          const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
          const m = d.getMonth();
          const y = d.getFullYear();
          
          const monthTotal = allSales
            .filter(s => {
              const sd = new Date(s.created_at);
              return sd.getMonth() === m && sd.getFullYear() === y;
            })
            .reduce((sum, s) => sum + (parseFloat(s.amount) || 0), 0);

          monthlyEv.push({
            label: MONTH_NAMES[m],
            value: monthTotal
          });
        }
        this.monthlyEvolutionData = monthlyEv;

      } catch (err) {
        console.error("[SalesDashboard] Erreur:", err);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.sales-dashboard-content {
  --background: #cbd5e1;
}

/* 1. Header Box as Premium Card */
.summary-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 24px 16px;
  margin: 16px 12px;
  text-align: center;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
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
  color: var(--ion-color-secondary);
}

.red-text {
  color: #ef4444;
}

/* 2. Action Buttons */
.actions-group {
  padding: 0 12px;
  margin-bottom: 20px;
}

.btn-rect {
  --background: #fff;
  --border-color: #e2e8f0;
  --border-style: solid;
  --border-width: 1px;
  --border-radius: 14px;
  --color: #334155;
  margin: 0;
  height: 54px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  
  &:active {
    --background: #f8fafc;
  }
}


/* 3. Donut Chart Section as Card */
.chart-area {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 24px 16px;
  margin: 0 12px 20px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
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
  border: 1px solid #cbd5e1;
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

/* 4. Switch Toggle */
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

/* Curve Chart Styles */
.curve-chart-container {
  padding: 20px 10px;
}

.curve-wrapper { width: 100%; height: auto; }
.curve-svg { width: 100%; height: auto; }
.chart-tick-text { font-size: 9px; fill: #64748b; font-weight: 600; }
.curve-legend-text { font-size: 8px; fill: #1e293b; font-weight: 700; }
.curve-sub-title { font-size: 9px; fill: #0f172a; font-weight: 800; }

@media (max-width: 360px) {
  .donut-wrapper { max-width: 260px; }
  .summary-title { font-size: 1.2rem; }
}
</style>
