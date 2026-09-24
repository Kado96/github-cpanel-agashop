<template>
  <div class="relative inline-block text-left">
    <!-- Bouton Cloche de Notification -->
    <button
      @click="toggleDropdown"
      class="relative p-2 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white focus:outline-none"
      aria-label="Notifications"
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
        />
      </svg>
      <!-- Badge non lu -->
      <span
        v-if="unreadCount > 0"
        class="absolute top-1 right-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white transform translate-x-1/4 -translate-y-1/4 bg-red-600 rounded-full"
      >
        {{ unreadCount }}
      </span>
    </button>

    <!-- Dropdown / Panneau des Notifications -->
    <div
      v-if="isOpen"
      class="origin-top-right absolute right-0 mt-2 w-80 md:w-96 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 z-50 divide-y divide-gray-100 dark:divide-gray-700"
    >
      <div class="p-3 flex items-center justify-between">
        <h3 class="text-sm font-semibold text-gray-900 dark:text-white">
          Notifications & Controls
        </h3>
        <button
          v-if="unreadCount > 0"
          @click="markAllAsRead"
          class="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 font-medium"
        >
          Tout marquer comme lu
        </button>
      </div>

      <div class="max-h-80 overflow-y-auto divide-y divide-gray-100 dark:divide-gray-700">
        <div
          v-for="item in notifications"
          :key="item.id"
          @click="markAsRead(item)"
          :class="[
            'p-3 cursor-pointer transition hover:bg-gray-50 dark:hover:bg-gray-700',
            !item.is_read ? 'bg-blue-50/50 dark:bg-blue-900/20' : ''
          ]"
        >
          <div class="flex items-start justify-between">
            <span
              :class="[
                'text-xs font-semibold px-2 py-0.5 rounded-full',
                getTypeBadgeClass(item.notification_type)
              ]"
            >
              {{ getTypeLabel(item.notification_type) }}
            </span>
            <span class="text-xs text-gray-400">
              {{ formatDate(item.created_at) }}
            </span>
          </div>
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mt-1">
            {{ item.title }}
          </h4>
          <p class="text-xs text-gray-600 dark:text-gray-300 mt-0.5">
            {{ item.message }}
          </p>
        </div>

        <div
          v-if="notifications.length === 0"
          class="p-4 text-center text-xs text-gray-500 dark:text-gray-400"
        >
          Aucune notification pour le moment.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const notifications = ref([])

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    fetchNotifications()
  }
}

const fetchNotifications = async () => {
  try {
    const res = await axios.get('/api/shops/notifications/')
    notifications.value = res.data.results || res.data
  } catch (err) {
    console.error('Erreur chargement notifications:', err)
  }
}

const markAsRead = async (item) => {
  if (item.is_read) return
  try {
    await axios.post(`/api/shops/notifications/${item.id}/mark_as_read/`)
    item.is_read = true
  } catch (err) {
    console.error('Erreur mark_as_read:', err)
  }
}

const markAllAsRead = async () => {
  try {
    await axios.post('/api/shops/notifications/mark_all_as_read/')
    notifications.value.forEach(n => (n.is_read = true))
  } catch (err) {
    console.error('Erreur mark_all_as_read:', err)
  }
}

const getTypeLabel = (type) => {
  switch (type) {
    case 'CONTROL_DONE': return 'Contrôle'
    case 'SUBSCRIPTION_ACTIVATED': return 'Abonnement'
    case 'SUBSCRIPTION_EXPIRED': return 'Expiration'
    case 'WARNING': return 'Alerte'
    default: return 'Système'
  }
}

const getTypeBadgeClass = (type) => {
  switch (type) {
    case 'CONTROL_DONE': return 'bg-purple-100 text-purple-800'
    case 'SUBSCRIPTION_ACTIVATED': return 'bg-green-100 text-green-800'
    case 'SUBSCRIPTION_EXPIRED': return 'bg-red-100 text-red-800'
    case 'WARNING': return 'bg-yellow-100 text-yellow-800'
    default: return 'bg-blue-100 text-blue-800'
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  fetchNotifications()
})
</script>
