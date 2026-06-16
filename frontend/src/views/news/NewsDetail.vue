<template>
  <div class="max-w-3xl mx-auto px-6 py-10">
    <div v-if="loading" class="text-center text-gray-500">Učitavanje...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else-if="newsPost">

      <router-link to="/news" class="text-sm text-blue-600 hover:underline mb-6 inline-block">
        ← Povratak na listu
      </router-link>

      <div class="bg-white border border-gray-200 rounded-xl p-8">

        <img
          v-if="newsPost.image_url"
          :src="newsPost.image_url"
          class="w-full rounded-lg mb-6 object-cover max-h-64"
        />

        <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ newsPost.title }}</h1>
        <p class="text-sm text-gray-400 mb-1">{{ formatDate(newsPost.created_at) }}</p>
        <p v-if="newsPost.author" class="text-sm text-gray-500 mb-6">Autor: {{ newsPost.author }}</p>

        <div v-if="successMessage" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
          {{ successMessage }}
        </div>

        <div class="flex gap-3 mb-8" v-if="isAdmin">
          <router-link
            :to="`/news/${newsPost.id}/edit`"
            class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-5 py-2 rounded-lg text-sm transition"
          >
            Uredi
          </router-link>
          <button
            @click="showModal = true"
            class="bg-red-600 hover:bg-red-700 text-white font-medium px-5 py-2 rounded-lg text-sm transition"
          >
            Obriši
          </button>
        </div>

        <div class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-2">Sadržaj</h2>
          <p class="text-gray-700 whitespace-pre-line leading-relaxed">{{ newsPost.content }}</p>
        </div>

        <div v-if="newsPost.role_models && newsPost.role_models.length > 0">
          <h2 class="text-lg font-semibold text-gray-900 mb-3">Povezani profili</h2>
          <div class="flex flex-col gap-3">
            <div
              v-for="model in newsPost.role_models"
              :key="model.id"
              @click="$router.push(`/role-models/${model.id}`)"
              class="flex items-center gap-4 border border-gray-200 rounded-xl px-5 py-3 cursor-pointer hover:shadow-md transition"
            >
              <div class="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold flex-shrink-0">
                {{ getInitials(model.first_name, model.last_name) }}
              </div>
              <div>
                <p class="font-semibold text-gray-900">{{ model.first_name }} {{ model.last_name }}</p>
                <p class="text-sm text-blue-600">{{ model.stem_field }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="newsPost.categories && newsPost.categories.length > 0" class="mt-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-3">Kategorije</h2>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="category in newsPost.categories"
              :key="category.id"
              class="bg-violet-100 text-violet-700 text-sm px-3 py-1 rounded-full"
            >
              {{ category.name }}
            </span>
          </div>
        </div>

      </div>
    </div>

    <ConfirmDeleteModal
      v-if="showModal"
      message="Da li ste sigurni da želite obrisati ovu objavu?"
      @confirm="handleDelete"
      @cancel="showModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getNewsPost, deleteNewsPost, getMe } from '../../services/api.js'
import ConfirmDeleteModal from '../../components/ConfirmDeleteModal.vue'

const route = useRoute()
const router = useRouter()
const newsPost = ref(null)
const loading = ref(true)
const error = ref(null)
const isAdmin = ref(false)
const showModal = ref(false)
const successMessage = ref('')

function getInitials(first, last) {
  return `${first?.[0] || ''}${last?.[0] || ''}`.toUpperCase()
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('bs-BA', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}

async function handleDelete() {
  showModal.value = false
  const token = localStorage.getItem('token')
  const result = await deleteNewsPost(newsPost.value.id, token)
  if (result.message) {
    successMessage.value = 'Objava je uspješno obrisana!'
    setTimeout(() => {
      router.push('/news')
    }, 1500)
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    if (token) {
      const user = await getMe(token)
      isAdmin.value = user.role === 'admin'
    }
    const data = await getNewsPost(route.params.id)
    if (data.detail) {
      error.value = 'Objava nije pronađena.'
    } else {
      newsPost.value = data
    }
  } catch {
    error.value = 'Došlo je do greške pri učitavanju objave.'
  } finally {
    loading.value = false
  }
})
</script>