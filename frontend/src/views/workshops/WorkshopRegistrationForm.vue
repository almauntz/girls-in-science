<template>
  <div class="bg-white p-8 rounded-2xl">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Prijava na radionicu</h2>
    
    <form @submit.prevent="submitForm" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Ime *</label>
          <input
            v-model="formData.first_name"
            @blur="touched.first_name = true"
            type="text"
            required
            class="w-full px-4 py-2 border rounded-lg transition-all focus:outline-none focus:ring-2"
            :class="touched.first_name && !formData.first_name 
              ? 'border-red-500 ring-2 ring-red-100' 
              : 'border-gray-300 focus:ring-purple-500'"
            placeholder="Unesite ime"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Prezime *</label>
          <input
            v-model="formData.last_name"
            @blur="touched.last_name = true"
            type="text"
            required
            class="w-full px-4 py-2 border rounded-lg transition-all focus:outline-none focus:ring-2"
            :class="touched.last_name && !formData.last_name 
              ? 'border-red-500 ring-2 ring-red-100' 
              : 'border-gray-300 focus:ring-purple-500'"
            placeholder="Unesite prezime"
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
        <input
          v-model="formData.email"
          @blur="touched.email = true"
          type="email"
          required
          class="w-full px-4 py-2 border rounded-lg transition-all focus:outline-none focus:ring-2"
          :class="touched.email && !formData.email 
            ? 'border-red-500 ring-2 ring-red-100' 
            : 'border-gray-300 focus:ring-purple-500'"
          placeholder="Unesite email"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Telefon *</label>
        <input
          v-model="formData.phone"
          @blur="touched.phone = true"
          type="tel"
          required
          class="w-full px-4 py-2 border rounded-lg transition-all focus:outline-none focus:ring-2"
          :class="touched.phone && !formData.phone 
            ? 'border-red-500 ring-2 ring-red-100' 
            : 'border-gray-300 focus:ring-purple-500'"
          placeholder="Unesite broj telefona"
        />
      </div>

      <div>
        <label class="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
          GitHub profil <span class="text-gray-400 font-normal">(opciono)</span>
          
          <div class="relative group cursor-help">
            <span class="inline-flex items-center justify-center w-4 h-4 text-[10px] font-bold text-gray-400 border border-gray-300 rounded-full group-hover:border-purple-500 group-hover:text-purple-500 transition-colors">
              ?
            </span>
            
            <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block w-48 p-2 bg-gray-900 text-white text-[11px] leading-tight rounded-lg shadow-xl z-50 text-center font-normal">
              Ovo nam pomaže da vidimo tvoje dosadašnje projekte.
              <div class="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-gray-900"></div>
            </div>
          </div>
        </label>

        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
            github.com/
          </span>
          <input
            v-model="formData.github_profile"
            type="text"
            class="w-full px-4 py-2 pl-[95px] border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all"
            placeholder="korisnicko-ime"
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Prethodno iskustvo (opciono)</label>
        <textarea
          v-model="formData.previous_experience"
          rows="3"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="Opišite vaše iskustvo..."
        ></textarea>
      </div>

      <div class="flex gap-4 pt-6">
        <button
          type="submit"
          :disabled="loading"
          class="flex-1 px-6 py-3 bg-purple-600 text-white font-bold rounded-xl shadow-[0_10px_20px_-5px_rgba(147,51,234,0.5)] hover:shadow-[0_15px_25px_-5px_rgba(147,51,234,0.6)] hover:-translate-y-1 active:translate-y-0.5 transition-all duration-200 disabled:opacity-50 uppercase tracking-wide"
        >
          {{ loading ? 'Slanje...' : 'Prijavi se ' }}
        </button>
        
        <button
          type="button"
          @click="$emit('cancel')"
          class="flex-1 px-6 py-3 border border-gray-300 text-gray-600 font-bold rounded-xl 
           bg-white shadow-sm
           hover:shadow-md hover:bg-gray-50
           hover:-translate-y-1 active:translate-y-0.5 
           transition-all duration-200 uppercase tracking-wide"
          >
          Odustani
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { registerForWorkshop, getMe } from '../../services/api.js'
import Swal from 'sweetalert2'
import confetti from 'canvas-confetti'

export default {
  emits: ['cancel', 'success'],
  setup(props, { emit }) {
    const route = useRoute()
    const loading = ref(false)

    const touched = ref({
      first_name: false,
      last_name: false,
      email: false,
      phone: false
    })

    const formData = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      workshop_id: parseInt(route.params.id),
      previous_experience: '',
      github_profile: ''
    })

    const fillUserData = async () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const user = await getMe(token)

          if (user?.full_name) {
            const parts = user.full_name.split(' ')
            formData.value.first_name = parts[0] || ''
            formData.value.last_name = parts.slice(1).join(' ') || ''
          }

          formData.value.email = user.email || ''
          if (user.phone) formData.value.phone = user.phone

        } catch (error) {
          console.error("Greška prilikom dohvata korisnika:", error)
        }
      }
    }

    onMounted(() => {
      fillUserData()
    })

    const triggerConfetti = () => {
      const end = Date.now() + 2 * 1000;
      const colors = ['#9333ea', '#ffffff'];

      (function frame() {
        confetti({
          particleCount: 3,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors
        });
        confetti({
          particleCount: 3,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
          colors
        });

        if (Date.now() < end) requestAnimationFrame(frame);
      })();
    }

    const submitForm = async () => {
      const token = localStorage.getItem('token')

      if (!token) {
        Swal.fire({
          title: 'Pažnja!',
          text: 'Morate se prijaviti na nalog da biste izvršili prijavu na radionicu.',
          icon: 'warning',
          confirmButtonColor: '#9333ea'
        })
        return
      }

      Object.keys(touched.value).forEach(k => touched.value[k] = true)

      // 🔴 REQUIRED FIELDS
      if (
        !formData.value.first_name ||
        !formData.value.last_name ||
        !formData.value.email ||
        !formData.value.phone
      ) {
        Swal.fire('Greška', 'Popunite obavezna polja.', 'error')
        return
      }

      // 🔴 PHONE VALIDATION (min 9 cifara)
      const phone = formData.value.phone?.toString().trim()

      if (!/^\d{9,}$/.test(phone)) {
        Swal.fire(
          'Greška',
          'Broj telefona mora imati najmanje 9 cifara.',
          'error'
        )
        return
      }

      try {
        loading.value = true

        await registerForWorkshop(formData.value)

        triggerConfetti()

        await Swal.fire({
          title: 'Uspješno! 🎉',
          text: 'Prijavljeni ste na radionicu.',
          icon: 'success',
          confirmButtonColor: '#9333ea'
        })

        emit('success')

      } catch (err) {
        // 🔥 OVO JE KLJUČNO (FastAPI + fetch/axios safe handling)
        const message =
          err?.response?.data?.detail ||
          err?.data?.detail ||
          err?.detail ||
          'Došlo je do greške.'

        Swal.fire('Greška', message, 'error')

      } finally {
        loading.value = false
      }
    }

    return {
      formData,
      touched,
      loading,
      submitForm
    }
  }
}
</script>