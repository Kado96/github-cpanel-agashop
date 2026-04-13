<!--
  * @file ContextualHelpBot.vue
  * @description Page pour la gestion de Contextual Help Bot.
  * @author Kora Agency
-->
<template>
  <div v-if="visible" class="contextual-help-container" :class="{'has-fab': hasPageFab}">
    <!-- Floating Action Button -->
    <div class="fab-container ion-activatable ripple-parent" @click="toggleChat">
      <div class="fab-circle">
        <ion-icon :icon="helpCircleOutline" class="help-icon"></ion-icon>
      </div>
      <ion-ripple-effect></ion-ripple-effect>
    </div>

    <!-- Chat Modal / Popover -->
    <transition name="pop-up">
      <div v-if="isOpen" class="chat-window">
        <!-- Header -->
        <div class="chat-header">
          <div class="header-info">
            <div class="avatar-circle">
              <ion-icon :icon="personCircleOutline"></ion-icon>
            </div>
            <div class="header-text">
              <h3>Assistant AgaShop</h3>
              <span class="status-dot"></span> <span class="status-text">En ligne</span>
            </div>
          </div>
          <button class="close-btn" @click="toggleChat">
            <ion-icon :icon="closeOutline"></ion-icon>
          </button>
        </div>

        <!-- Body -->
        <!-- Body -->
        <div class="chat-body" ref="chatBody">
          <!-- Initial Welcome -->
          <div class="message bot-message">
            <p>Bonjour ! 👋 Je suis votre assistant personnel. J'ai préparé pour vous un guide complet de cet écran ci-dessous.</p>
          </div>

          <!-- Dynamic Conversation (Contains the auto-manual and follow-ups) -->
          <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.isUser ? 'user-message' : 'bot-message']">
            <p>{{ msg.text }}</p>
          </div>

          <!-- Persistent Guide (Restored) -->
          <div v-if="pageContext && pageContext.elements && pageContext.elements.length > 0" class="message bot-message help-guide" style="margin-top: 10px;">
             <p style="margin-bottom:6px; color:#666; font-size:11px; text-transform:uppercase; font-weight:700;">Accès rapide aux détails :</p>
             <ul class="help-list">
                <li v-for="(el, idx) in pageContext.elements" :key="idx" class="help-item" @click="askAbout(el)">
                    <span class="help-badge">{{ el.type }}</span> <span class="font-bold">{{ el.label }}</span>
                </li>
             </ul>
             <p style="font-size:11px; color:#666; margin-top:8px; font-style:italic;">Cliquez sur un bouton pour avoir son explication complète.</p>
          </div>
          
          <div v-if="isTyping" class="message bot-message typing-indicator">
            <span>.</span><span>.</span><span>.</span>
          </div>
        </div>

        <!-- Input Area -->
        <div class="chat-footer">
          <input 
            id="bot-message-input"
            name="bot-message-input"
            type="text" 
            v-model="userQuery" 
            @keyup.enter="sendMessage" 
            placeholder="Posez une question supplémentaire..."
          />
          <button class="send-btn" @click="sendMessage" :disabled="!userQuery.trim()">
            <ion-icon :icon="sendOutline"></ion-icon>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { IonIcon, IonRippleEffect } from '@ionic/vue';
import { helpCircleOutline, closeOutline, personCircleOutline, sendOutline } from 'ionicons/icons';

/**
 * Composant ContextualHelpBot
 * - Gère l'interface et la logique métier de Contextual Help Bot.
 */
