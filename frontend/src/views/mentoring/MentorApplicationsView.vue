<template>
  <div class="py-8 px-4">
    <h1 class="text-4xl font-semibold text-gray-800 mb-2">Moji zahtjevi</h1>
    <p class="text-gray-500 mb-8">Upravljajte zahtjevima studentica za mentorstvo</p>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-purple-600 border-t-transparent"></div>
      <span class="ml-4 text-gray-500">Učitavanje zahtjeva...</span>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <!-- Content -->
    <div v-else class="space-y-8">
      <!-- Main Container -->
      <div class="border border-gray-300 rounded-lg p-6 bg-white">
        <!-- PRISTIGLI ZAHTJEVI Section -->
        <div>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">PRISTIGLI ZAHTJEVI</h2>
          <div v-if="pendingApplications.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
            <p class="text-gray-500">Nema novih zahtjeva za sada</p>
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="app in pendingApplications"
              :key="app.id"
              class="bg-white border border-gray-200 rounded-lg p-4 flex items-start gap-4 hover:shadow-md transition"
            >
              <!-- Avatar placeholder -->
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                  <span class="text-purple-600 font-semibold">{{ getInitials(app.student_name) }}</span>
                </div>
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-gray-800">{{ app.student_name }}</h3>
                <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ app.message }}</p>
                <p class="text-gray-400 text-xs mt-2">{{ formatDate(app.created_at) }}</p>
              </div>

              <!-- Actions -->
              <div class="flex-shrink-0 flex flex-col gap-2">
                <div class="flex gap-2">
                  <button
                    @click="approveApplication(app.id, app)"
                    class="px-4 py-2 bg-white border border-gray-800 text-gray-800 font-semibold rounded hover:bg-gray-800 hover:text-white transition"
                  >
                    Prihvati
                  </button>
                  <button
                    @click="rejectApplication(app.id, app)"
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

        <!-- AKTIVNI ODNOSI Section -->
        <div class="mt-8 pt-8 border-t border-gray-200">
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">AKTIVNI ODNOSI</h2>
          <div v-if="activeApplications.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
            <p class="text-gray-500">Nema aktivnih odnosa za sada</p>
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="app in activeApplications"
              :key="app.id"
              class="bg-white border border-gray-200 rounded-lg p-4 flex items-start gap-4"
            >
              <!-- Avatar placeholder -->
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                  <span class="text-purple-600 font-semibold">{{ getInitials(app.student_name) }}</span>
                </div>
              </div>

              <!-- Content -->
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-gray-800">{{ app.student_name }}</h3>
                <p class="text-gray-600 text-sm mt-1 line-clamp-2">{{ app.message }}</p>
                <p class="text-gray-400 text-xs mt-2">{{ formatDate(app.created_at) }}</p>
              </div>

              <!-- Status badge -->
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
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="showDetailsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-md w-full p-8 shadow-xl">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-semibold text-gray-800">Profil studentice</h2>
          <button
            @click="closeDetails"
            class="text-gray-500 hover:text-gray-700 text-2xl font-bold"
          >
            ✕
          </button>
        </div>

        <div class="space-y-5 bg-gray-50 rounded-lg p-6">
          <!-- Avatar -->
          <div class="flex justify-center">
            <div class="w-16 h-16 bg-purple-200 rounded-full flex items-center justify-center">
              <span class="text-purple-600 font-semibold text-xl">{{ getInitials(selectedApplication.student_name) }}</span>
            </div>
          </div>

          <!-- Student Info -->
          <div class="text-center">
            <h3 class="text-xl font-semibold text-gray-800">{{ selectedApplication.student_name }}</h3>
            <p class="text-gray-600 text-sm">{{ selectedApplication.student_email }}</p>
          </div>

          <!-- Message/Motivation -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Motivacija/Poruka:</label>
            <div class="bg-white border border-gray-200 rounded p-3 text-gray-600 text-sm">
              {{ selectedApplication.message }}
            </div>
          </div>

          <!-- Date -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Primljena:</label>
            <p class="text-gray-600">{{ formatDateFull(selectedApplication.created_at) }}</p>
          </div>

          <!-- Close Button -->
          <div class="flex mt-6">
            <button
              @click="closeDetails"
              class="w-full px-4 py-2 bg-gray-300 text-gray-800 font-semibold rounded hover:bg-gray-400 transition"
            >
              Zatvori
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getMentorApplications, updateApplicationStatus } from '../../services/mentoring.js'

const applications = ref([])
const loading = ref(true)
const error = ref(null)
const showDetailsModal = ref(false)
const selectedApplication = ref(null)

const pendingApplications = computed(() => {
  return applications.value.filter(app => app.status === 'PENDING')
})

const activeApplications = computed(() => {
  return applications.value.filter(app => app.status === 'APPROVED')
})

const getInitials = (name) => {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
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

const approveApplication = async (applicationId, app) => {
  try {
    await updateApplicationStatus(applicationId, 'APPROVED')
    app.status = 'APPROVED'
    closeDetails()
  } catch (err) {
    console.error('Greška pri prihvatanju zahtjeva:', err)
    error.value = 'Nije moguće prihvatiti zahtjev'
  }
}

const rejectApplication = async (applicationId, app) => {
  try {
    await updateApplicationStatus(applicationId, 'REJECTED')
    applications.value = applications.value.filter(a => a.id !== applicationId)
    closeDetails()
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
