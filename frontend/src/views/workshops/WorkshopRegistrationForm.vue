<template>
  <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Forma za prijavu na radionicu</h2>
    
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
          class="flex-1 px-6 py-2 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          {{ loading ? 'Slanje...' : 'Prijavi se' }}
        </button>
        <button
          type="button"
          @click="$emit('cancel')"
          class="flex-1 px-6 py-2 border border-gray-400 text-gray-600 font-bold rounded-lg hover:bg-gray-100"
        >
          Odustani
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { registerForWorkshop } from '../../services/api.js'
import Swal from 'sweetalert2'

export default {
  emits: ['cancel', 'success'],
  setup(props, { emit }) {
    const route = useRoute()
    const loading = ref(false)
    const touched = ref({ first_name: false, last_name: false, email: false, phone: false })
    
    const formData = ref({
      first_name: '', last_name: '', email: '', phone: '',
      workshop_id: parseInt(route.params.id),
      previous_experience: '', github_profile: ''
    })

    const submitForm = async () => {
      Object.keys(touched.value).forEach(k => touched.value[k] = true)
      
      if (!formData.value.first_name || !formData.value.last_name || !formData.value.email || !formData.value.phone) {
        Swal.fire('Pažnja', 'Popunite obavezna polja označena crvenom bojom.', 'warning')
        return
      }

      try {
        loading.value = true
        const token = localStorage.getItem('token')
        await registerForWorkshop(formData.value, token)
        
        await Swal.fire({
          title: 'Uspješno!',
          text: 'Prijavljeni ste na radionicu.',
          icon: 'success',
          timer: 2500,
          showConfirmButton: false
        })
        emit('success')
      } catch (err) {
        Swal.fire('Greška', err.message || 'Greška pri prijavi.', 'error')
      } finally {
        loading.value = false
      }
    }

    return { formData, touched, loading, submitForm }
  }
}
</script>