export default {
  name: 'ContextualHelpBot',
  components: { IonIcon, IonRippleEffect },
  data() {
    return {
      helpCircleOutline,
      closeOutline,
      personCircleOutline,
      sendOutline,
      isOpen: false,
      visible: true,
      userQuery: '',
      messages: [],
      isTyping: false
    };
  },
  computed: {
    helpContext() {
      return this.$store.state.helpContext;
    },
    pageContext() {
      return this.helpContext || {
        title: 'Accueil',
        description: 'Bienvenue sur AgaShop. Naviguez pour explorer votre espace de gestion.'
      };
    },
    hasPageFab() {
      // Pages known to have elements at the bottom (FAB or large primary buttons)
      const fabRoutes = [
        'expenses-list', 'active-articles-list', 'manage-basic-products',
        'profits-dashboard', 'sales-dashboard', 'expenses-dashboard', 
        'stock-volume-dashboard', 'active-articles-dashboard', 'critical-articles-dashboard'
      ];
      const currentRoute = this.$route.name;
      return fabRoutes.includes(currentRoute) || (this.pageContext && this.pageContext.elements && this.pageContext.elements.some(el => el.type === 'Bouton (+)' || el.desc.includes('Flottant')));
    }
  },
  watch: {
    helpContext: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal?.title !== oldVal?.title) {
          this.initContextualGuide();
        }
      }
    }
  },
  methods: {
    initContextualGuide() {
      const ctx = this.pageContext;
      this.messages = [];
      
      // On génère immédiatement le guide de référence complet
      let fullGuide = `Bienvenue ! Je vais vous présenter l'écran "${ctx.title}" en détail pour que vous puissiez l'utiliser immédiatement.\n\n`;
      fullGuide += `CE QUE VOUS DEVEZ SAVOIR :\n${ctx.description}\n\n`;
      
      if (ctx.elements && ctx.elements.length > 0) {
          fullGuide += `LES FONCTIONNALITÉS CLÉS :\n`;
          ctx.elements.forEach(el => {
              fullGuide += `\n• ${el.label} : ${el.desc}`;
          });
      }
      
      if (ctx.faq && ctx.faq.length > 0) {
          fullGuide += `\n\nASTUCES ET SOLUTIONS :\n`;
          ctx.faq.forEach(f => {
              fullGuide += `\n- ${f.question} : ${f.answer}`;
          });
      }

      fullGuide += `\n\nVous avez maintenant toutes les clés en main. Si vous avez besoin d'un éclaircissement sur un point précis, cliquez sur les badges ci-dessous ou écrivez-moi !`;
      
      this.messages.push({ text: fullGuide, isUser: false });
    },
    toggleChat() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        // Au lieu de défiler vers le bas, on s'assure de voir le début du guide
        this.$nextTick(() => {
            const el = this.$refs.chatBody;
            if (el) el.scrollTop = 0;
        });
      }
    },
    scrollToLastMessage() {
      const scrollLogic = () => {
        const el = this.$refs.chatBody;
        if (el) {
          const messages = el.querySelectorAll('.message:not(.typing-indicator)');
          if (messages.length > 0) {
            // Pour afficher l'interaction complète (User + Bot) comme sur la photo :
            // On cible l'avant-dernier message (celui de l'utilisateur) s'il existe.
            const targetIndex = messages.length >= 2 ? messages.length - 2 : messages.length - 1;
            const targetMsg = messages[targetIndex];
            
            targetMsg.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }
        }
      };
      this.$nextTick(scrollLogic);
      setTimeout(scrollLogic, 50);
    },
    askAbout(element) {
        // Trigger a deep dive for the specific element
        this.userQuery = `Explique-moi tout sur "${element.label}"`;
        this.sendMessage();
    },
    sendMessage() {
      if (!this.userQuery || !this.userQuery.trim()) return;

      const query = this.userQuery;
      this.messages.push({ text: query, isUser: true });
      this.userQuery = '';
      
      this.$nextTick(() => {
        this.scrollToLastMessage();
      });

      this.isTyping = true;

      // Simulate AI response with a more "thinking" delay
      setTimeout(() => {
        const response = this.getAnswerFor(query);
        this.messages.push({ text: response, isUser: false });
        this.isTyping = false;
        this.$nextTick(() => {
          this.scrollToLastMessage();
        });
      }, 1000);
    },
    getAnswerFor(query) {
      const lowerQ = query.toLowerCase().trim();
      const ctx = this.pageContext;

      // --- 1. CORE PERSONALITY & SMALL TALK (ChatGPT Style) ---
      
      const greetings = ['bonjour', 'salut', 'coucou', 'hello', 'hey'];
      if (greetings.some(g => lowerQ === g || lowerQ.startsWith(g + ' '))) {
        return "Bonjour ! Je suis l'Assistant intelligent d'AgaShop. 👋 Je connais cette application par cœur. Comment puis-je vous aider à optimiser votre commerce aujourd'hui ?";
      }

      if (lowerQ.includes('qui es-tu') || lowerQ.includes('ton nom')) {
        return "Je suis l'Assistant AgaShop, votre conseiller business intégré. Contrairement à une aide classique, je comprends le contexte de ce que vous faites pour vous guider vers la rentabilité.";
      }

      if (lowerQ === 'merci' || lowerQ.includes('merci beaucoup')) {
        return "Je vous en prie ! C'est un plaisir de vous aider à faire grandir votre boutique. Autre chose ?";
      }

      if (lowerQ.includes('ca va') || lowerQ.includes('comment vas-tu')) {
        return "Je fonctionne à plein régime ! Prêt à analyser vos stocks ou vos ventes. Et vous, comment se passe votre journée de vente ?";
      }

      // --- 2. AGASHOP GLOBAL KNOWLEDGE (Universal Fallbacks) ---
      
      const knowledgeBase = [
        {
          keys: ['stock', 'produit', 'article', 'inventaire'],
          answer: "La gestion des **Stocks** est le cœur d'AgaShop. Vous devez d'abord créer vos produits dans le menu 'Produits', puis enregistrer vos 'Achats' pour augmenter les quantités. Un bon commerçant fait un 'Contrôle' d'inventaire chaque semaine !"
        },
        {
          keys: ['vente', 'vendre', 'caisse', 'encaissement'],
          answer: "Pour réaliser une **Vente**, utilisez le terminal de vente (POS). Sélectionnez vos articles, ajustez les quantités et validez. Le système calculera votre bénéfice net instantanément si vous avez bien renseigné vos prix d'achat."
        },
        {
          keys: ['argent', 'bénéfice', 'profit', 'perte', 'statistique', 'stats'],
          answer: "Vos **Statistiques** vous montrent la vérité financière. Le bénéfice est calculé selon la formule : `Ventes - (Achats + Dépenses)`. Le mode Premium vous offre des graphiques détaillés pour piloter votre croissance."
        },
        {
          keys: ['dépense', 'charge', 'frais', 'loyer', 'facture'],
          answer: "N'oubliez jamais de noter vos **Dépenses** (loyer, électricité, sacs). C'est le seul moyen pour qu'AgaShop calcule votre bénéfice NET réel et non juste votre chiffre d'affaires."
        },
        {
          keys: ['premium', 'abonnement', 'payer', 'essai', 'gratuit'],
          answer: "Le mode **Premium** débloque la puissance illimitée : export PDF pour la comptabilité, gestion multi-utilisateurs et analyses avancées. Vous pouvez demander une activation à votre agent directement depuis l'accueil."
        }
      ];

      // --- 3. CONTEXTUAL MATCHING (Page Specific) ---

      // Deep dive request
      if (lowerQ.includes('explique tout') || lowerQ.includes('tous les détails') || lowerQ.includes('aide moi')) {
          let fullGuide = `D'accord, je vous explique tout sur l'écran "${ctx.title}".\n\n`;
          fullGuide += `Votre objectif ici : ${ctx.description}\n\n`;
          
          if (ctx.elements && ctx.elements.length > 0) {
              fullGuide += `Les outils à votre disposition :\n`;
              ctx.elements.forEach(el => {
                  fullGuide += `\n• ${el.label} : ${el.desc}`;
              });
          }
          
          if (ctx.faq && ctx.faq.length > 0) {
              fullGuide += `\n\nQuestions fréquentes :\n`;
              ctx.faq.forEach(f => {
                  fullGuide += `\n- ${f.question} : ${f.answer}`;
              });
          }

          fullGuide += `\n\nVoulez-vous que j'approfondisse un de ces points ?`;
          return fullGuide;
      }

      // Specific Element Search
      if (ctx.elements) {
        const foundEl = ctx.elements.find(el => lowerQ.includes(el.label.toLowerCase()));
        if (foundEl) {
            return `Précisions sur "${foundEl.label}" : \n\n${foundEl.desc}\n\nC'est un élément clé de cet écran. Avez-vous une autre question ?`;
        }
      }

      // --- 4. GLOBAL KNOWLEDGE MATCHING ---
      const globalMatch = knowledgeBase.find(k => k.keys.some(key => lowerQ.includes(key)));
      if (globalMatch) return globalMatch.answer;

      // --- 5. FALLBACK (ChatGPT Style) ---
      return "Je ne suis pas sûr de comprendre cette demande spécifique. Je suis spécialisé dans la gestion de votre boutique AgaShop. 📊\n\nVous pouvez me demander :\n• \"Explique tout\" pour ce menu\n• Des infos sur vos stocks, ventes ou bénéfices\n• Comment passer en Premium";
    }
  }
};
</script>

