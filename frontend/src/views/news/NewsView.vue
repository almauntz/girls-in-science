<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-3xl font-bold text-gray-900 mb-1">Blog i vijesti</h1>
    <p class="text-gray-500 mb-6">Pratite aktivnosti centra i žene u STEM oblastima</p>

    <div class="flex justify-end mb-6" v-if="isAdmin">
      <router-link
        to="/news/create"
        class="bg-violet-600 hover:bg-violet-700 text-white px-6 py-2 rounded-lg transition">
        Kreiraj objavu
      </router-link>
    </div>

    <div v-if="isAdmin" class="flex gap-2 mb-4">
  <input
    v-model="newCategory"
    placeholder="Nova kategorija..."
    class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
  />
  <button
    @click="addCategory"
    class="bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg text-sm transition"
  >
    Dodaj kategoriju
  </button>
</div>

    <div class="flex flex-wrap gap-2 mb-6">
      <button
        @click="selectedCategory = null"
        :class="selectedCategory === null ? 'bg-violet-600 text-white' : 'bg-gray-100 text-gray-700'"
        class="px-3 py-1 rounded-full text-sm font-medium transition"
      >
        Sve
      </button>
      <button
        v-for="category in categories"
        :key="category.id"
        @click="selectedCategory = category.name"
        :class="selectedCategory === category.name ? 'bg-violet-600 text-white' : 'bg-gray-100 text-gray-700'"
        class="px-3 py-1 rounded-full text-sm font-medium transition"
      >
        {{ category.name }}
      </button>
    </div>

    <div v-if="loading" class="text-center text-gray-500">
      Učitavanje...
    </div>

    <div v-else-if="filteredPosts.length === 0" class="text-center text-gray-500 py-12">
      Trenutno nema objava.
    </div>

    <div v-else class="flex flex-col gap-4">
      <NewsCard
        v-for="post in filteredPosts"
        :key="post.id"
        :newsPost="post"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getMe, getNewsPosts, getCategories, createCategory} from '../../services/api.js'
import NewsCard from '../../components/NewsCard.vue'

const newsPosts = ref([])
const categories = ref([])
const loading = ref(true)
const isAdmin = ref(false)
const selectedCategory = ref(null)
const newCategory = ref('')

const filteredPosts = computed(() => {
  if (!selectedCategory.value) return newsPosts.value
  return newsPosts.value.filter(post =>
    post.categories && post.categories.includes(selectedCategory.value)
  )
})

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    const user = await getMe(token)
    isAdmin.value = user.role === 'admin'
  }
  newsPosts.value = await getNewsPosts()
  categories.value = await getCategories()
  loading.value = false
})

async function addCategory() {
  if (!newCategory.value.trim()) return

  const token = localStorage.getItem('token')
  if (!token) return

  try {
    const category = await createCategory({ name: newCategory.value.trim() }, token)
    categories.value.push(category)
    newCategory.value = ''
  } catch (error) {
    console.error('Error creating category:', error)
  }
}
</script>