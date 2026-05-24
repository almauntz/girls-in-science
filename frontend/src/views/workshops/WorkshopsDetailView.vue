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
    </div> 
    
    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center">
      <div 
        class="absolute inset-0 bg-gray-900/70 backdrop-blur-sm transition-opacity" 
        @click="showForm = false"
      ></div>

      <div class="relative z-10 w-[600px] shadow-2xl animate-in fade-in zoom-in duration-200">
        <button 
          @click="showForm = false" 
          class="absolute -top-10 right-0 text-white hover:text-purple-300 font-bold flex items-center gap-1"
        >
          Zatvori <span class="text-2xl">×</span>
        </button>

        <div class="bg-white rounded-2xl overflow-hidden">
          <WorkshopRegistrationForm 
            @cancel="showForm = false" 
            @success="handleSuccess" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router' // Dodato: useRouter
import WorkshopRegistrationForm from './WorkshopRegistrationForm.vue'
import Swal from 'sweetalert2' // Dodato: Swal uvoz

export default {
  components: { WorkshopRegistrationForm },
  setup() {
    const route = useRoute()
    const router = useRouter() // Dodato: router definicija
    const workshop = ref({})
    const loading = ref(true)
    const error = ref(null)
    const showForm = ref(false)

    const fetchWorkshop = async () => {
      try {
        loading.value = true
        const response = await fetch(`http://127.0.0.1:8000/workshops/${route.params.id}`)
        if (!response.ok) throw new Error("Radionica nije pronađena")
        workshop.value = await response.json()
      } catch (err) { 
        error.value = 'Greška pri učitavanju.' 
      } finally { 
        loading.value = false 
      }
    }

    // Dodata funkcija unutar setup-a
    const handleRegistrationClick = () => {
      const token = localStorage.getItem('token'); 
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
          if (result.isConfirmed) {
            router.push('/login'); 
          }
        });
      } else {
        showForm.value = true;
      }
    };

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
    
    // Dodato handleRegistrationClick u return
    return { 
      workshop, 
      loading, 
      error, 
      showForm, 
      handleSuccess, 
      formatDate, 
      handleRegistrationClick 
    }
  }
}
</script>