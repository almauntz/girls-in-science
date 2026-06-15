<template>
  <div class="min-h-screen bg-purple-100">
    <p v-if="loading" class="text-center text-gray-500 py-20 font-medium">Učitavanje...</p>
    <p v-else-if="error" class="text-center text-red-500 py-20 font-medium">{{ error }}</p>

    <div v-else>
      <div class="text-center py-12 px-4">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">{{ workshop.title }}</h1>
      </div>

      <hr class="border-gray-300" />

      <div class="max-w-5xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-2 gap-12">
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Opis radionice</h2>
          <p class="text-gray-600 leading-relaxed">{{ workshop.description }}</p>
          <div class="pt-6">
            <p class="font-semibold text-gray-800">Organizator</p>
            <p class="text-sm text-gray-700">{{ workshop.organizer_name }}</p>
            <p class="text-sm text-gray-600">Email: <a :href="`mailto:${workshop.organizer_email}`" class="text-purple-600">{{ workshop.organizer_email }}</a></p>
            <p class="text-sm text-gray-600">Telefon: {{ workshop.organizer_phone }}</p>
          </div>
        </div>

        <div class="flex flex-col gap-6">
          <h2 class="text-2xl font-bold text-gray-800">Detalji radionice</h2>
          <div class="space-y-4">
            <div>
              <p class="font-semibold text-gray-800">Datum početka</p>
              <p class="text-sm text-gray-600">{{ formatDate(workshop.date) }}</p>
            </div>
            <div>
              <p class="font-semibold text-gray-800">Kapacitet</p>
              <p class="text-sm text-gray-600">{{ workshop.capacity }} polaznika</p>
            </div>
            <div>
              <p class="font-semibold text-gray-800">Slobodna mjesta</p>
              <p class="text-sm" :class="workshop.free_spots === 0 ? 'text-red-500' : 'text-green-600 font-bold'">
                {{ workshop.free_spots }}
              </p>
            </div>

            <div class="flex gap-4 pt-4">
              <router-link to="/workshops" class="px-5 py-2 border-2 border-gray-300 rounded-lg font-bold">Nazad</router-link>
              <button
                @click="handleRegistrationClick"
                :disabled="workshop.free_spots === 0 || workshop.status !== 'upcoming'"
                class="px-5 py-2 bg-purple-600 text-white rounded-lg font-bold hover:bg-purple-700 disabled:opacity-50 transition-colors"
              >
                Prijavi se
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SEKCIJA ZA OCJENE -->
      <div v-if="workshop.status === 'completed'" class="max-w-5xl mx-auto px-6 pb-16">
        <hr class="border-gray-300 mb-10" />
        <h2 class="text-2xl font-bold text-gray-800 mb-6">Ocjene radionice</h2>

        <!-- Prosjek -->
        <div class="bg-white rounded-2xl p-6 mb-8 flex items-center gap-6 shadow-sm">
          <div class="text-center">
            <p class="text-5xl font-bold text-purple-600">{{ ratingsAverage.average || '—' }}</p>
            <p class="text-sm text-gray-500 mt-1">od 5</p>
          </div>
          <div>
            <div class="flex gap-1 text-2xl">
              <span v-for="n in 5" :key="n" :class="n <= Math.round(ratingsAverage.average) ? 'text-yellow-400' : 'text-gray-300'">★</span>
            </div>
            <p class="text-sm text-gray-500 mt-1">{{ ratingsAverage.count }} ocjena</p>
          </div>
        </div>

        <!-- Forma za ocjenu -->
        <div v-if="isLoggedIn && wasRegistered && !alreadyRated" class="bg-white rounded-2xl p-6 mb-8 shadow-sm">
          <h3 class="text-lg font-bold text-gray-800 mb-4">Ostavite vašu ocjenu</h3>
          <div class="flex gap-2 mb-4">
            <button
              v-for="n in 5"
              :key="n"
              @click="ratingForm.score = n"
              class="text-3xl transition-transform hover:scale-110"
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
          <button
            @click="submitRating"
            :disabled="!ratingForm.score || ratingSubmitting"
            class="px-6 py-2 bg-purple-600 text-white rounded-lg font-bold hover:bg-purple-700 disabled:opacity-50 transition-colors"
          >
            {{ ratingSubmitting ? 'Šaljem...' : 'Pošalji ocjenu' }}
          </button>
          <p v-if="ratingError" class="text-red-500 text-sm mt-2">{{ ratingError }}</p>
        </div>

        <div v-else-if="alreadyRated" class="bg-green-50 border border-green-200 rounded-2xl p-4 mb-8 text-green-700 text-sm font-medium">
          ✓ Već ste ocjenili ovu radionicu. Hvala!
        </div>

        <!-- Lista ocjena -->
        <div v-if="ratings.length > 0" class="space-y-4">
          <div v-for="r in ratings" :key="r.id" class="bg-white rounded-2xl p-5 shadow-sm">
            <div class="flex items-center gap-2 mb-2">
              <span v-for="n in 5" :key="n" class="text-lg" :class="n <= r.score ? 'text-yellow-400' : 'text-gray-300'">★</span>
              <span class="text-xs text-gray-400 ml-2">{{ formatDate(r.created_at) }}</span>
            </div>
            <p v-if="r.comment" class="text-sm text-gray-600">{{ r.comment }}</p>
          </div>
        </div>
        <p v-else class="text-gray-500 text-sm">Još nema ocjena za ovu radionicu.</p>
      </div>
    </div>

    <!-- Modal za registraciju -->
    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center">
      <div class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm" @click="showForm = false"></div>
      <div class="relative z-10 w-[600px] shadow-2xl animate-in fade-in zoom-in duration-200">
        <button @click="showForm = false" class="absolute -top-10 right-0 text-white hover:text-purple-300 font-bold flex items-center gap-1">
          Zatvori <span class="text-2xl">×</span>
        </button>
        <div class="bg-white rounded-2xl overflow-hidden">
          <WorkshopRegistrationForm @cancel="showForm = false" @success="handleSuccess" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import WorkshopRegistrationForm from './WorkshopRegistrationForm.vue'
