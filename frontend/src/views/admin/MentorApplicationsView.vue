<template>
<div class="min-h-screen bg-gradient-to-br from-purple-200 via-pink-100 to-pink-200 py-8 px-4">
    <div class="max-w-5xl mx-auto">

      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold text-gray-800 tracking-tight">Admin Panel</h1>
        <span v-if="userRole === 'admin'" class="border border-black px-2 py-1 text-xs font-semibold rounded">ADMIN</span>
      </div>

      <div v-if="loading" class="text-center py-16 text-gray-400">
        Učitavanje...
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-600 rounded-lg px-4 py-3 mb-6">
        {{ error }}
      </div>

      <template v-else>

        <div class="flex gap-1 mb-6 border-b border-gray-200">
          <button
            @click="mainTab = 'mentorice'"
            :class="['px-5 py-2.5 text-sm font-semibold border-b-2 -mb-px transition-colors',
                     mainTab === 'mentorice' ? 'border-black text-black' : 'border-transparent text-gray-400 hover:text-gray-600']"
          >
            Mentorice
          </button>
          <button
            @click="mainTab = 'studentice'"
            :class="['px-5 py-2.5 text-sm font-semibold border-b-2 -mb-px transition-colors',
                     mainTab === 'studentice' ? 'border-black text-black' : 'border-transparent text-gray-400 hover:text-gray-600']"
          >
            Studentice
          </button>
        </div>

        <div class="flex gap-2 mb-6">
          <button
            v-for="t in subTabs"
            :key="t.key"
            @click="setSubTab(t.key)"
            :class="['text-xs font-semibold px-3 py-1.5 rounded-full transition-colors',
                     activeSubTab === t.key ? 'bg-black text-white' : 'bg-gray-100 text-gray-500 hover:bg-gray-200']"
          >
            {{ t.label }} ({{ countFor(t.key) }})
          </button>
        </div>

        <section v-if="mainTab === 'mentorice'">
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
                <tr v-if="currentMentorList.length === 0">
                  <td colspan="4" class="px-5 py-6 text-center text-gray-400">{{ emptyMessage }}</td>
                </tr>
                <tr
                  v-for="app in currentMentorList"
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

                      <template v-if="mentorSubTab === 'PENDING'">
                        <button
                          @click="approveMentor(app.id)"
                          :disabled="actionLoading === `mentor-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-white border border-black text-black rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
                        >✓</button>
                        <button
                          @click="rejectMentor(app.id)"
                          :disabled="actionLoading === `mentor-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                        >✕</button>
                      </template>

                      <template v-else-if="mentorSubTab === 'DELETED'">
                        <button
                          @click="restoreMentor(app.id)"
                          :disabled="actionLoading === `mentor-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-white border border-black text-black rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
                        >↺ Vrati</button>
                      </template>

                      <template v-else>
                        <button
                          @click="deleteMentor(app.id)"
                          :disabled="actionLoading === `mentor-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                        >Obriši</button>
                      </template>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section v-else>
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
                <tr v-if="currentStudentList.length === 0">
                  <td colspan="5" class="px-5 py-6 text-center text-gray-400">{{ emptyMessage }}</td>
                </tr>
                <tr
                  v-for="app in currentStudentList"
                  :key="app.id"
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

                      <template v-if="studentSubTab === 'PENDING'">
                        <button
                          @click="approveStudent(app.id)"
                          :disabled="actionLoading === `student-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-white border border-black text-black rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
                        >✓</button>
                        <button
                          @click="rejectStudent(app.id)"
                          :disabled="actionLoading === `student-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                        >✕</button>
                      </template>

                      <template v-else-if="studentSubTab === 'DELETED'">
                        <button
                          @click="restoreStudent(app.id)"
                          :disabled="actionLoading === `student-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-white border border-black text-black rounded hover:bg-gray-50 transition-colors disabled:opacity-50"
                        >↺ Vrati</button>
                      </template>

                      <template v-else>
                        <button
                          @click="deleteStudent(app.id)"
                          :disabled="actionLoading === `student-${app.id}`"
                          class="text-xs px-3 py-1.5 bg-black text-white rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                        >Obriši</button>
                      </template>
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

      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const BASE_URL = 'http://127.0.0.1:8000'

const router = useRouter()
const loading = ref(true)
const error = ref(null)
const actionLoading = ref(null)

const userRole = computed(() => localStorage.getItem('user_role'))

const mainTab = ref('mentorice')
const mentorSubTab = ref('PENDING')
const studentSubTab = ref('PENDING')

const subTabs = [
  { key: 'PENDING', label: 'Na čekanju' },
  { key: 'APPROVED', label: 'Prihvaćene' },
  { key: 'REJECTED', label: 'Odbijene' },
  { key: 'DELETED', label: 'Obrisane' },
]

const activeSubTab = computed(() =>
  mainTab.value === 'mentorice' ? mentorSubTab.value : studentSubTab.value
)

function setSubTab(key) {
  if (mainTab.value === 'mentorice') mentorSubTab.value = key
  else studentSubTab.value = key
}

function countFor(key) {
  const source = mainTab.value === 'mentorice' ? mentorsByStatus.value : studentsByStatus.value
  return (source[key] || []).length
}

const emptyMessage = computed(() => {
  const labels = { PENDING: 'na čekanju', APPROVED: 'prihvaćenih', REJECTED: 'odbijenih', DELETED: 'obrisanih' }
  const subject = mainTab.value === 'mentorice' ? 'mentorica' : 'studentica'
  return `Nema ${labels[activeSubTab.value]} ${subject}`
})

