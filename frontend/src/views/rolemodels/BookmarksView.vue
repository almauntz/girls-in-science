<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-3xl font-bold text-gray-900 mb-1">Moji favoriti</h1>
    <p class="text-gray-500 mb-6">Profili koje ste sačuvali</p>

    <div v-if="loading" class="text-center text-gray-500">
      Učitavanje...
    </div>

    <div v-else-if="bookmarks.length === 0" class="text-center text-gray-500 py-12">
      Nemate sačuvanih profila.
    </div>

    <div v-else class="grid md:grid-cols-2 gap-6">
      <div
        v-for="model in bookmarks"
        :key="model.id"
        @click="router.push(`/role-models/${model.id}`)"
        class="bg-white border border-gray-100 rounded-2xl p-6 cursor-pointer hover:shadow-lg transition"
      >
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-full bg-violet-600 text-white flex items-center justify-center font-bold text-lg flex-shrink-0">
            {{ getInitials(model.first_name, model.last_name) }}
          </div>
          <div>
            <p class="font-semibold text-gray-900">{{ model.first_name }} {{ model.last_name }}</p>
            <p class="text-sm text-violet-600 font-medium">{{ model.stem_field }}</p>
            <p class="text-sm text-gray-500">{{ model.institution }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getBookmarks } from '../../services/api.js'

const router = useRouter()
const bookmarks = ref([])
const loading = ref(true)

function getInitials(first, last) {
  return `${first?.[0] || ''}${last?.[0] || ''}`.toUpperCase()
}

onMounted(async () => {
  try {
    const data = await getBookmarks()
    bookmarks.value = Array.isArray(data) ? data : []
  } catch {
    bookmarks.value = []
  } finally {
    loading.value = false
  }
})
</script>