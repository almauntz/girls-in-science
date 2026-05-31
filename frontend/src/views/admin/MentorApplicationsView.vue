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
                    <div class="flex items-center gap-2">
                      <button
                        @click="pregledajPrijavu(app.id)"
                        class="flex items-center gap-1 text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-gray-600"
                      >
                        🔍 Pregledaj
                      </button>
                      <button
                        @click="deleteApplication(app.id)"
                        class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors"
                      >
                        Obriši
                      </button>
                    </div>
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
                    <div class="flex items-center gap-2">
                      <button
                        @click="pregledajPrijavu(app.id)"
                        class="flex items-center gap-1 text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-gray-600"
                      >
                        🔍 Pregledaj
                      </button>
                      <button
                        @click="deleteApplication(app.id)"
                        class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors"
                      >
                        Obriši
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- ======================= -->
        <!-- STUDENT APLIKACIJE       -->
        <!-- ======================= -->

        <!-- Student - Zahtjevi na čekanju -->
        <section class="mb-10 mt-16 pt-8 border-t-2 border-gray-300">
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">Studentice - Zahtjevi na čekanju</h2>
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-100 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Ime</th>
                  <th class="text-left px-5 py-3">Email</th>
                  <th class="text-left px-5 py-3">Fakultet</th>
                  <th class="text-left px-5 py-3">Status</th>
                  <th class="text-left px-5 py-3">Akcija</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="studentPending.length === 0">
                  <td colspan="5" class="px-5 py-6 text-center text-gray-400">Nema zahtjeva na čekanju</td>
                </tr>
                <tr
                  v-for="app in studentPending"
                  :key="`student-${app.id}`"
                  :class="['border-t border-gray-100 transition-all duration-500', studentRowFlash[app.id] || 'hover:bg-gray-50']"
                >
                  <td class="px-5 py-3 font-medium text-gray-800">{{ app.first_name }} {{ app.last_name }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.email }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.faculty }}</td>
                  <td class="px-5 py-3">
                    <span :class="['text-xs font-semibold px-2.5 py-0.5 rounded-full transition-all duration-500', statusBadgeClass(app.status)]">
                      {{ statusLabel(app.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3">
                    <div class="flex items-center gap-2">
                      <button
                        @click="openDetailModal(app.id)"
                        class="flex items-center gap-1 text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-gray-600"
                      >
                        🔍 Pregledaj
                      </button>
                      <button
                        @click="approveStudent(app.id)"
                        :disabled="actionLoading === `student-${app.id}`"
                        class="text-xs px-3 py-1.5 bg-white border border-black text-black rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
                      >
                        ✓
                      </button>
                      <button
                        @click="rejectStudent(app.id)"
                        :disabled="actionLoading === `student-${app.id}`"
                        class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                      >
                        ✕
                      </button>
                      <button
                        @click="openDeleteConfirm(app.id)"
                        :disabled="actionLoading === `student-${app.id}`"
                        class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                      >
                        Obriši
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Student - Odobrene -->
        <section class="mb-10">
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">Studentice - Odobrene</h2>
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-100 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Ime</th>
                  <th class="text-left px-5 py-3">Email</th>
                  <th class="text-left px-5 py-3">Fakultet</th>
                  <th class="text-left px-5 py-3">Status</th>
                  <th class="text-left px-5 py-3">Akcija</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="studentApproved.length === 0">
                  <td colspan="5" class="px-5 py-6 text-center text-gray-400">Nema odobrenih studentica</td>
                </tr>
                <tr
                  v-for="app in studentApproved"
                  :key="`student-${app.id}`"
                  class="border-t border-gray-100 hover:bg-gray-50 transition-colors"
                >
                  <td class="px-5 py-3 font-medium text-gray-800">{{ app.first_name }} {{ app.last_name }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.email }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.faculty }}</td>
                  <td class="px-5 py-3">
                    <span :class="['text-xs font-semibold px-2.5 py-0.5 rounded-full', statusBadgeClass(app.status)]">
                      {{ statusLabel(app.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3">
                    <div class="flex items-center gap-2">
                      <button
                        @click="openDetailModal(app.id)"
                        class="flex items-center gap-1 text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-gray-600"
                      >
                        🔍 Pregledaj
                      </button>
                      <button
                        @click="openDeleteConfirm(app.id)"
                        :disabled="actionLoading === `student-${app.id}`"
                        class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                      >
                        Obriši
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Student - Odbijene -->
        <section class="mb-10">
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">Studentice - Odbijene</h2>
          <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-100 text-gray-500 text-xs uppercase tracking-wider">
                  <th class="text-left px-5 py-3">Ime</th>
                  <th class="text-left px-5 py-3">Email</th>
                  <th class="text-left px-5 py-3">Fakultet</th>
                  <th class="text-left px-5 py-3">Status</th>
                  <th class="text-left px-5 py-3">Akcija</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="studentRejected.length === 0">
                  <td colspan="5" class="px-5 py-6 text-center text-gray-400">Nema odbijenih studentica</td>
                </tr>
                <tr
                  v-for="app in studentRejected"
                  :key="`student-${app.id}`"
                  class="border-t border-gray-100 hover:bg-gray-50 transition-colors"
                >
                  <td class="px-5 py-3 font-medium text-gray-800">{{ app.first_name }} {{ app.last_name }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.email }}</td>
                  <td class="px-5 py-3 text-gray-600">{{ app.faculty }}</td>
                  <td class="px-5 py-3">
                    <span :class="['text-xs font-semibold px-2.5 py-0.5 rounded-full', statusBadgeClass(app.status)]">
                      {{ statusLabel(app.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3">
                    <div class="flex items-center gap-2">
                      <button
                        @click="openDetailModal(app.id)"
                        class="flex items-center gap-1 text-xs px-3 py-1.5 border border-gray-300 rounded hover:bg-gray-50 transition-colors text-gray-600"
                      >
                        🔍 Pregledaj
                      </button>
                      <button
                        @click="openDeleteConfirm(app.id)"
                        :disabled="actionLoading === `student-${app.id}`"
                        class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                      >
                        Obriši
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Detail Modal -->
        <div v-if="showDetailModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <h2 class="text-lg font-bold text-gray-800">Detalji studentice</h2>
              <button @click="showDetailModal = false" class="text-gray-400 hover:text-gray-600 text-2xl">×</button>
            </div>
            <div v-if="selectedStudent" class="px-6 py-4 space-y-4">
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase">Ime i prezime</label>
                <p class="text-gray-800 mt-1">{{ selectedStudent.first_name }} {{ selectedStudent.last_name }}</p>
              </div>
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase">Email</label>
                <p class="text-gray-800 mt-1">{{ selectedStudent.email }}</p>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-xs font-semibold text-gray-500 uppercase">Fakultet</label>
                  <p class="text-gray-800 mt-1">{{ selectedStudent.faculty }}</p>
                </div>
                <div>
                  <label class="text-xs font-semibold text-gray-500 uppercase">Godina studija</label>
                  <p class="text-gray-800 mt-1">{{ selectedStudent.year_of_study || 'Nije navedena' }}</p>
                </div>
              </div>
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase">Interesovanja</label>
                <p class="text-gray-800 mt-1">{{ selectedStudent.areas_of_interest || 'Nije navedeno' }}</p>
              </div>
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase">Očekivanja od programa</label>
                <p class="text-gray-800 mt-1">{{ selectedStudent.expectations || 'Nije navedeno' }}</p>
              </div>
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase">Motivacijska poruka</label>
                <p class="text-gray-800 mt-1">{{ selectedStudent.motivational_message || 'Nije navedena' }}</p>
              </div>
              <div>
                <label class="text-xs font-semibold text-gray-500 uppercase">Vještine za poboljšanje</label>
                <p class="text-gray-800 mt-1">{{ selectedStudent.skills_to_improve || 'Nije navedeno' }}</p>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-xs font-semibold text-gray-500 uppercase">Format sesije</label>
                  <p class="text-gray-800 mt-1">{{ selectedStudent.preferred_session_format || 'Nije navedena' }}</p>
                </div>
                <div>
                  <label class="text-xs font-semibold text-gray-500 uppercase">Commitment</label>
                  <p class="text-gray-800 mt-1">{{ selectedStudent.session_commitment ? 'Da' : 'Ne' }}</p>
                </div>
              </div>
            </div>
            <div class="border-t border-gray-200 px-6 py-4 flex justify-end">
              <button @click="showDetailModal = false" class="px-4 py-2 bg-gray-100 text-gray-800 rounded hover:bg-gray-200 transition-colors">
                Zatvori
              </button>
            </div>
          </div>
        </div>

        <!-- Delete Confirm Modal -->
        <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div class="bg-white rounded-lg shadow-xl max-w-sm w-full">
            <div class="px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-bold text-gray-800">Potvrdi brisanje</h2>
            </div>
            <div class="px-6 py-4">
              <p class="text-gray-600">Jeste li sigurni da želite obrisati ovu studenticu? Ova akcija se ne može poništiti.</p>
            </div>
            <div class="border-t border-gray-200 px-6 py-4 flex justify-end gap-2">
              <button @click="showDeleteConfirm = false" class="px-4 py-2 bg-gray-100 text-gray-800 rounded hover:bg-gray-200 transition-colors">
                Poništi
              </button>
              <button @click="confirmDelete" :disabled="actionLoading" class="px-4 py-2 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50">
                Obriši
              </button>
            </div>
          </div>
        </div>
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

// Student aplikacije
const students = ref([])
const studentPending = computed(() => students.value.filter(s => s.status === 'PENDING'))
const studentApproved = computed(() => students.value.filter(s => s.status === 'APPROVED'))
const studentRejected = computed(() => students.value.filter(s => s.status === 'REJECTED'))
const studentRowFlash = ref({})

// Modal state
const showDetailModal = ref(false)
const selectedStudent = ref(null)
const showDeleteConfirm = ref(false)
const deleteConfirmId = ref(null)

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
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications?limit=100`, {
      headers: authHeaders()
    })
    if (res.status === 401) {
      router.push('/unauthorized')
      return
    }
    const pendingData = await pendingRes.json()

    const allRes = await fetch(`${BASE_URL}/mentoring/mentors?limit=100`)
    const allApproved = await allRes.json()
    const approvedMapped = allApproved.map(m => {
      const nameParts = (m.full_name || '').trim().split(/\s+/)
      const firstName = nameParts[0] || ''
      const lastName = nameParts.slice(1).join(' ') || ''
      return {
        ...m,
        first_name: firstName,
        last_name: lastName,
        status: 'APPROVED'
      }
    })

    applications.value = [...pendingData, ...approvedMapped]
    applications.value = await res.json()
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
  router.push(`/admin/mentor-applications/${id}`)
}

// ========================================
// STUDENT FUNKCIJE
// ========================================

async function fetchStudentApplications() {
  try {
    // Pending student aplikacije
    const pendingRes = await fetch(`${BASE_URL}/api/v1/admin/student-applications?limit=100`, {
      headers: authHeaders()
    })
    if (pendingRes.ok) {
      const pendingData = await pendingRes.json()
      
      // Approved student aplikacije
      const approvedRes = await fetch(`${BASE_URL}/api/v1/admin/student-applications-approved?limit=100`, {
        headers: authHeaders()
      })
      const approvedData = approvedRes.ok ? await approvedRes.json() : []
      
      // Rejected student aplikacije
      const rejectedRes = await fetch(`${BASE_URL}/api/v1/admin/student-applications-rejected?limit=100`, {
        headers: authHeaders()
      })
      const rejectedData = rejectedRes.ok ? await rejectedRes.json() : []
      
      students.value = [...pendingData, ...approvedData, ...rejectedData]
    }
  } catch (e) {
    console.error('Greška pri učitavanju student aplikacija:', e)
  }
}

async function approveStudent(id) {
  actionLoading.value = `student-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/student-applications/${id}/approve`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) {
      const updated = await res.json()
      const idx = students.value.findIndex(s => s.id === id)
      if (idx !== -1) {
        students.value[idx] = updated
        studentRowFlash.value[id] = 'bg-green-50'
        setTimeout(() => {
          delete studentRowFlash.value[id]
        }, 1000)
      }
    } else {
      error.value = 'Greška pri odobravanju studentice — server nije vratio uspješan odgovor.'
    }
  } catch (e) {
    error.value = 'Greška pri odobravanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function rejectStudent(id) {
  actionLoading.value = `student-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/student-applications/${id}/reject`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) {
      const updated = await res.json()
      const idx = students.value.findIndex(s => s.id === id)
      if (idx !== -1) {
        students.value[idx] = updated
        studentRowFlash.value[id] = 'bg-red-50'
        setTimeout(() => {
          delete studentRowFlash.value[id]
        }, 1000)
      }
    } else {
      error.value = 'Greška pri odbijanju studentice — server nije vratio uspješan odgovor.'
    }
  } catch (e) {
    error.value = 'Greška pri odbijanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function openDetailModal(id) {
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/student-applications/${id}`, {
      headers: authHeaders()
    })
    if (res.ok) {
      selectedStudent.value = await res.json()
      showDetailModal.value = true
    } else {
      error.value = 'Greška pri učitavanju detaljnih informacija studentice.'
    }
  } catch (e) {
    error.value = 'Greška pri učitavanju detaljnih informacija. Provjerite konekciju.'
  }
}

function openDeleteConfirm(id) {
  deleteConfirmId.value = id
  showDeleteConfirm.value = true
}

async function confirmDelete() {
  if (!deleteConfirmId.value) return
  
  actionLoading.value = `student-${deleteConfirmId.value}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/student-applications/${deleteConfirmId.value}`, {
      method: 'DELETE',
      headers: authHeaders()
    })
    if (res.ok) {
      students.value = students.value.filter(s => s.id !== deleteConfirmId.value)
      showDeleteConfirm.value = false
      deleteConfirmId.value = null
    } else {
      error.value = 'Greška pri brisanju studentice — server nije vratio uspješan odgovor.'
    }
  } catch (e) {
    error.value = 'Greška pri brisanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

onMounted(() => {
  const token = getToken()
  if (!token) {
    router.push('/login')
    return
  }
  fetchAllApplications()
  fetchStudentApplications()
})
</script>