<style scoped>
.contextual-help-container {
  position: fixed;
  bottom: 15px; /* Légèrement plus bas pour laisser de la place au FAB au-dessus */
  right: 15px;
  z-index: 10000;
  font-family: 'Outfit', sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}

.contextual-help-container * {
  pointer-events: auto;
}

/* FAB Styling - Premium & Subtle */
.fab-container {
  position: relative;
  width: 56px;
  height: 56px;
  cursor: pointer;
  border-radius: 18px;
  background: #1e293b;
  box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  overflow: hidden;
}

.fab-container:hover {
  transform: translateY(-4px) scale(1.05);
  background: #0f172a;
}

.help-icon {
  font-size: 28px;
  color: white;
}

/* Chat Window Styling - Matching Dashboard Cards */
.chat-window {
  position: absolute;
  bottom: 70px; /* S'ouvre juste au-dessus du bouton d'aide */
  right: 0;
  width: calc(100vw - 40px);
  max-width: 380px;
  height: calc(100vh - 120px);
  max-height: 580px;
  background: #ffffff;
  border-radius: 28px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1.5px solid #e2e8f0;
  transform-origin: bottom right;
}

/* Header - Modern & Clean */
.chat-header {
  background: white;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1.5px solid #f1f5f9;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-circle {
  width: 38px;
  height: 38px;
  background: #f1f5f9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.header-text h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.status-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  background: #10b981;
  border-radius: 50%;
  margin-right: 6px;
}

