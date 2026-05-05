<template>
  <ion-page>
    <ion-header class="ion-no-border">
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-button @click="dismiss(null)">
            <ion-icon slot="icon-only" :icon="arrowBackOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
        <ion-title>Bibliothèque d'images</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="dismiss(null)">
            <ion-icon slot="icon-only" :icon="close"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar color="primary">
        <ion-searchbar 
          placeholder="Rechercher une image..." 
          v-model="searchQuery" 
          @ionInput="onSearch"
          animated
        ></ion-searchbar>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <!-- Upload Section -->
      <div class="upload-section ion-margin-bottom">
        <input
          type="file"
          accept="image/*"
          @change="handleFileUpload"
          style="display: none"
          ref="fileInput"
        />
        <ion-button expand="block" color="secondary" @click="$refs.fileInput.click()" :disabled="uploading">
          <ion-icon slot="start" :icon="cloudUploadOutline"></ion-icon>
          <ion-spinner v-if="uploading" slot="start"></ion-spinner>
          {{ uploading ? 'Téléchargement...' : 'Ajouter une nouvelle image' }}
        </ion-button>
      </div>

      <!-- Media Grid -->
      <ion-grid v-if="mediaItems.length > 0">
        <ion-row>
          <ion-col size="6" size-md="4" size-lg="3" v-for="item in mediaItems" :key="item.id">
            <div class="media-card" :class="{ 'selected': selectedId === item.id }" @click="selectItem(item)">
              <div class="image-container">
                <img :src="item.file" :alt="item.name" loading="lazy" />
              </div>
              <div class="media-info">
                <p class="media-name">{{ item.name || 'Sans nom' }}</p>
              </div>
              <div class="selection-badge" v-if="selectedId === item.id">
                <ion-icon :icon="checkmarkCircle"></ion-icon>
              </div>
            </div>
          </ion-col>
        </ion-row>
      </ion-grid>

      <!-- Empty State -->
      <div v-else-if="!loading" class="empty-state">
        <ion-icon :icon="imageOutline"></ion-icon>
        <p>Aucune image trouvée</p>
        <ion-button fill="clear" @click="searchQuery = ''; fetchMedia()">Réinitialiser</ion-button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <ion-spinner name="crescent"></ion-spinner>
        <p>Chargement des images...</p>
      </div>

      <!-- Infinite Scroll -->
      <ion-infinite-scroll @ionInfinite="loadMore" :disabled="!hasNextPage">
        <ion-infinite-scroll-content loading-text="Chargement de plus d'images..."></ion-infinite-scroll-content>
      </ion-infinite-scroll>
    </ion-content>

    <ion-footer class="ion-no-border" v-if="selectedItem">
      <ion-toolbar class="ion-padding-horizontal">
        <ion-button expand="block" color="success" @click="confirmSelection">
          Confirmer la sélection
        </ion-button>
      </ion-toolbar>
    </ion-footer>
  </ion-page>
</template>

<script>
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonIcon,
  IonContent,
  IonSearchbar,
  IonGrid,
  IonRow,
  IonCol,
  IonSpinner,
  IonFooter,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  modalController
} from '@ionic/vue';
import {
  close,
  arrowBackOutline,
  cloudUploadOutline,
  imageOutline,
  checkmarkCircle,
  search
} from 'ionicons/icons';
import { mediaService } from '../../services/api';

export default {
  name: 'MediaLibrary',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonIcon,
    IonContent,
    IonSearchbar,
    IonGrid,
    IonRow,
    IonCol,
    IonSpinner,
    IonFooter,
    IonInfiniteScroll,
    IonInfiniteScrollContent
  },
  data() {
    return {
      close,
      arrowBackOutline,
      cloudUploadOutline,
      imageOutline,
      checkmarkCircle,
      search,
      mediaItems: [],
      loading: false,
      uploading: false,
      searchQuery: '',
      selectedId: null,
      selectedItem: null,
      currentPage: 1,
      hasNextPage: false,
      pageSize: 20
    };
  },
  mounted() {
    this.fetchMedia();
  },
  methods: {
    async fetchMedia(append = false) {
      if (!append) {
        this.loading = true;
        this.currentPage = 1;
      }
      
      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize,
          search: this.searchQuery
        };
        
        const res = await mediaService.getMedia(params);
        const data = res.data;
        
        if (append) {
          this.mediaItems.push(...(data.results || []));
        } else {
          this.mediaItems = data.results || [];
        }
        
        this.hasNextPage = !!data.next;
      } catch (err) {
        console.error('Erreur lors du chargement des médias:', err);
      } finally {
        this.loading = false;
      }
    },
    
    async loadMore(ev) {
      if (this.hasNextPage) {
        this.currentPage++;
        await this.fetchMedia(true);
      }
      ev.target.complete();
    },
    
    onSearch() {
      // Debounce simple
      if (this.searchTimer) clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.fetchMedia();
      }, 500);
    },
    
    selectItem(item) {
      if (this.selectedId === item.id) {
        this.selectedId = null;
        this.selectedItem = null;
      } else {
        this.selectedId = item.id;
        this.selectedItem = item;
      }
    },
    
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      this.uploading = true;
      const formData = new FormData();
      formData.append('file', file);
      formData.append('name', file.name.split('.')[0]);
      
      try {
        const res = await mediaService.uploadMedia(formData);
        const newItem = res.data;
        this.mediaItems.unshift(newItem);
        this.selectItem(newItem);
        // Réinitialiser l'input file
        this.$refs.fileInput.value = '';
      } catch (err) {
        console.error('Erreur lors du téléchargement:', err);
      } finally {
        this.uploading = false;
      }
    },
    
    confirmSelection() {
      this.dismiss(this.selectedItem);
    },
    
    dismiss(data) {
      modalController.dismiss(data, data ? 'confirm' : 'cancel');
    }
  }
};
</script>

<style scoped>
.media-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #f4f5f8;
  aspect-ratio: 1;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
}

.media-card.selected {
  border-color: var(--ion-color-success);
  transform: scale(0.95);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.image-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.5);
  padding: 4px 8px;
}

.media-name {
  color: white;
  margin: 0;
  font-size: 0.7rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.selection-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  color: var(--ion-color-success);
  font-size: 1.5rem;
  background: white;
  border-radius: 50%;
  display: flex;
}

.empty-state, .loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #8e8e93;
}

.empty-state ion-icon, .loading-state ion-spinner {
  font-size: 4rem;
  margin-bottom: 16px;
}

.upload-section {
  position: sticky;
  top: 0;
  z-index: 10;
  background: white;
}
</style>