const mentorsByStatus = ref({ PENDING: [], APPROVED: [], REJECTED: [], DELETED: [] })
const studentsByStatus = ref({ PENDING: [], APPROVED: [], REJECTED: [], DELETED: [] })

const currentMentorList = computed(() => mentorsByStatus.value[mentorSubTab.value] || [])
const currentStudentList = computed(() => studentsByStatus.value[studentSubTab.value] || [])

function statusBadgeClass(status) {
  if (status === 'APPROVED') return 'bg-green-100 text-green-700'
  if (status === 'REJECTED') return 'bg-red-100 text-red-700'
  if (status === 'DELETED') return 'bg-gray-200 text-gray-500'
  return 'bg-yellow-100 text-yellow-700'
}

function statusLabel(status) {
  if (status === 'APPROVED') return 'OK ✓'
  if (status === 'REJECTED') return 'Odbijena'
  if (status === 'DELETED') return 'Obrisana'
  return 'Čeka'
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

async function fetchMentors() {
  const statuses = ['PENDING', 'APPROVED', 'REJECTED', 'DELETED']
  const results = await Promise.all(
    statuses.map(s =>
      fetch(`${BASE_URL}/api/v1/admin/mentor-applications?status=${s}&limit=100`, { headers: authHeaders() })
        .then(res => (res.ok ? res.json() : []))
    )
  )
  statuses.forEach((s, i) => { mentorsByStatus.value[s] = results[i] })
}

function replaceMentorInLists(updated) {
  Object.keys(mentorsByStatus.value).forEach(key => {
    mentorsByStatus.value[key] = mentorsByStatus.value[key].filter(m => m.id !== updated.id)
  })
  if (mentorsByStatus.value[updated.status]) {
    mentorsByStatus.value[updated.status].push(updated)
  }
}

async function approveMentor(id) {
  actionLoading.value = `mentor-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}/approve`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) replaceMentorInLists(await res.json())
    else error.value = 'Greška pri odobravanju mentorice.'
  } catch (e) {
    error.value = 'Greška pri odobravanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function rejectMentor(id) {
  actionLoading.value = `mentor-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}/reject`, {
      method: 'PATCH',
      headers: authHeaders(),
      body: JSON.stringify({ rejection_reason: 'Aplikacija je odbijena' })
    })
    if (res.ok) replaceMentorInLists(await res.json())
    else error.value = 'Greška pri odbijanju mentorice.'
  } catch (e) {
    error.value = 'Greška pri odbijanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function deleteMentor(id) {
  actionLoading.value = `mentor-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}`, {
      method: 'DELETE',
      headers: authHeaders()
    })
    if (res.ok) replaceMentorInLists(await res.json())
    else if (res.status === 401) router.push('/unauthorized')
    else error.value = 'Greška pri brisanju mentorice.'
  } catch (e) {
    error.value = 'Greška pri brisanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function restoreMentor(id) {
  actionLoading.value = `mentor-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/mentor-applications/${id}/resubmit`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) replaceMentorInLists(await res.json())
    else error.value = 'Greška pri vraćanju mentorice.'
  } catch (e) {
    error.value = 'Greška pri vraćanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

function pregledajPrijavu(id) {
  router.push(`/admin/mentor-applications/${id}`)
}

async function fetchStudents() {
  const endpointByStatus = {
    PENDING: 'student-applications',
    APPROVED: 'student-applications-approved',
    REJECTED: 'student-applications-rejected',
    DELETED: 'student-applications-deleted',
  }
  const statuses = Object.keys(endpointByStatus)
  const results = await Promise.all(
    statuses.map(s =>
      fetch(`${BASE_URL}/api/v1/admin/${endpointByStatus[s]}?limit=100`, { headers: authHeaders() })
        .then(res => (res.ok ? res.json() : []))
    )
  )
  statuses.forEach((s, i) => { studentsByStatus.value[s] = results[i] })
}

function replaceStudentInLists(updated) {
  Object.keys(studentsByStatus.value).forEach(key => {
    studentsByStatus.value[key] = studentsByStatus.value[key].filter(s => s.id !== updated.id)
  })
  if (studentsByStatus.value[updated.status]) {
    studentsByStatus.value[updated.status].push(updated)
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
    if (res.ok) replaceStudentInLists(await res.json())
    else error.value = 'Greška pri odobravanju studentice.'
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
    if (res.ok) replaceStudentInLists(await res.json())
    else error.value = 'Greška pri odbijanju studentice.'
  } catch (e) {
    error.value = 'Greška pri odbijanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function restoreStudent(id) {
  actionLoading.value = `student-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/student-applications/${id}/restore`, {
      method: 'PATCH',
      headers: authHeaders()
    })
    if (res.ok) replaceStudentInLists(await res.json())
    else error.value = 'Greška pri vraćanju studentice.'
  } catch (e) {
    error.value = 'Greška pri vraćanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

async function deleteStudent(id) {
  actionLoading.value = `student-${id}`
  error.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/v1/admin/student-applications/${id}`, {
      method: 'DELETE',
      headers: authHeaders()
    })
    if (res.ok) replaceStudentInLists(await res.json())
    else error.value = 'Greška pri brisanju studentice.'
  } catch (e) {
    error.value = 'Greška pri brisanju. Provjerite konekciju.'
  } finally {
    actionLoading.value = null
  }
}

const showDetailModal = ref(false)
const selectedStudent = ref(null)

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

onMounted(async () => {
  const token = getToken()
  if (!token) {
    router.push('/login')
    return
  }
  try {
    await Promise.all([fetchMentors(), fetchStudents()])
  } catch (e) {
    error.value = 'Greška pri učitavanju podataka.'
  } finally {
    loading.value = false
  }
})
</script>