<template>
  <div class="max-w-3xl mx-auto px-6 py-10">
    <div v-if="loading" class="text-center text-gray-500">Učitavanje...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else-if="roleModel">

      <router-link to="/role-models" class="text-sm text-blue-600 hover:underline mb-6 inline-block">
        ← Povratak na listu
      </router-link>

      <div class="bg-white border border-gray-200 rounded-xl p-8">
        <div class="flex items-center gap-6 mb-6">
          <div class="w-20 h-20 rounded-full bg-blue-600 text-white flex items-center justify-center text-2xl font-bold flex-shrink-0">
            {{ getInitials(roleModel.first_name, roleModel.last_name) }}
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ roleModel.first_name }} {{ roleModel.last_name }}</h1>
            <p class="text-blue-600 font-medium">{{ roleModel.stem_field }}</p>
            <p class="text-gray-500">{{ roleModel.institution }}</p>
            <p class="text-gray-400 text-sm">{{ roleModel.position }}</p>
          </div>
        </div>

        <div class="flex gap-3 mb-8" v-if="isAdmin">
          <router-link
            :to="`/role-models/${roleModel.id}/edit`"
            class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-5 py-2 rounded-lg text-sm transition"
          >
            Uredi
          </router-link>
          <button
            @click="handleDelete"
            class="bg-red-600 hover:bg-red-700 text-white font-medium px-5 py-2 rounded-lg text-sm transition"
          >
            Obriši
          </button>
        </div>

        <div class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-2">Biografija</h2>
          <p class="text-gray-700 whitespace-pre-line leading-relaxed">
            {{ roleModel.biography || 'Nema dostupne biografije.' }}
          </p>
        </div>

        <div>
          <h2 class="text-lg font-semibold text-gray-900 mb-2">Postignuća</h2>
          <ul class="list-disc list-inside text-gray-700 space-y-1">
            <li v-for="(achievement, index) in achievements" :key="index">
              {{ achievement }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getRoleModel, deleteRoleModel, getMe } from '../../services/api.js'

const route = useRoute()
const router = useRouter()
const roleModel = ref(null)
const loading = ref(true)
const error = ref(null)
const isAdmin = ref(false)

const achievements = computed(() => {
  if (!roleModel.value?.achievements) return []
  return roleModel.value.achievements.split('\n').filter(a => a.trim())
})

function getInitials(first, last) {
  return `${first?.[0] || ''}${last?.[0] || ''}`.toUpperCase()
}

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
    const token = localStorage.getItem('token')
    if (token) {
      const user = await getMe(token)
      isAdmin.value = user.role === 'admin'
    }
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