.status-text {
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.close-btn {
  background: #f8fafc;
  border: none;
  color: #94a3b8;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover { background: #fee2e2; color: #ef4444; }

/* Body - Soft Contrast */
.chat-body {
  flex: 1;
  padding: 20px 16px;
  overflow-y: auto;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.message {
  max-width: 88%;
  padding: 14px 18px;
  font-size: 0.9rem;
  line-height: 1.6;
  white-space: pre-wrap;
}

.bot-message {
  align-self: flex-start;
  background: white;
  color: #334155;
  border: 1.5px solid #e2e8f0;
  border-radius: 20px 20px 20px 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  font-weight: 500;
}

.user-message {
  align-self: flex-end;
  background: #1e293b;
  color: white;
  border-radius: 20px 20px 6px 20px;
  font-weight: 600;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Help Guide - Matching Dashboard Styles */
.help-guide {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  padding: 16px !important;
}

.help-list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0 0;
}

.help-item {
  padding: 0 16px;
  height: 52px;
  background: white;
  border: 1.5px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.9rem;
  border-radius: 14px; /* Matching btn-rect */
  margin-bottom: 8px;
  font-weight: 700;
  color: #334155;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.help-item:hover {
  transform: translateX(4px);
  border-color: var(--ion-color-secondary);
  color: var(--ion-color-secondary);
}

.help-item:active {
  transform: scale(0.98);
  background: #f8fafc;
}

.help-badge {
  background: #f1f5f9;
  color: #64748b;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 10px;
  text-transform: uppercase;
  font-weight: 800;
  min-width: 50px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.typing-indicator {
  display: flex;
  gap: 5px;
  padding: 12px 16px;
}

.typing-indicator span {
  width: 7px;
  height: 7px;
  background: #cbd5e1;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.3); opacity: 0.3; }
  40% { transform: scale(1.0); opacity: 1; }
}

/* Footer - Clean Input */
.chat-footer {
  padding: 16px 20px;
  background: white;
  border-top: 1.5px solid #f1f5f9;
  display: flex;
  gap: 12px;
  align-items: center;
}

.chat-footer input {
  flex: 1;
  border: 1.5px solid #e2e8f0;
  padding: 12px 18px;
  border-radius: 16px;
  outline: none;
  background: #f8fafc;
  color: #0f172a;
  font-size: 0.95rem;
  transition: all 0.2s;
  font-family: inherit;
  font-weight: 500;
}

.chat-footer input:focus {
  border-color: #1e293b;
  background: white;
  box-shadow: 0 0 0 3px rgba(30, 41, 59, 0.05);
}

.send-btn {
  background: #1e293b;
  color: white;
  border: none;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.send-btn:hover { background: #0f172a; transform: scale(1.05); }
.send-btn:disabled { background: #f1f5f9; color: #cbd5e1; cursor: not-allowed; }

/* Transitions */
.pop-up-enter-active, .pop-up-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-up-enter-from, .pop-up-leave-to {
  opacity: 0;
  transform: scale(0.85) translate(20px, 60px);
}

.chat-body::-webkit-scrollbar { width: 5px; }
.chat-body::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }

.font-bold { font-weight: 800; }
</style>
