<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">Uredi profil</h1>

    <div v-if="loadError" class="text-red-500 mb-4">{{ loadError }}</div>

    <div v-if="successMessage" class="text-green-600 mb-4">{{ successMessage }}</div>

    <form v-if="form" @submit.prevent="handleSubmit" class="space-y-4">

      <div>
        <label class="block text-sm font-medium mb-1">Ime *</label>
        <input v-model="form.first_name" type="text"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400" />
        <p v-if="errors.first_name" class="text-red-500 text-sm mt-1">{{ errors.first_name }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Prezime *</label>
        <input v-model="form.last_name" type="text"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400" />
        <p v-if="errors.last_name" class="text-red-500 text-sm mt-1">{{ errors.last_name }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">STEM oblast *</label>
        <input v-model="form.stem_field" type="text"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400" />
        <p v-if="errors.stem_field" class="text-red-500 text-sm mt-1">{{ errors.stem_field }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Institucija *</label>
        <input v-model="form.institution" type="text"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400" />
        <p v-if="errors.institution" class="text-red-500 text-sm mt-1">{{ errors.institution }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Pozicija/zvanje *</label>
        <input v-model="form.position" type="text"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400" />
        <p v-if="errors.position" class="text-red-500 text-sm mt-1">{{ errors.position }}</p>
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Biografija</label>
        <textarea v-model="form.biography" rows="4"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400" />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Postignuća</label>
        <textarea v-model="form.achievements" rows="4"
          class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-400" />
      </div>

      <div class="flex gap-4 pt-2">
        <button type="submit"
          class="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700 disabled:opacity-50"
          :disabled="submitting">
          {{ submitting ? 'Čuvanje...' : 'Sačuvaj izmjene' }}
        </button>
        <router-link :to="`/role-models/${route.params.id}`"
          class="px-6 py-2 rounded border hover:bg-gray-100">
          Odustani
        </router-link>
      </div>

    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getRoleModel, updateRoleModel } from '@/services/api.js'

const route = useRoute()
const router = useRouter()

const form = ref(null)
const errors = ref({})
const submitting = ref(false)
const loadError = ref(null)
const successMessage = ref(null)

onMounted(async () => {
  try {
    const data = await getRoleModel(route.params.id)
    if (data.detail) {
      loadError.value = 'Profil nije pronađen.'
    } else {
      form.value = {
        first_name: data.first_name,
        last_name: data.last_name,
        stem_field: data.stem_field,
        institution: data.institution,
        position: data.position,
        biography: data.biography || '',
        achievements: data.achievements || ''
      }
    }
  } catch {
    loadError.value = 'Greška pri učitavanju profila.'
  }
})

function validate() {
  errors.value = {}
  const required = ['first_name', 'last_name', 'stem_field', 'institution', 'position']
  for (const field of required) {
    if (!form.value[field] || !form.value[field].trim()) {
      errors.value[field] = 'Ovo polje je obavezno.'
    }
  }
  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return
  submitting.value = true
  successMessage.value = null
  try {
    const result = await updateRoleModel(route.params.id, form.value)
    if (result.detail) {
      loadError.value = result.detail
    } else {
      successMessage.value = 'Profil je uspješno ažuriran!'
      setTimeout(() => {
        router.push(`/role-models/${route.params.id}`)
      }, 1500)
    }
  } catch {
    loadError.value = 'Greška pri čuvanju. Pokušaj ponovo.'
  } finally {
    submitting.value = false
  }
}
</script>