import Swal from 'sweetalert2'

export default {
  components: { WorkshopRegistrationForm },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const workshop = ref({})
    const loading = ref(true)
    const error = ref(null)
    const showForm = ref(false)

    const ratings = ref([])
    const ratingsAverage = ref({ average: 0, count: 0 })
    const alreadyRated = ref(false)
    const wasRegistered = ref(false)
    const ratingForm = ref({ score: 0, comment: '' })
    const ratingSubmitting = ref(false)
    const ratingError = ref('')

    const isLoggedIn = computed(() => !!localStorage.getItem('token'))

    const fetchWorkshop = async () => {
      try {
        loading.value = true
        const response = await fetch(`http://127.0.0.1:8000/workshops/${route.params.id}`)
        if (!response.ok) throw new Error("Radionica nije pronađena")
        workshop.value = await response.json()

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
        fetch(`http://127.0.0.1:8000/workshops/${id}/ratings/average`),
        fetch(`http://127.0.0.1:8000/workshops/${id}/ratings`)
      ])

      ratingsAverage.value = await avgRes.json()
      ratings.value = await listRes.json()

      if (token) {
        // provjeri registraciju
        const regRes = await fetch(`http://127.0.0.1:8000/workshops/registration/check/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        const regData = await regRes.json()
        wasRegistered.value = regData.registered

        // provjeri je li već ocjenila
        const myRatings = ratings.value.filter(r => {
          // ne možemo direktno znati user_id, pa provjeravamo kroz API
          return false
        })

        // bolji način — pokušaj POST pa ako dobijemo 409 znači već je ocijenila
        // jednostavnije: čuvamo u localStorage
        const key = `rated_${id}`
        alreadyRated.value = !!localStorage.getItem(key)
      }
    }

    const submitRating = async () => {
      ratingSubmitting.value = true
      ratingError.value = ''
      const token = localStorage.getItem('token')

      try {
        const res = await fetch(`http://127.0.0.1:8000/workshops/${route.params.id}/ratings`, {
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
          ratingError.value = err.detail || 'Greška pri slanju ocjene.'
          return
        }

        localStorage.setItem(`rated_${route.params.id}`, '1')
        alreadyRated.value = true
        await fetchRatings()
      } catch {
        ratingError.value = 'Greška pri slanju ocjene.'
      } finally {
        ratingSubmitting.value = false
      }
    }

    const handleRegistrationClick = () => {
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
      fetchWorkshop()
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const d = new Date(dateString)
      return `${String(d.getDate()).padStart(2, '0')}.${String(d.getMonth() + 1).padStart(2, '0')}.${d.getFullYear()}`
    }

    onMounted(fetchWorkshop)

    return {
      workshop, loading, error, showForm,
      ratings, ratingsAverage, alreadyRated, wasRegistered,
      ratingForm, ratingSubmitting, ratingError, isLoggedIn,
      handleSuccess, formatDate, handleRegistrationClick, submitRating
    }
  }
}
</script>