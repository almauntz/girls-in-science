<template>
  <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Forma za prijavu na radionicu</h2>
    
    <form @submit.prevent="submitForm" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Ime *</label>
          <input
            v-model="formData.first_name"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Unesite ime"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Prezime *</label>
          <input
            v-model="formData.last_name"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Unesite prezime"
          />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
        <input
          v-model="formData.email"
          type="email"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="Unesite email"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Telefon *</label>
        <input
          v-model="formData.phone"
          type="tel"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="Unesite broj telefona"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Prethodno iskustvo (opciono)</label>
        <textarea
          v-model="formData.previous_experience"
          rows="3"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="Opišite vaše iskustvo sa ovom temom..."
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">GitHub profil (opciono)</label>
        <input
          v-model="formData.github_profile"
          type="url"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="https://github.com/vas-username"
        />
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

      <div v-if="error" class="text-red-600 text-sm mt-4 p-4 bg-red-50 rounded">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { registerForWorkshop } from '@/services/api'

export default {
  emits: ['cancel', 'success'],
  setup(props, { emit }) {
    const route = useRoute()
    const loading = ref(false)
    const error = ref(null)
    
    const formData = ref({
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      workshop_id: parseInt(route.params.id),
      previous_experience: '',
      github_profile: ''
    })

    const submitForm = async () => {
      try {
        loading.value = true
        error.value = null
        
        const token = localStorage.getItem('token')
        if (!token) {
          error.value = 'Trebate biti ulogovani'
          return
        }

        await registerForWorkshop(formData.value, token)
        
        emit('success')
      } catch (err) {
        error.value = err.message || 'Greška pri registraciji'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    return {
      formData,
      loading,
      error,
      submitForm
    }
  }
}
</script>

<style scoped>
</style>
