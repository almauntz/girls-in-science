<template>
  <div class="max-w-3xl mx-auto p-6">
    <div v-if="loading" class="text-center text-gray-500">
      Učitavanje...
    </div>
    <div v-else-if="error" class="text-center text-red-500">
      {{ error }}
    </div>
    <div v-else-if="roleModel">
      <h1 class="text-3xl font-bold mb-2">
        {{ roleModel.first_name }} {{ roleModel.last_name }}
      </h1>
      <p class="text-purple-600 font-medium mb-1">{{ roleModel.position }}</p>
      <p class="text-gray-600 mb-1">{{ roleModel.institution }}</p>
      <p class="text-gray-500 mb-6">{{ roleModel.stem_field }}</p>
      <div class="mb-6">
        <h2 class="text-xl font-semibold mb-2">Biografija</h2>
        <p class="text-gray-700 whitespace-pre-line">
          {{ roleModel.biography || 'Nema dostupne biografije.' }}
        </p>
      </div>
      <div class="mb-6">
        <h2 class="text-xl font-semibold mb-2">Postignuća</h2>
        <p class="text-gray-700 whitespace-pre-line">
          {{ roleModel.achievements || 'Nema dostupnih postignuća.' }}
        </p>
      </div>
      <router-link
        v-if="isAdmin"
        :to="/role-models/${roleModel.id}/edit"
        class="inline-block bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
      >
        Uredi profil
      </router-link>
      <button
        v-if="isAdmin"
        @click="handleDelete"
        class="inline-block bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 ml-2"
      >
        Obriši profil
      </button>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getRoleModel, deleteRoleModel } from '../../services/api.js'
const route = useRoute()
const router = useRouter()
const roleModel = ref(null)
const loading = ref(true)
const error = ref(null)
const isAdmin = computed(() => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return false
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.role === 'admin'
  } catch {
    return false
  }
})
async function handleDelete() {
  if (!confirm('Da li ste sigurni da želite obrisati ovaj profil?')) return
  const token = localStorage.getItem('token')
  const result = await deleteRoleModel(roleModel.value.id, token)
  if (result.message) {
    router.push('/role-models')
  }
}
onMounted(async () => {
  try {
    const data = await getRoleModel(route.params.id)
    if (data.detail) {
      error.value = 'Profil nije pronađen.'
    } else {
      roleModel.value = data
    }
  } catch {
    error.value = 'Došlo je do greške pri učitavanju profila.'
  } finally {
    loading.value = false
  }
})
</script>