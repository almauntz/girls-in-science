<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-3xl font-bold text-gray-900 mb-1">Blog i vijesti</h1>
    <p class="text-gray-500 mb-6">Pratite aktivnosti centra i žene u STEM oblastima</p>

    <div v-if="loading" class="text-center text-gray-500">
      Učitavanje...
    </div>

    <div v-else-if="newsPosts.length === 0" class="text-center text-gray-500 py-12">
      Trenutno nema objava.
    </div>

    <div v-else class="flex flex-col gap-4">
      <NewsCard
        v-for="post in newsPosts"
        :key="post.id"
        :newsPost="post"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getNewsPosts } from '../../services/api.js'
import NewsCard from '../../components/NewsCard.vue'

const newsPosts = ref([])
const loading = ref(true)

onMounted(async () => {
  newsPosts.value = await getNewsPosts()
  loading.value = false
})
</script>