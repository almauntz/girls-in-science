<template>
  <div 
    class="bg-white border border-gray-200 rounded-xl px-6 py-4 cursor-pointer hover:shadow-md transition"
    @click="$router.push(`/news/${newsPost.id}`)"
  >
    <div class="flex flex-wrap gap-2 mb-2" v-if="newsPost.categories && newsPost.categories.length > 0">
      <span
        v-for="category in newsPost.categories"
        :key="category.id"
        class="bg-primary text-white text-xs px-2 py-1 rounded-full"
      >
        {{ category.name }}
      </span>
    </div>
    <h2 class="font-semibold text-gray-900 mb-1">{{ newsPost.title }}</h2>
    <p class="text-sm text-gray-500">{{ formatDate(newsPost.created_at) }}</p>
  </div>
</template>

<script setup>
defineProps({
  newsPost: Object
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('bs-BA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>