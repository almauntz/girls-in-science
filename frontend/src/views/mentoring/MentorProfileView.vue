<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-2xl mx-auto">

      <!-- Nazad dugme — samo za admina -->
      <button
        v-if="isAdmin"
        @click="router.push('/admin/mentor-applications')"
        class="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 transition-colors mb-6"
      >
        ← Nazad na Admin Panel
      </button>

      <!-- Placeholder dok kolegica ne implementira -->
      <div class="bg-white rounded-xl border border-gray-200 p-8 text-center text-gray-400">
        <p>Profil mentorice — coming soon</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isAdmin = computed(() => {
  const token = localStorage.getItem('token')
  if (!token) return false
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.role === 'admin'
  } catch {
    return false
  }
})
</script>