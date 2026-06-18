<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-200 via-pink-100 to-pink-200 p-8">
    <div class="max-w-2xl mx-auto">
      <button @click="router.back()" class="mb-4 text-sm text-blue-600 hover:underline">
        ← Nazad
      </button>

      <div v-if="loading" class="text-center py-10">Učitavanje...</div>
      <div v-else-if="error" class="text-red-500 text-center py-10">{{ error }}</div>

      <div v-else-if="application">
        <div class="border rounded-xl p-6 mb-4 bg-white">
          <div class="flex items-start justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ application.first_name }} {{ application.last_name }}</h1>
              <p class="text-gray-600 mt-2">{{ application.email }}</p>
            </div>
            <span :class="['text-xs font-semibold px-3 py-1 rounded-full', statusBadgeClass(application.status)]">
              {{ statusLabel(application.status) }}
            </span>
          </div>
        </div>

        <div class="bg-white border rounded-xl p-6 mb-4 grid grid-cols-2 gap-4">
          <div>
            <p class="text-sm text-gray-500 mb-1">Oblast stručnosti</p>
            <p class="font-semibold">{{ application.field_of_expertise }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 mb-1">Godine iskustva</p>
            <p class="font-semibold">{{ application.years_of_experience || '—' }} godina</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 mb-1">Institucija</p>
            <p class="font-semibold">{{ application.institution || 'Nije navedeno' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 mb-1">Pozicija</p>
            <p class="font-semibold">{{ application.position || 'Nije navedeno' }}</p>
          </div>
        </div>

        <div v-if="application.linkedin_url" class="bg-white border rounded-xl p-6 mb-4">
          <p class="text-sm text-gray-500 mb-2">LinkedIn profil</p>
          <a :href="application.linkedin_url" target="_blank" class="text-blue-600 hover:underline break-all">
            {{ application.linkedin_url }}
          </a>
        </div>

        <div class="bg-white border rounded-xl p-6 mb-4">
          <h2 class="font-bold text-lg mb-3">Biografija</h2>
          <p class="text-gray-700 whitespace-pre-wrap">{{ application.bio }}</p>
        </div>

        <div v-if="application.cv_url" class="bg-white border rounded-xl p-6 mb-4">
          <h2 class="font-bold text-lg mb-3">CV datoteka</h2>
          <p class="text-sm text-gray-600 mb-3">{{ application.cv_url }}</p>
          <a :href="`${BASE_URL}/mentoring/cv/${application.cv_url}`" :download="application.cv_url" class="inline-flex items-center gap-2 bg-black text-white text-sm px-4 py-2 rounded-lg hover:bg-gray-800 transition">Preuzmi CV</a>
        </div>

        <div v-if="application.academic_title" class="bg-white border rounded-xl p-6 mb-4">
          <p class="text-sm text-gray-500 mb-1">Akademski naslov</p>
          <p class="font-semibold">{{ application.academic_title }}</p>
        </div>

        <div class="bg-white border rounded-xl p-6 mb-4">
          <p class="text-sm text-gray-500 mb-2">Iskustvo u mentorstvu</p>
          <p class="font-semibold">{{ application.has_mentoring_experience ? 'Da' : 'Ne' }}</p>
        </div>

        <div v-if="application.motivation" class="bg-white border rounded-xl p-6 mb-4">
          <h2 class="font-bold text-lg mb-3">Motivacija</h2>
          <p class="text-gray-700 whitespace-pre-wrap">{{ application.motivation }}</p>
        </div>

        <div v-if="application.rejection_reason" class="bg-red-50 border border-red-200 rounded-xl p-6 mb-4">
          <h2 class="font-bold text-lg mb-3 text-red-700">Razlog odbijanja</h2>
          <p class="text-red-600 whitespace-pre-wrap">{{ application.rejection_reason }}</p>
        </div>

        <div v-if="application.status === 'PENDING'" class="bg-white border rounded-xl p-6 mb-4">
          <h2 class="font-bold text-lg mb-3">Razlog odbijanja (opciono)</h2>
          <textarea
            v-model="rejectionReason"
            placeholder="Unesite razlog odbijanja..."
            class="w-full border border-gray-300 rounded-lg p-3 text-sm resize-none focus:outline-none focus:border-black"
            rows="4"
          ></textarea>
        </div>

        <div class="bg-white border rounded-xl p-6">
          <p class="text-sm text-gray-600 mb-4">Akcije:</p>
          <div class="flex gap-3">
            <button
              v-if="application.status === 'PENDING'"
              @click="approveApplication"
              :disabled="actionLoading"
              class="flex-1 bg-green-600 text-white py-2 rounded-lg font-semibold hover:bg-green-700 transition disabled:opacity-50"
            >
              {{ actionLoading ? 'Odobravanje...' : '✓ Odobri' }}
            </button>
            <button
              v-if="application.status === 'PENDING'"
              @click="rejectApplication"
              :disabled="actionLoading"
              class="flex-1 bg-red-600 text-white py-2 rounded-lg font-semibold hover:bg-red-700 transition disabled:opacity-50"
            >
              {{ actionLoading ? 'Odbijanje...' : '✕ Odbij' }}
            </button>
            <button
              @click="deleteApplication"
              :disabled="actionLoading"
              class="flex-1 bg-black text-white py-2 rounded-lg font-semibold hover:bg-gray-800 transition disabled:opacity-50"
            >
              {{ actionLoading ? 'Brisanje...' : 'Obriši' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const application = ref(null)
const loading = ref(true)
const error = ref(null)
const actionLoading = ref(false)
const rejectionReason = ref('')

const BASE_URL = 'http://127.0.0.1:8000'

function getToken() {
  return localStorage.getItem('token')
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`
  }
}

function statusBadgeClass(status) {
  if (status === 'APPROVED') return 'bg-green-100 text-green-700'
  if (status === 'REJECTED') return 'bg-red-100 text-red-700'
  return 'bg-yellow-100 text-yellow-700'
}

function statusLabel(status) {
  if (status === 'APPROVED') return 'Odobrena'
  if (status === 'REJECTED') return 'Odbijena'
  return 'Čeka se odobrenje'
}

async function fetchApplication() {
  try {
    const id = route.params.id
    const response = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}`, {
      headers: authHeaders()
    })
    if (response.status === 401) {
      router.push('/unauthorized')
      return
    }
    if (!response.ok) throw new Error('Nije pronađena aplikacija')
    application.value = await response.json()
  } catch (err) {
    error.value = err.message || 'Greška pri učitavanju podataka'
  } finally {
    loading.value = false
  }
}

async function approveApplication() {
  actionLoading.value = true
  try {
    const response = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${application.value.id}/approve`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (response.ok) {
      application.value = await response.json()
    } else {
      error.value = 'Greška pri odobravanju'
    }
  } catch (err) {
    error.value = 'Greška pri odobravanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = false
  }
}

async function rejectApplication() {
  actionLoading.value = true
  try {
    const response = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${application.value.id}/reject`, {
      method: 'PATCH',
      headers: authHeaders(),
      body: JSON.stringify({ rejection_reason: rejectionReason.value || null })
    })
    if (response.ok) {
      application.value = await response.json()
      rejectionReason.value = ''
    } else {
      error.value = 'Greška pri odbijanju'
    }
  } catch (err) {
    error.value = 'Greška pri odbijanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = false
  }
}

async function deleteApplication() {
  actionLoading.value = true
  try {
    const response = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${application.value.id}`, {
      method: 'DELETE',
      headers: authHeaders()
    })
    if (response.ok) {
      router.push('/admin/mentor-applications')
    } else if (response.status === 401) {
      router.push('/unauthorized')
    } else {
      error.value = 'Greška pri brisanju'
    }
  } catch (err) {
    error.value = 'Greška pri brisanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = false
  }
}

onMounted(() => {
  const token = getToken()
  if (!token) {
    router.push('/login')
    return
  }
  fetchApplication()
})
</script>
