<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-xl mx-auto">
      <h1 class="text-2xl font-bold text-gray-800 mb-6">Status prijave za mentoricu</h1>

      <div v-if="loading" class="text-center py-16 text-gray-400">Učitavanje...</div>

      <div v-else-if="notFound" class="bg-white border border-gray-200 rounded-xl p-6 text-center">
        <p class="text-gray-600 mb-4">Nemate aktivnu prijavu za mentoricu.</p>
        <router-link to="/mentoring/apply" class="inline-block px-4 py-2 bg-black text-white rounded hover:bg-gray-800 transition-colors">
          Prijavi se kao mentorica
        </router-link>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm text-gray-500">Vaš status</span>
          <span :class="['text-xs font-semibold px-3 py-1 rounded-full', statusBadgeClass]">
            {{ statusLabel }}
          </span>
        </div>

        <p v-if="application.status === 'PENDING'" class="text-gray-600">
          Vaša prijava je na čekanju. Administratorica će je pregledati u najkraćem mogućem roku.
        </p>

        <p v-else-if="application.status === 'APPROVED'" class="text-gray-600">
          Čestitamo! Vaša prijava je prihvaćena. Sada ste aktivna mentorica na platformi.
        </p>

        <template v-else-if="application.status === 'REJECTED'">
          <p class="text-gray-600 mb-3">Vaša prijava je nažalost odbijena.</p>
          <div v-if="application.rejection_reason" class="bg-red-50 border-l-4 border-red-400 text-red-700 text-sm rounded p-3 mb-4">
            <strong>Razlog:</strong> {{ application.rejection_reason }}
          </div>
          <button
            @click="resubmit"
            :disabled="resubmitting"
            class="w-full px-4 py-2 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
          >
            {{ resubmitting ? 'Slanje...' : 'Pošalji prijavu ponovo' }}
          </button>
        </template>

        <div v-if="error" class="mt-4 bg-red-50 border border-red-200 text-red-600 rounded-lg px-4 py-3 text-sm">
          {{ error }}
        </div>
        <div v-if="success" class="mt-4 bg-green-50 border border-green-200 text-green-700 rounded-lg px-4 py-3 text-sm">
          {{ success }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const BASE_URL = 'http://127.0.0.1:8000'

const loading = ref(true)
const notFound = ref(false)
const application = ref(null)
const error = ref(null)
const success = ref(null)
const resubmitting = ref(false)

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
}

const statusBadgeClass = computed(() => {
  if (!application.value) return ''
  if (application.value.status === 'APPROVED') return 'bg-green-100 text-green-700'
  if (application.value.status === 'REJECTED') return 'bg-red-100 text-red-700'
  return 'bg-yellow-100 text-yellow-700'
})

const statusLabel = computed(() => {
  if (!application.value) return ''
  if (application.value.status === 'APPROVED') return 'Prihvaćena'
  if (application.value.status === 'REJECTED') return 'Odbijena'
  return 'Na čekanju'
})

async function fetchMyApplication() {
  try {
    const res = await fetch(`${BASE_URL}/mentoring/my-application`, { headers: authHeaders() })
    if (res.status === 404) {
      notFound.value = true
    } else if (res.ok) {
      application.value = await res.json()
    } else {
      error.value = 'Greška pri učitavanju statusa prijave.'
    }
  } catch (e) {
    error.value = 'Greška pri učitavanju. Provjerite konekciju.'
  } finally {
    loading.value = false
  }
}

async function resubmit() {
  resubmitting.value = true
  error.value = null
  success.value = null
  try {
    const res = await fetch(`${BASE_URL}/mentoring/my-application/resubmit`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) {
      application.value = await res.json()
      success.value = 'Prijava je ponovo poslana i čeka odobrenje.'
    } else {
      const data = await res.json().catch(() => null)
      error.value = data?.detail || 'Greška pri ponovnom slanju prijave.'
    }
  } catch (e) {
    error.value = 'Greška pri slanju. Provjerite konekciju.'
  } finally {
    resubmitting.value = false
  }
}

onMounted(fetchMyApplication)
</script>