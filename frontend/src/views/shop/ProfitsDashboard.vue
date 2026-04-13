<!--
  * @file ProfitsDashboard.vue
  * @description Page pour la gestion de Profits Dashboard.
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
            <span>Bénéfices</span>
          </div>
        </ion-title>
      </ion-toolbar>
      <ion-progress-bar v-if="loading" type="indeterminate" color="success"></ion-progress-bar>
    </ion-header>

    <ion-content class="profits-dashboard-content">
      <!-- 1. Header Card: Totals -->
      <div class="summary-banner">
        <h2 class="summary-title">Rapport de Rentabilité</h2>
        
        <div class="summary-sections">
          <div class="summary-box">
            <span class="box-label">Cette Semaine</span>
            <div class="box-details">
              <div class="detail-row">
                <span>Marge :</span>
                <span class="green-text">+{{ money(weeklyProfitSales) }}</span>
              </div>
              <div class="detail-row">
                <span>Dépenses :</span>
                <span class="red-text">-{{ money(weeklyExpenses) }}</span>
              </div>
              <div class="detail-divider"></div>
              <div class="detail-row result">
                <span>Net :</span>
                <span :class="weeklyTrueNet >= 0 ? 'green-text' : 'red-text'">
                  {{ weeklyTrueNet >= 0 ? '' : '-' }}{{ money(Math.abs(weeklyTrueNet)) }}
                </span>
              </div>
            </div>
          </div>

          <div class="vertical-divider"></div>

          <div class="summary-box">
            <span class="box-label">Année {{ currentYear }}</span>
            <div class="box-details">
              <div class="detail-row">
                <span>Marge :</span>
                <span class="green-text">+{{ money(yearlyProfitSales) }}</span>
              </div>
              <div class="detail-row">
                <span>Dépenses :</span>
                <span class="red-text">-{{ money(yearlyExpenses) }}</span>
              </div>
              <div class="detail-divider"></div>
              <div class="detail-row result">
                <span>Net :</span>
                <span :class="yearlyTrueNet >= 0 ? 'green-text' : 'red-text'">
                  {{ yearlyTrueNet >= 0 ? '' : '-' }}{{ money(Math.abs(yearlyTrueNet)) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Action Buttons -->
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
            
            <!-- Segments (only for positive values to simplify donut) -->
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
              <template v-if="segment.percent >= 8">
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
              Bénéfices mensuels
            </text>
          </svg>
        </div>

        <!-- Legend -->
        <div class="legend-box">
          <div v-for="(item, index) in sortedProfitsData" :key="index" class="legend-pill">
            <span class="pill-dot" :style="{ backgroundColor: item.color }"></span>
            <span class="pill-name">{{ item.month }}</span>
          </div>
          <span class="pill-name-main">Mois</span>
        </div>
      </div>

      <!-- 3b. Evolution Curve Section -->
      <div class="chart-area curve-chart-container" v-if="currentView === 'curve'">
        <div class="curve-wrapper">
          <svg viewBox="0 0 215 175" class="curve-svg">
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

            <!-- The Curve -->
            <path :d="curvePath" fill="none" stroke="#6c5ce7" stroke-width="1.5" stroke-linecap="round" />

            <!-- Legend for Curve -->
            <g transform="translate(32, 162)">
              <rect width="6" height="6" fill="#6c5ce7" />
              <text x="10" y="5.5" class="curve-legend-text">Courbe d'évolution des bénéfices en {{ currentYear }}</text>
            </g>
            
            <text x="190" y="125" text-anchor="end" class="curve-sub-title">Bénéfices</text>
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
  IonProgressBar
} from '@ionic/vue';
import { arrowBackOutline } from 'ionicons/icons';
import { salesService } from '../../services/api/sales';
import { expensesService } from '../../services/api/expenses';
import { suppliesService } from '../../services/api/supplies';
import { shopsService } from '../../services/api/shops';

const MONTH_NAMES = [
  'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
];

const MONTH_COLORS = [
  '#E55F55', '#D26B7B', '#109618', '#00E5FF', '#7EAB9F', '#B088FF',
  '#FF9800', '#795548', '#607D8B', '#9C27B0', '#3F51B5', '#F44336'
];

/**
 * Composant ProfitsDashboard
 * - Gère l'interface et la logique métier de Profits Dashboard.
 */
export default {
  name: 'ProfitsDashboard',
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
      weeklyTotal: 0,
      weeklyProfitSales: 0,
      weeklyExpenses: 0,
      yearlyTotal: 0,
      yearlySales: 0,
      yearlyExpenses: 0,
      yearlyProfitSales: 0,
      profitsData: [],
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
    totalPositiveValue() {
      return this.profitsData.reduce((acc, curr) => acc + (curr.value > 0 ? curr.value : 0), 0);
    },
    weeklyTrueNet() {
      // Pour être sûr du signe affiché dans le Net
      return this.weeklyProfitSales - this.weeklyExpenses;
    },
    yearlyTrueNet() {
      return this.yearlyProfitSales - this.yearlyExpenses;
    },
    sortedProfitsData() {
      return [...this.profitsData].sort((a,b) => b.value - a.value);
    },
    chartSegments() {
      const totalValue = this.yearlyProfitSales; // Use yearlyProfitSales as the base for the donut chart
      const expenses = this.yearlyExpenses;
      
      if (totalValue <= 0 && expenses <= 0) return [];
      
      // On compare la Marge avec ce qui est consommé par les Dépenses
      const parts = [
        { label: 'Marge Consommée (Dépenses)', value: expenses, color: '#F44336' },
        { label: 'Marge Restante (Bénéfice Net)', value: Math.max(0, this.yearlyTotal), color: '#4CAF50' }
      ];

      let cumulativePercent = 0;
      const radius = 35;
      const circumference = 2 * Math.PI * radius;

      return parts.map((item) => {
        const percent = totalValue > 0 ? (item.value / totalValue) * 100 : 0;
        const dashArray = `${(percent * circumference) / 100} ${circumference}`;
        const dashOffset = (cumulativePercent * circumference) / 100;

        const angle = ((cumulativePercent + percent / 2) / 100) * 360 - 90;
        const radian = (angle * Math.PI) / 180;
        const labelR = 40; 
        const labelX = 50 + labelR * Math.cos(radian);
        const labelY = 50 + labelR * Math.sin(radian);

        cumulativePercent += percent;

        return {
          month: item.label,
          value: item.value,
          percent: percent,
          color: item.color,
          dashArray,
          dashOffset: -dashOffset,
          labelX,
          labelY
        };
      });
    },
    curveYLabels() {
      const maxVal = this.curveMaxY;
      const minVal = this.curveMinY;
      const range = maxVal - minVal;
      if (range === 0) return [minVal];
      
      const labels = [];
      const step = range / 9;
      for (let i = 0; i <= 9; i++) {
        labels.push(Math.round(minVal + (i * step)));
      }
      return labels;
    },
    curveMaxY() {
      if (this.profitsData.length === 0) return 0;
      const values = this.profitsData.map(d => d.value);
      const max = Math.max(...values, 0);
      return max > 0 ? max * 1.15 : 1000; 
    },
    curveMinY() {
      if (this.profitsData.length === 0) return 0;
      const values = this.profitsData.map(d => d.value);
      const min = Math.min(...values, 0);
      return min < 0 ? min * 1.15 : 0;
    },
    curvePath() {
      if (this.profitsData.length === 0) return '';
      const maxY = this.curveMaxY;
      const minY = this.curveMinY;
      const range = maxY - minY;
      const count = this.profitsData.length;
      const xStep = count > 1 ? 150 / (count - 1) : 150;

      const points = this.profitsData.map((item, i) => ({
        x: 32 + (i * xStep),
        y: 130 - ((item.value - minY) / range) * 120
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
      return this.profitsData.map((d, i) => ({
        x: 32 + (i * (this.profitsData.length > 1 ? 150 / (this.profitsData.length - 1) : 150)),
        label: d.month
      }));
    }
  },
  beforeMount() {
    this.shop = this.getShopFromLocalStorage();
    this.$store.state.shop = this.shop;
    this.fetchDashboardData();
  },
  ionViewWillEnter() {
    this.fetchDashboardData();
  },
  methods: {
    formatSmallMoney(val) {
      if (val === 0) return '0';
      return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    },
    viewHistory() { 
      this.$router.push({ name: 'profits-list' }); 
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
        const todayStr = toLocalISO(now);

        // 1. Fetch Summary Stats from Backend (plus fiable)
        const weekAgo = new Date(now);
        weekAgo.setDate(now.getDate() - 7);
        const weekAgoStr = toLocalISO(weekAgo);
        const yearStartStr = `${year}-01-01`;

        const [weekRes, yearRes] = await Promise.all([
          shopsService.getShopStats(this.shopId, { created_at__gte: weekAgoStr, created_at__lte: todayStr }),
          shopsService.getShopStats(this.shopId, { created_at__gte: yearStartStr, created_at__lte: todayStr })
        ]);

        const wD = weekRes.data || {};
        const yD = yearRes.data || {};

        this.weeklyProfitSales = wD.b_sales || 0;
        this.weeklyExpenses = wD.total_general_expenses || 0;
        this.weeklyTotal = wD.total_profit || 0;

        this.yearlySales = yD.sales?.total_amount || 0;
        this.yearlyProfitSales = yD.b_sales || 0;
        this.yearlyExpenses = yD.total_general_expenses || 0;
        this.yearlyTotal = yD.total_profit || 0;

        // 2. Fetch all sales/expenses for the yearly evolution curve
        const [ySalesRes, yExpRes] = await Promise.all([
          salesService.getSales(this.shopId, { created_at__gte: yearStartStr, created_at__lte: todayStr, limit: 1000 }),
          expensesService.getExpenses(this.shopId, { expense_date__gte: yearStartStr, expense_date__lte: todayStr, limit: 1000 })
        ]);

        const allSales = ySalesRes.data.results || ySalesRes.data || [];
        const allExp = yExpRes.data.results || yExpRes.data || [];

        // 3. Monthly breakdown for Evolution Curve
        const evolution = [];
        for (let i = 5; i >= 0; i--) {
          const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
          const m = d.getMonth();
          const y = d.getFullYear();
          
          const sT = allSales.filter(s => { const sd = new Date(s.created_at); return sd.getMonth() === m && sd.getFullYear() === y; });
          const mProfitSales = sT.reduce((sum, s) => {
            const qty = parseFloat(s.quantity) || 0;
            const amount = parseFloat(s.amount) || 0;
            const bP = parseFloat(s.buy_price || s.product?.buy_price) || 0;
            return sum + (amount - (bP * qty)); // Formule alignée backend
          }, 0);

          const eT = allExp.filter(e => { const ed = new Date(e.expense_date); return ed.getMonth() === m && ed.getFullYear() === y; })
                      .reduce((sum, e) => sum + (parseFloat(e.amount) || 0), 0);

          evolution.push({
            label: MONTH_NAMES[m],
            value: mProfitSales - eT
          });
        }
        this.monthlyEvolutionData = evolution;
        
        // Données du graphique Donut
        this.profitsData = [
          { month: 'Dépenses', value: this.yearlyExpenses, color: '#F44336' },
          { month: 'Bénéfice Net', value: Math.max(0, this.yearlyTotal), color: '#4CAF50' }
        ];
      } catch (err) {
        console.error("[ProfitsDashboard] Erreur:", err);
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
.profits-dashboard-content {
  --background: #cbd5e1;
}

.summary-banner {
  background: white;
  margin: 16px;
  border-radius: 20px;
  padding: 24px 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  text-align: center;
  border: 1.5px solid #e2e8f0;
}

.summary-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 24px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-sections {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.summary-box {
  flex: 1;
}

.box-label {
  display: block;
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 700;
  margin-bottom: 14px;
}

.box-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  font-weight: 600;
}

.detail-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 6px 0;
}

.detail-row.result {
  font-weight: 800;
  font-size: 1rem;
}

.vertical-divider {
  width: 1.5px;
  height: 90px;
  background: #f1f5f9;
}

.green-text { color: #10b981; }
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

.curve-chart-container {
  padding: 20px 10px;
}

.curve-wrapper { width: 100%; height: auto; }
.curve-svg { width: 100%; height: auto; }
.chart-tick-text { font-size: 9px; fill: #64748b; font-weight: 600; }
.curve-legend-text { font-size: 8px; fill: #1e293b; font-weight: 700; }
.curve-sub-title { font-size: 9px; fill: #0f172a; font-weight: 800; }

.header-title-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

@media (max-width: 360px) {
  .donut-wrapper { max-width: 260px; }
  .summary-title { font-size: 1.2rem; }
}
</style>
