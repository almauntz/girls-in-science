<template>
  <div class="min-h-screen" style="background: #f4f1fb; font-family: 'Segoe UI', system-ui, sans-serif;">
    <div
      class="relative overflow-hidden px-6 pt-12 pb-16 mb-0"
      style="background: linear-gradient(135deg, #6d28d9 0%, #7c3aed 50%, #9333ea 100%);"
    >
      <div class="absolute top-0 right-0 w-72 h-72 rounded-full opacity-10" style="background:#fff; transform:translate(30%,-30%);"></div>
      <div class="absolute bottom-0 left-0 w-56 h-56 rounded-full opacity-10" style="background:#fff; transform:translate(-30%,30%);"></div>

      <div class="relative max-w-3xl mx-auto text-center">
        <span
          :style="workshop.status === 'completed'
            ? 'background:rgba(255,255,255,0.2); color:#fff;'
            : 'background:rgba(255,255,255,0.2); color:#fff;'"
          class="inline-flex items-center gap-1.5 text-xs font-bold px-4 py-1.5 rounded-full mb-4 border border-white/30"
        >
          <span class="w-1.5 h-1.5 rounded-full inline-block" :style="workshop.status === 'completed' ? 'background:#86efac;' : 'background:#fde68a;'"></span>
          {{ workshop.status === 'completed' ? 'Završena' : 'Aktivna' }}
        </span>

        <h1 class="text-4xl md:text-5xl font-extrabold text-white mb-3 drop-shadow">{{ workshop.title }}</h1>
        <p class="text-purple-200 text-base mb-6">Detalji i ocjene radionice</p>


        <div class="flex justify-center gap-6 flex-wrap">
          <div class="flex items-center gap-2 text-white/80 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
            {{ formatDate(workshop.date) }}
          </div>
          <div class="flex items-center gap-2 text-white/80 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
            {{ workshop.capacity }} polaznika
          </div>
          <div class="flex items-center gap-2 text-white/80 text-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            {{ workshop.location }}
          </div>
        </div>
      </div>
    </div>

    <p v-if="loading" class="text-center text-gray-500 py-20">Učitavanje...</p>
    <p v-else-if="error" class="text-center text-red-500 py-20">{{ error }}</p>

    <div v-else class="max-w-5xl mx-auto px-4 py-10">

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">

        <!-- Opis -->
        <div class="bg-white rounded-2xl shadow-sm border border-purple-100 p-6">
          <h2 class="text-lg font-extrabold text-gray-800 mb-3 flex items-center gap-2">
            <span class="w-8 h-8 rounded-lg flex items-center justify-center text-base" style="background:#ede9fe;">📖</span>
            Opis radionice
          </h2>
          <p class="text-gray-600 text-sm leading-relaxed">{{ workshop.description }}</p>
        </div>

        <!-- Organizator -->
        <div class="bg-white rounded-2xl shadow-sm border border-purple-100 p-6">
          <h2 class="text-lg font-extrabold text-gray-800 mb-4 flex items-center gap-2">
            <span class="w-8 h-8 rounded-lg flex items-center justify-center text-base" style="background:#ede9fe;">👩</span>
            Organizator
          </h2>
          <div class="flex items-center gap-4 mb-4">
            <div class="w-12 h-12 rounded-full flex items-center justify-center text-white font-extrabold text-lg flex-shrink-0"
              style="background: linear-gradient(135deg, #7c3aed, #a855f7);">
              {{ workshop.organizer_name?.charAt(0)?.toUpperCase() || 'O' }}
            </div>
            <div>
              <p class="font-bold text-gray-800">{{ workshop.organizer_name }}</p>
              <p class="text-xs text-gray-400">Organizator radionice</p>
            </div>
          </div>
          <div class="space-y-2 text-sm">
            <div class="flex items-center gap-2 text-gray-600">
              <svg class="w-4 h-4 flex-shrink-0" style="color:#7c3aed;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              {{ workshop.organizer_email }}
            </div>
            <div v-if="workshop.organizer_phone" class="flex items-center gap-2 text-gray-600">
              <svg class="w-4 h-4 flex-shrink-0" style="color:#7c3aed;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.18 2 2 0 0 1 3.6 1h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.6a16 16 0 0 0 6 6l.92-.92a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              {{ workshop.organizer_phone }}
            </div>
          </div>
        </div>

        <!-- Detalji -->
        <div class="bg-white rounded-2xl shadow-sm border border-purple-100 p-6">
          <h2 class="text-lg font-extrabold text-gray-800 mb-4 flex items-center gap-2">
            <span class="w-8 h-8 rounded-lg flex items-center justify-center text-base" style="background:#ede9fe;">📌</span>
            Detalji radionice
          </h2>
          <div class="space-y-3 text-sm text-gray-700">
            <div class="flex items-center justify-between py-2 border-b border-gray-50">
              <span class="text-gray-400">Datum početka</span>
              <span class="font-semibold">{{ formatDate(workshop.date) }}</span>
            </div>
            <div class="flex items-center justify-between py-2 border-b border-gray-50">
              <span class="text-gray-400">Završetak</span>
              <span class="font-semibold">{{ formatDate(workshop.end_time) }}</span>
            </div>
            <div class="flex items-center justify-between py-2 border-b border-gray-50">
              <span class="text-gray-400">Kapacitet</span>
              <span class="font-semibold">{{ workshop.capacity }} polaznika</span>
            </div>
            <div class="flex items-center justify-between py-2">
              <span class="text-gray-400">Slobodna mjesta</span>
              <span class="font-extrabold text-lg" :style="workshop.free_spots === 0 ? 'color:#dc2626;' : 'color:#16a34a;'">
                {{ workshop.free_spots }}
              </span>
            </div>
          </div>

          <div class="flex gap-3 pt-4 mt-2 border-t border-gray-50">
            <router-link to="/workshops"
              class="flex-1 py-2.5 text-center border-2 border-gray-200 rounded-xl font-bold text-sm text-gray-600 hover:bg-gray-50 transition">
              ⬅ Nazad
            </router-link>
           <button
              @click="handleRegistrationClick"
              :disabled="wasRegistered || workshop.free_spots === 0 || isCompleted(workshop)"
              class="flex-1 py-2.5 rounded-xl font-bold text-sm transition"
              :class="(wasRegistered || workshop.free_spots === 0 || isCompleted(workshop))
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed opacity-70'
                : 'text-white hover:opacity-90'"
              :style="!(wasRegistered || workshop.free_spots === 0 || isCompleted(workshop))
                ? 'background: linear-gradient(135deg, #7c3aed, #a855f7);'
                : ''"
              >
               {{
                  isCompleted(workshop)
                    ? `📅 Završena ${formatDateM(workshop.end_time)}`
                  : wasRegistered
                    ? '✓ Prijavljeni'
                   : workshop.free_spots === 0
                    ? '⛔ Popunjeno'
                   : '🎟 Prijavi se'
               }}
            </button>
          </div>
        </div>

        <!-- Slobodna mjesta  -->
        <div class="bg-white rounded-2xl shadow-sm border border-purple-100 p-6 flex flex-col justify-between">
          <h2 class="text-lg font-extrabold text-gray-800 mb-4 flex items-center gap-2">
            <span class="w-8 h-8 rounded-lg flex items-center justify-center text-base" style="background:#ede9fe;">👥</span>
            Popunjenost
          </h2>
          <div>
            <div class="flex justify-between text-sm mb-2">
              <span class="text-gray-400">Prijavljenih</span>
              <span class="font-bold text-gray-700">{{ workshop.capacity - workshop.free_spots }} / {{ workshop.capacity }}</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-3 mb-4">
              <div
                class="h-3 rounded-full transition-all"
                :style="{
                  width: ((workshop.capacity - workshop.free_spots) / workshop.capacity * 100) + '%',
                  background: workshop.free_spots === 0 ? '#dc2626' : 'linear-gradient(90deg, #7c3aed, #a855f7)'
                }"
              ></div>
            </div>
            <div class="text-center py-4 rounded-xl" :style="workshop.free_spots === 0 ? 'background:#fef2f2;' : 'background:#f0fdf4;'">
              <p class="text-3xl font-extrabold" :style="workshop.free_spots === 0 ? 'color:#dc2626;' : 'color:#16a34a;'">
                {{ workshop.free_spots }}
              </p>
              <p class="text-sm font-medium mt-1" :style="workshop.free_spots === 0 ? 'color:#dc2626;' : 'color:#16a34a;'">
                {{ workshop.free_spots === 0 ? 'Popunjeno' : 'slobodnih mjesta' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Ocjene -->
      <div v-if="workshop.status === 'completed'" class="bg-white rounded-2xl shadow-sm border border-purple-100 p-6">
        <h2 class="text-lg font-extrabold text-gray-800 mb-6 flex items-center gap-2">
          <span class="w-8 h-8 rounded-lg flex items-center justify-center text-base" style="background:#ede9fe;">⭐</span>
          Ocjene radionice
        </h2>

        <div class="flex items-center gap-6 mb-6 p-4 rounded-xl" style="background:#f9f7ff;">
          <div class="text-center">
            <p class="text-5xl font-extrabold" style="color:#7c3aed;">{{ ratingsAverage.average.toFixed(1) }}</p>
            <p class="text-xs text-gray-400 mt-1">od 5</p>
          </div>
          <div class="flex-1">
            <div class="flex text-yellow-400 text-xl mb-1">
              <span v-for="i in 5" :key="i">{{ i <= Math.round(ratingsAverage.average) ? '★' : '☆' }}</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="h-2.5 rounded-full" style="background: linear-gradient(90deg, #7c3aed, #a855f7);" :style="{ width: (ratingsAverage.average/5*100) + '%' }"></div>
            </div>
            <p class="text-xs text-gray-400 mt-1">{{ ratingsAverage.count }} ocjena</p>
          </div>
        </div>
        <div v-if="!alreadyRated" class="mb-6 flex justify-center">
          <button
            @click="showRatingModal = true"
            class="px-6 py-3 text-white rounded-xl font-bold text-sm transition hover:opacity-90 flex items-center gap-2"
            style="background: linear-gradient(135deg, #7c3aed, #a855f7);"
          >
            ★ Ocijeni ovu radionicu
          </button>
        </div>

<div v-if="ratings.length > 0" class="space-y-3">
  <div v-for="r in ratings" :key="r.id"
    class="flex items-start gap-3 p-4 rounded-xl border border-gray-50"
    style="background:#fafafa;">
    <div class="w-9 h-9 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0"
      style="background: linear-gradient(135deg, #7c3aed, #a855f7);">
      {{ r.user_name?.charAt(0)?.toUpperCase() || 'U' }}  <!-- ← promjena -->
    </div>
    <div class="flex-1">
      <p class="text-sm font-semibold text-gray-800 mb-1">{{ r.user_name || 'Nepoznat' }}</p>  <!-- ← dodano -->
      <div class="flex text-yellow-400 text-sm mb-1">
        <span v-for="i in 5" :key="i">{{ i <= r.score ? '★' : '☆' }}</span>
      </div>
      <p class="text-sm text-gray-600">{{ r.comment || 'Bez komentara' }}</p>
    </div>
  </div>
</div>
        <p v-else class="text-gray-400 text-sm italic text-center py-4">Još nema ocjena za ovu radionicu.</p>
      </div>
    </div>

    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm" @click="showForm = false"></div>
      <div class="relative z-10 w-[600px] shadow-2xl">
        <button @click="showForm = false" class="absolute -top-10 right-0 text-white font-bold flex items-center gap-1">
          Zatvori <span class="text-2xl">×</span>
        </button>
        <div class="bg-white rounded-2xl overflow-hidden">
          <WorkshopRegistrationForm @cancel="showForm = false" @success="handleSuccess" />
        </div>
      </div>
    </div>

    <div v-if="showRatingModal" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm" @click="showRatingModal = false"></div>
      <div class="relative z-10 bg-white rounded-2xl p-8 w-[480px] shadow-2xl">
        <button @click="showRatingModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 text-2xl">×</button>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Ocjenite radionicu</h3>
        <p class="text-sm text-gray-500 mb-6">{{ workshop.title }}</p>
        <div class="flex gap-3 mb-6 justify-center">
          <button
            v-for="n in 5"
            :key="n"
            @click="ratingForm.score = n"
            class="text-4xl transition-transform hover:scale-110"
            :class="n <= ratingForm.score ? 'text-yellow-400' : 'text-gray-300'"
          >★</button>
        </div>
        <textarea
          v-model="ratingForm.comment"
          placeholder="Komentar (opciono)..."
          maxlength="500"
          rows="3"
          class="w-full border border-gray-300 rounded-lg p-3 text-sm focus:outline-none focus:border-purple-400 resize-none mb-4"
        ></textarea>
        <p v-if="ratingError" class="text-red-500 text-xs mb-3">{{ ratingError }}</p>
        <button
          @click="submitRating"
          :disabled="!ratingForm.score || ratingSubmitting"
          class="w-full py-3 text-white rounded-lg font-bold disabled:opacity-50 transition-colors"
          style="background:#7c3aed;"
        >
          {{ ratingSubmitting ? 'Šaljem...' : 'Pošalji ocjenu' }}
        </button>
      </div>
    </div>

  </div>
</template>


<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import WorkshopRegistrationForm from './WorkshopRegistrationForm.vue'
import Swal from 'sweetalert2'
import confetti from 'canvas-confetti'

export default {
  components: { WorkshopRegistrationForm },
  setup() {
    const BASE_URL = import.meta.env.VITE_API_URL
    const route = useRoute()
    const router = useRouter()
    const workshop = ref({})
    const loading = ref(true)
    const error = ref(null)
    const showForm = ref(false)
    const showRatingModal = ref(false)

    const ratings = ref([])
    const ratingsAverage = ref({ average: 0, count: 0 })
    const alreadyRated = ref(false)
    const wasRegistered = ref(false)
    const ratingForm = ref({ score: 0, comment: '' })
    const ratingSubmitting = ref(false)
    const ratingError = ref('')

    const isLoggedIn = computed(() => !!localStorage.getItem('token'))




const formatDateM = (date) => {
  return new Date(date).toLocaleDateString('bs-BA', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const isCompleted = (workshop) => {
  if (!workshop?.end_time) return false
  return new Date(workshop.end_time) < new Date()
}


    const fetchWorkshop = async () => {
      try {
        loading.value = true
        const response = await fetch(`${BASE_URL}/workshops/${route.params.id}`)
        if (!response.ok) throw new Error("Radionica nije pronađena")
        workshop.value = await response.json()

        const token = localStorage.getItem('token')
        if (token) {
          const regRes = await fetch(`${BASE_URL}/workshops/registration/check/${route.params.id}`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          const regData = await regRes.json()
          wasRegistered.value = regData.registered
        }

        if (workshop.value.status === 'completed') {
          await fetchRatings()
        }
      } catch (err) {
        error.value = 'Greška pri učitavanju.'
      } finally {
        loading.value = false
      }
    }

const fetchRatings = async () => {
  const id = route.params.id
  const token = localStorage.getItem('token')

  const [avgRes, listRes] = await Promise.all([
    fetch(`${BASE_URL}/workshops/${id}/ratings/average`),
    fetch(`${BASE_URL}/workshops/${id}/ratings`)
  ])

  ratingsAverage.value = await avgRes.json()
  ratings.value = await listRes.json()

  if (token) {
    const regRes = await fetch(`${BASE_URL}/workshops/registration/check/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const regData = await regRes.json()
    wasRegistered.value = regData.registered


const username = localStorage.getItem('username')
alreadyRated.value = ratings.value.some(r => r.user_name === username)
  }
}

const submitRating = async () => {
  ratingSubmitting.value = true
  ratingError.value = ''
  const token = localStorage.getItem('token')

  if (!token) {
    ratingError.value = 'Morate biti prijavljeni da biste ocijenili radionicu.'
    ratingSubmitting.value = false
    return
  }

  try {
    const res = await fetch(`${BASE_URL}/workshops/${route.params.id}/ratings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        score: ratingForm.value.score,
        comment: ratingForm.value.comment || null
      })
    })

    if (!res.ok) {
      const err = await res.json()
      const poruka = err.detail === 'Could not validate credentials'
        ? 'Morate biti prijavljeni da biste ocijenili radionicu.'
        : err.detail || 'Greška pri slanju ocjene.'
      ratingError.value = poruka
      return
    }

    localStorage.setItem(`rated_${route.params.id}`, '1')
    alreadyRated.value = true
    showRatingModal.value = false

    confetti({
      particleCount: 120,
      spread: 80,
      origin: { y: 0.6 },
      colors: ['#7c3aed', '#9333ea', '#a78bfa', '#fbbf24', '#34d399']
    })

    await fetchRatings()
  } catch {
    ratingError.value = 'Greška pri slanju ocjene.'
  } finally {
    ratingSubmitting.value = false
  }
}
    const handleRegistrationClick = () => {
      if (wasRegistered.value) return

      const token = localStorage.getItem('token')
      if (!token) {
        Swal.fire({
          title: 'Niste prijavljeni!',
          text: 'Morate biti prijavljeni na svoj nalog da biste rezervisali mjesto na radionici.',
          icon: 'info',
          showCancelButton: true,
          confirmButtonColor: '#9333ea',
          cancelButtonColor: '#6b7280',
          confirmButtonText: 'Prijavi se odmah',
          cancelButtonText: 'Odustani',
          customClass: {
            popup: 'rounded-[2rem]',
            confirmButton: 'rounded-xl px-6 py-3 font-bold',
            cancelButton: 'rounded-xl px-6 py-3 font-bold'
          }
        }).then((result) => {
          if (result.isConfirmed) router.push('/login')
        })
      } else {
        showForm.value = true
      }
    }

    const handleSuccess = () => {
      showForm.value = false
      wasRegistered.value = true
      fetchWorkshop()
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const d = new Date(dateString)
      return `${String(d.getDate()).padStart(2, '0')}.${String(d.getMonth() + 1).padStart(2, '0')}.${d.getFullYear()}`
    }

    onMounted(fetchWorkshop)

    return {
      workshop, loading, error, showForm, showRatingModal,
      ratings, ratingsAverage, alreadyRated, wasRegistered,
      ratingForm, ratingSubmitting, ratingError, isLoggedIn,isCompleted,
      handleSuccess, formatDate, formatDateM, handleRegistrationClick, submitRating
    }
  }
}
</script>