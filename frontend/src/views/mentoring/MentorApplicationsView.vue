<template>
  <div class="py-8 px-4">
    <h1 class="text-4xl font-semibold text-gray-800 mb-2">Moji zahtjevi</h1>
    <p class="text-gray-500 mb-6">Upravljajte zahtjevima studentica za mentorstvo</p>

    <div class="flex border-b border-gray-200 mb-8">
      <button
        @click="activeTab = 'pending'"
        :class="[
          'py-3 px-6 font-semibold text-sm border-b-2 transition',
          activeTab === 'pending'
            ? 'border-purple-600 text-purple-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        ]"
      >
        Pristigli zahtjevi ({{ pendingApplications.length }})
      </button>
      <button
        @click="activeTab = 'active'"
        :class="[
          'py-3 px-6 font-semibold text-sm border-b-2 transition',
          activeTab === 'active'
            ? 'border-purple-600 text-purple-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        ]"
      >
        Aktivni odnosi ({{ activeApplications.length }})
      </button>
      <button
        @click="activeTab = 'rejected'"
        :class="[
          'py-3 px-6 font-semibold text-sm border-b-2 transition',
          activeTab === 'rejected'
            ? 'border-purple-600 text-purple-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        ]"
      >
        Odbijeni zahtjevi ({{ rejectedApplications.length }})
      </button>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
      <span class="ml-4 text-gray-500">Učitavanje zahtjeva...</span>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <div v-else class="border border-gray-300 rounded-lg p-6 bg-white">
      
      <div v-if="activeTab === 'pending'">
        <div v-if="pendingApplications.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
          <p class="text-gray-500">Nema novih zahtjeva za sada</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="app in pendingApplications"
            :key="app.id"
            class="bg-white border border-gray-200 rounded-lg p-4 flex items-start gap-4 hover:shadow-md transition"
          >
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                <span class="text-purple-600 font-semibold">{{ getInitials(app.student_name) }}</span>
              </div>
            </div>

            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-gray-800">{{ app.student_name }}</h3>
              <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ app.message }}</p>
              <p class="text-gray-400 text-xs mt-2">{{ formatDate(app.created_at) }}</p>
            </div>

            <div class="flex-shrink-0 flex flex-col gap-2">
              <div class="flex gap-2">
                <button
                  @click="approveApplication(app.id, app)"
                  class="px-4 py-2 bg-white border border-gray-800 text-gray-800 font-semibold rounded hover:bg-gray-800 hover:text-white transition"
                >
                  Prihvati
                </button>
                <button
                  @click="openRejectModal(app)"
                  class="px-4 py-2 bg-gray-400 text-white font-semibold rounded hover:bg-gray-500 transition"
                >
                  Odbij
                </button>
              </div>
              <button
                @click="openDetails(app)"
                class="px-4 py-2 bg-purple-100 border border-purple-300 text-purple-600 font-semibold rounded hover:bg-purple-200 transition whitespace-nowrap"
              >
                Detalji
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'active'">
        <div v-if="activeApplications.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
          <p class="text-gray-500">Nema aktivnih odnosa za sada</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="app in activeApplications"
            :key="app.id"
            class="bg-white border border-gray-200 rounded-lg p-4 flex items-start gap-4"
          >
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                <span class="text-purple-600 font-semibold">{{ getInitials(app.student_name) }}</span>
              </div>
            </div>

            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-gray-800">{{ app.student_name }}</h3>
              <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ app.message }}</p>
              <p class="text-gray-400 text-xs mt-2">{{ formatDate(app.created_at) }}</p>
            </div>

            <div class="flex-shrink-0">
              <button
                disabled
                class="px-4 py-2 bg-green-100 text-green-700 font-semibold rounded cursor-default"
              >
                Aktivan
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'rejected'">
        <div v-if="rejectedApplications.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
          <p class="text-gray-500">Nema odbijenih zahtjeva</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="app in rejectedApplications"
            :key="app.id"
            class="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-4"
          >
            <div class="flex-shrink-0">
              <div class="w-12 h-12 bg-red-200 rounded-full flex items-center justify-center">
                <span class="text-red-600 font-semibold">{{ getInitials(app.student_name) }}</span>
              </div>
            </div>

            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-gray-800">{{ app.student_name }}</h3>
              <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ app.message }}</p>
              <p class="text-gray-400 text-xs mt-2">{{ formatDate(app.created_at) }}</p>
              <div v-if="app.rejection_reason" class="mt-2 p-2 bg-red-100 border-l-4 border-red-500 text-red-700 text-sm rounded">
                <strong>Razlog:</strong> {{ app.rejection_reason }}
              </div>
            </div>

            <div class="flex-shrink-0">
              <button
                disabled
                class="px-4 py-2 bg-red-100 text-red-700 font-semibold rounded cursor-default"
              >
                Odbijen
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMentorApplications, updateApplicationStatus } from '../../services/mentoring.js'

// Dodana varijabla za praćenje aktivnog taba
const activeTab = ref('pending') // Početni tab je 'pending'

const applications = ref([])
const loading = ref(true)
const error = ref(null)
const showDetailsModal = ref(false)
const showRejectModal = ref(false)
const selectedApplication = ref(null)
const appToReject = ref(null)
const rejectionReason = ref('')

const pendingApplications = computed(() => {
  return applications.value.filter(app => app.status === 'PENDING')
})

const activeApplications = computed(() => {
  return applications.value.filter(app => app.status === 'ACCEPTED')
})

const rejectedApplications = computed(() => {
  return applications.value.filter(app => app.status === 'REJECTED')
})

// OSTATAK TVOG SCRIPT SETUP KODA OSTANE POTPUNO ISTI...
const getInitials = (name) => {
  return name.split(' ').map(word => word[0]).join('').toUpperCase().slice(0, 2)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 60) return `prije ${diffMins} min`
  if (diffHours < 24) return `prije ${diffHours}h`
  if (diffDays < 7) return `prije ${diffDays}d`
  
  return date.toLocaleDateString('sr-BA')
}

const formatDateFull = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('sr-BA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const openDetails = (app) => {
  selectedApplication.value = app
  showDetailsModal.value = true
}

const closeDetails = () => {
  showDetailsModal.value = false
  selectedApplication.value = null
}

const openRejectModal = (app) => {
  appToReject.value = app
  rejectionReason.value = ''
  showRejectModal.value = true
}

const closeRejectModal = () => {
  showRejectModal.value = false
  appToReject.value = null
  rejectionReason.value = ''
}

const approveApplication = async (applicationId, app) => {
  try {
    await updateApplicationStatus(applicationId, 'ACCEPTED')
    app.status = 'ACCEPTED'
    closeDetails()
  } catch (err) {
    console.error('Greška pri prihvatanju zahtjeva:', err)
    error.value = 'Nije moguće prihvatiti zahtjev'
  }
}

const confirmReject = async (applicationId) => {
  try {
    await updateApplicationStatus(applicationId, 'REJECTED', rejectionReason.value)
    const app = applications.value.find(a => a.id === applicationId)
    if (app) {
      app.status = 'REJECTED'
      app.rejection_reason = rejectionReason.value
    }
    closeRejectModal()
  } catch (err) {
    console.error('Greška pri odbijanju zahtjeva:', err)
    error.value = 'Nije moguće odbiti zahtjev'
  }
}

onMounted(async () => {
  try {
    const data = await getMentorApplications()
    applications.value = data
  } catch (err) {
    console.error('Greška pri dohvaćanju zahtjeva:', err)
    error.value = 'Nije moguće učitati zahtjeve'
  } finally {
    loading.value = false
  }
})
</script>