<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-5xl mx-auto">

      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-2xl font-bold text-gray-800 tracking-tight">Admin Panel</h1>
        <span v-if="userRole === 'admin'" class="border border-black px-2 py-1 text-xs font-semibold rounded">ADMIN</span>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-16 text-gray-400">
        Učitavanje...
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-600 rounded-lg px-4 py-3 mb-6">
        {{ error }}
      </div>

      <template v-else>
        <!-- Zahtjevi na čekanju -->
        <section class="mb-10">
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">Zahtjevi na čekanju</h2>
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-100 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Ime</th>
                  <th class="text-left px-5 py-3">Oblast</th>
                  <th class="text-left px-5 py-3">Status</th>
                  <th class="text-left px-5 py-3">Akcija</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="pending.length === 0">
                  <td colspan="4" class="px-5 py-6 text-center text-gray-400">Nema zahtjeva na čekanju</td>
                </tr>
                <tr
                  v-for="app in pending"
                  :key="app.id"
                  :class="['border-t border-gray-100 transition-all duration-500', rowFlash[app.id] || 'hover:bg-gray-50']"
                >
                  <td class="px-5 py-3 font-medium text-gray-800">{{ app.first_name }} {{ app.last_name }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.field_of_expertise }}</td>
                  <td class="px-5 py-3">
                    <span :class="['text-xs font-semibold px-2.5 py-0.5 rounded-full transition-all duration-500', statusBadgeClass(app.status)]">
                      {{ statusLabel(app.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3">
                    <div class="flex items-center gap-2">
                      <button
                        @click="pregledajPrijavu(app.id)"
                        class="flex items-center gap-1 text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-gray-600"
                      >
                        🔍 Pregledaj
                      </button>
                      <button
                        @click="approveApplication(app.id)"
                        :disabled="actionLoading === app.id || app.status !== 'PENDING'"
                        class="text-xs px-3 py-1.5 bg-white border border-black text-black rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
                      >
                        ✓
                      </button>
                      <button
                        @click="rejectApplication(app.id)"
                        :disabled="actionLoading === app.id || app.status !== 'PENDING'"
                        class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                      >
                        ✕
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Odobrene mentorice -->
        <section class="mb-10">
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">Odobrene mentorice</h2>
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-100 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Ime</th>
                  <th class="text-left px-5 py-3">Oblast</th>
                  <th class="text-left px-5 py-3">Status</th>
                  <th class="text-left px-5 py-3">Akcija</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="approved.length === 0">
                  <td colspan="4" class="px-5 py-6 text-center text-gray-400">Nema odobrenih mentorica</td>
                </tr>
                <tr
                  v-for="app in approved"
                  :key="app.id"
                  class="border-t border-gray-100 hover:bg-gray-50 transition-colors"
                >
                  <td class="px-5 py-3 font-medium text-gray-800">{{ app.first_name }} {{ app.last_name }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.field_of_expertise }}</td>
                  <td class="px-5 py-3">
                    <span :class="['text-xs font-semibold px-2.5 py-0.5 rounded-full', statusBadgeClass(app.status)]">
                      {{ statusLabel(app.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3">
                    <button
                      @click="deleteApplication(app.id)"
                      class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors"
                    >
                      Obriši
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Odbijene mentorice -->
        <section>
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">Odbijene mentorice</h2>
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-100 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Ime</th>
                  <th class="text-left px-5 py-3">Oblast</th>
                  <th class="text-left px-5 py-3">Status</th>
                  <th class="text-left px-5 py-3">Akcija</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="rejected.length === 0">
                  <td colspan="4" class="px-5 py-6 text-center text-gray-400">Nema odbijenih mentorica</td>
                </tr>
                <tr
                  v-for="app in rejected"
                  :key="app.id"
                  class="border-t border-gray-100 hover:bg-gray-50 transition-colors"
                >
                  <td class="px-5 py-3 font-medium text-gray-800">{{ app.first_name }} {{ app.last_name }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.field_of_expertise }}</td>
                  <td class="px-5 py-3">
                    <span :class="['text-xs font-semibold px-2.5 py-0.5 rounded-full', statusBadgeClass(app.status)]">
                      {{ statusLabel(app.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3">
                    <button
                      @click="deleteApplication(app.id)"
                      class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors"
                    >
                      Obriši
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const BASE_URL = 'http://127.0.0.1:8000'

const router = useRouter()
const applications = ref([])
const loading = ref(true)
const error = ref(null)
const actionLoading = ref(null)
const rowFlash = ref({})

const userRole = computed(() => {
  const token = localStorage.getItem('token')
  if (!token) return null
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.role
  } catch {
    return null
  }
})

const pending = computed(() => applications.value.filter(a => a.status === 'PENDING'))
const approved = computed(() => applications.value.filter(a => a.status === 'APPROVED'))
const rejected = computed(() => applications.value.filter(a => a.status === 'REJECTED'))

function statusBadgeClass(status) {
  if (status === 'APPROVED') return 'bg-green-100 text-green-700'
  if (status === 'REJECTED') return 'bg-red-100 text-red-700'
  return 'bg-yellow-100 text-yellow-700'
}

function statusLabel(status) {
  if (status === 'APPROVED') return 'OK ✓'
  if (status === 'REJECTED') return 'Odbijena'
  return 'Čeka'
}

function flashRow(id, type) {
  rowFlash.value[id] = type === 'APPROVED' ? 'bg-green-50' : 'bg-red-50'
  setTimeout(() => {
    delete rowFlash.value[id]
  }, 1000)
}

function getToken() {
  return localStorage.getItem('token')
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`
  }
}

async function fetchAllApplications() {
  try {
    const pendingRes = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications?limit=100`, {
      headers: authHeaders()
    })
    if (pendingRes.status === 401) {
      router.push('/unauthorized')
      return
    }
    const pendingData = await pendingRes.json()

    const allRes = await fetch(`${BASE_URL}/mentoring/mentors?limit=100`)
    const allApproved = await allRes.json()
    const approvedMapped = allApproved.map(m => ({ ...m, status: 'APPROVED' }))

    applications.value = [...pendingData, ...approvedMapped]
  } catch (e) {
    error.value = 'Greška pri učitavanju podataka.'
  } finally {
    loading.value = false
  }
}

async function approveApplication(id) {
  actionLoading.value = id
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}/approve`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) {
      const updated = await res.json()
      const idx = applications.value.findIndex(a => a.id === id)
      if (idx !== -1) {
        applications.value[idx] = updated
        flashRow(id, 'APPROVED')
      }
    } else {
      error.value = 'Greška pri odobravanju — server nije vratio uspješan odgovor.'
    }
  } catch (e) {
    error.value = 'Greška pri odobravanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function rejectApplication(id) {
  actionLoading.value = id
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}/reject`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) {
      const updated = await res.json()
      const idx = applications.value.findIndex(a => a.id === id)
      if (idx !== -1) {
        applications.value[idx] = updated
        flashRow(id, 'REJECTED')
      }
    } else {
      error.value = 'Greška pri odbijanju — server nije vratio uspješan odgovor.'
    }
  } catch (e) {
    error.value = 'Greška pri odbijanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function deleteApplication(id) {
  if (!confirm('Jeste li sigurni da želite obrisati ovu mentoricu?')) return
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}`, {
      method: 'DELETE',
      headers: authHeaders()
    })
    if (res.ok) {
      applications.value = applications.value.filter(a => a.id !== id)
    } else if (res.status === 401) {
      router.push('/unauthorized')
    } else {
      error.value = 'Greška pri brisanju — server nije vratio uspješan odgovor.'
    }
  } catch (e) {
    error.value = 'Greška pri brisanju. Provjerite konekciju.'
  }
}

function pregledajPrijavu(id) {
  router.push(`/mentors/${id}?from=admin`)
}

onMounted(() => {
  const token = getToken()
  if (!token) {
    router.push('/login')
    return
  }
  fetchAllApplications()
})
</script>