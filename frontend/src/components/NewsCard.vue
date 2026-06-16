<template>
  <div 
    class="bg-white border border-gray-200 rounded-xl px-6 py-4 cursor-pointer hover:shadow-md transition"
    @click="$router.push(`/news/${newsPost.id}`)"
  >
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