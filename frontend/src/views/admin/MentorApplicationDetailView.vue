<template>
  <div class="max-w-2xl mx-auto p-4">
    <!-- Dugme Nazad -->
    <button @click="router.back()" class="mb-4 text-sm text-blue-600 hover:underline">
      ← Nazad
    </button>

    <div v-if="loading" class="text-center py-10">Učitavanje...</div>
    <div v-else-if="error" class="text-red-500 text-center py-10">{{ error }}</div>

    <div v-else-if="application">
      <!-- Header -->
      <div class="border rounded-xl p-6 mb-4">
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

      <!-- Osnovna informacija -->
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

      <!-- LinkedIn -->
      <div v-if="application.linkedin_url" class="bg-white border rounded-xl p-6 mb-4">
        <p class="text-sm text-gray-500 mb-2">LinkedIn profil</p>
        <a :href="application.linkedin_url" target="_blank" class="text-blue-600 hover:underline break-all">
          {{ application.linkedin_url }}
        </a>
      </div>

      <!-- Biografija -->
      <div class="bg-white border rounded-xl p-6 mb-4">
        <h2 class="font-bold text-lg mb-3">Biografija</h2>
        <p class="text-gray-700 whitespace-pre-wrap">{{ application.bio }}</p>
      </div>

      <!-- CV -->
      <div v-if="application.cv_url" class="bg-white border rounded-xl p-6 mb-4">
        <h2 class="font-bold text-lg mb-3">CV datoteka</h2>
        <p class="text-sm text-gray-600 mb-2">{{ application.cv_url }}</p>
        <p class="text-xs text-gray-500">Datoteka je pohranjena na serveru</p>
      </div>

      <!-- Akademski naslov -->
      <div v-if="application.academic_title" class="bg-white border rounded-xl p-6 mb-4">
        <p class="text-sm text-gray-500 mb-1">Akademski naslov</p>
        <p class="font-semibold">{{ application.academic_title }}</p>
      </div>

      <!-- Mentorsko iskustvo -->
      <div class="bg-white border rounded-xl p-6 mb-4">
        <p class="text-sm text-gray-500 mb-2">Iskustvo u mentorstvu</p>
        <p class="font-semibold">{{ application.has_mentoring_experience ? 'Da' : 'Ne' }}</p>
      </div>

      <!-- Motivacija -->
      <div v-if="application.motivation" class="bg-white border rounded-xl p-6 mb-4">
        <h2 class="font-bold text-lg mb-3">Motivacija</h2>
        <p class="text-gray-700 whitespace-pre-wrap">{{ application.motivation }}</p>
      </div>

      <!-- Akcije -->
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
            {{ actionLoading ? 'Brisanje...' : '🗑 Obriši' }}
          </button>
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

    if (!response.ok) {
      throw new Error('Nije pronađena aplikacija')
    }

    application.value = await response.json()
  } catch (err) {
    error.value = err.message || 'Greška pri učitavanju podataka'
  } finally {
    loading.value = false
  }
}

async function approveApplication() {
  if (!confirm('Jeste li sigurni da želite odobrit ovu aplikaciju?')) return

  actionLoading.value = true
  try {
    const response = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${application.value.id}/approve`, {
      method: 'PATCH',
      headers: authHeaders()
    })

    if (response.ok) {
      application.value = await response.json()
      alert('Aplikacija je odobrena!')
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
  if (!confirm('Jeste li sigurni da želite odbiti ovu aplikaciju?')) return

  actionLoading.value = true
  try {
    const response = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${application.value.id}/reject`, {
      method: 'PATCH',
      headers: authHeaders()
    })

    if (response.ok) {
      application.value = await response.json()
      alert('Aplikacija je odbijena!')
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
  if (!confirm('Jeste li sigurni da želite obrisati ovu aplikaciju?')) return

  actionLoading.value = true
  try {
    const response = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${application.value.id}`, {
      method: 'DELETE',
      headers: authHeaders()
    })

    if (response.ok) {
      alert('Aplikacija je obrisana!')
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
