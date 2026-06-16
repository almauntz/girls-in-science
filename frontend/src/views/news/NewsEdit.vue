<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4">
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-1">Uredi objavu</h1>
      <p class="text-gray-500 mb-8">Ažuriraj informacije o blog objavi</p>

      <div class="bg-white rounded-xl shadow p-8">
        <div v-if="serverError" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {{ serverError }}
        </div>
        <div v-if="successMessage" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
          {{ successMessage }}
        </div>

        <!-- Naslov -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Naslov <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.title"
            type="text"
            placeholder="Unesite naslov"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            :class="{ 'border-red-400': errors.title }"
          />
          <p v-if="errors.title" class="text-red-500 text-xs mt-1">{{ errors.title }}</p>
        </div>

        <!-- Sadržaj -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Sadržaj <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="form.content"
            placeholder="Unesite sadržaj"
            rows="6"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 resize-y"
            :class="{ 'border-red-400': errors.content }"
          ></textarea>
          <p v-if="errors.content" class="text-red-500 text-xs mt-1">{{ errors.content }}</p>
        </div>

        <!-- Slika -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            URL slike
          </label>
          <input
            v-model="form.image_url"
            type="text"
            placeholder="Unesite URL slike (opcionalno)"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <!-- Povezani profili -->
        <div class="mb-8">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Povezani profili iz direktorija
          </label>
          <div v-if="allRoleModels.length === 0" class="text-sm text-gray-400">Učitavanje profila...</div>
          <div class="flex flex-col gap-2">
            <label
              v-for="model in allRoleModels"
              :key="model.id"
              class="flex items-center gap-3 cursor-pointer"
            >
              <input
                type="checkbox"
                :value="model.id"
                v-model="form.role_model_ids"
                class="accent-purple-600"
              />
              <span class="text-sm text-gray-700">{{ model.first_name }} {{ model.last_name }} — {{ model.stem_field }}</span>
            </label>
          </div>
        </div>

        <div class="mb-8">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Kategorije
          </label>
          <div class="flex flex-wrap gap-2">
           <button
            v-for="category in allCategories"
            :key="category.id"
            @click="toggleCategory(category.id)"
            :class="form.category_ids.includes(category.id) ? 'bg-violet-600 text-white' : 'bg-gray-100 text-gray-700'"
            class="px-3 py-1 rounded-full text-sm font-medium transition"
          >

            {{ category.name }}
            </button>
          </div>
        </div>

        <!-- Dugmad -->
        <div class="flex gap-4">
          <button
            @click="handleSubmit"
            :disabled="isLoading"
            class="bg-purple-700 hover:bg-purple-800 text-white font-medium px-6 py-2 rounded-lg text-sm transition disabled:opacity-50"
          >
            {{ isLoading ? 'Čuvanje...' : 'Sačuvaj izmjene' }}
          </button>
          <button
            @click="$router.push(`/news/${route.params.id}`)"
            class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-6 py-2 rounded-lg text-sm transition"
          >
            Otkaži
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getNewsPost, updateNewsPost, getRoleModels, getCategories } from '../../services/api.js'

const router = useRouter()
const route = useRoute()

const form = ref({
  title: '',
  content: '',
  image_url: '',
  role_model_ids: []
})

const errors = ref({})
const serverError = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const allRoleModels = ref([])
const allCategories = ref([])

onMounted(async () => {
  try {
    const [newsData, roleModels, categoriesData] = await Promise.all([
      getNewsPost(route.params.id),
      getRoleModels(),
      getCategories()
    ])
    if (newsData.detail) {
      serverError.value = 'Objava nije pronađena.'
      return
    }
    form.value = {
      title: newsData.title,
      content: newsData.content,
      image_url: newsData.image_url || '',
      role_model_ids: newsData.role_models?.map(m => m.id) || [],
      category_ids: newsData.categories?.map(c => c.id) || []
    }
    allRoleModels.value = roleModels
    allCategories.value = [...categoriesData].sort((a, b) => a.name.localeCompare(b.name))
  } catch {
    serverError.value = 'Greška pri učitavanju objave.'
  }
})

function validate() {
  const e = {}
  if (!form.value.title.trim()) e.title = 'Naslov je obavezan'
  if (!form.value.content.trim()) e.content = 'Sadržaj je obavezan'
  errors.value = e
  return Object.keys(e).length === 0
}

function toggleCategory(id) {
  if (form.value.category_ids.includes(id)) {
    form.value.category_ids = form.value.category_ids.filter(c => c !== id)
  } else {
    form.value.category_ids.push(id)
  }
}

async function handleSubmit() {
  serverError.value = ''
  successMessage.value = ''
  if (!validate()) return
  isLoading.value = true
  try {
    const result = await updateNewsPost(route.params.id, form.value)
    if (result.id) {
      successMessage.value = 'Objava je uspješno ažurirana!'
      setTimeout(() => router.push(`/news/${route.params.id}`), 1500)
    } else {
      serverError.value = result.detail || 'Došlo je do greške. Pokušajte ponovo.'
    }
  } catch {
    serverError.value = 'Greška pri komunikaciji sa serverom.'
  } finally {
    isLoading.value = false
  }
}
</script>