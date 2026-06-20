<template>
  <div class="bg-white rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-300 p-6 flex flex-col items-center text-center gap-4">

    <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-100 flex items-center justify-center">
      <img
        v-if="mentor.avatar_url"
        :src="mentor.avatar_url"
        :alt="mentor.full_name"
        class="w-full h-full object-cover"
      />
      <span v-else class="text-3xl text-gray-400">👤</span>
    </div>

    <h3 class="text-lg font-semibold text-gray-800">
      {{ mentor.full_name }}
    </h3>

    <span class="px-3 py-1 rounded-full text-sm font-medium text-white"
          :style="{ backgroundColor: badgeColor }">
      {{ mentor.field_of_expertise }}
    </span>

    <router-link
      :to="`/mentoring/${mentor.id}`"
      class="mt-2 w-full bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition-colors duration-200"
    >
      Pogledaj profil
    </router-link>

  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  mentor: {
    type: Object,
    required: true
  }
})

const BADGE_COLORS = {
  'Softverski inženjering': '#7C3AED',
  'Mašinsko učenje': '#2563EB',
  'Bioinformatika': '#059669',
  'Telekomunikacije': '#D97706',
  'Biologija': '#16A34A',
  'Fizika': '#DC2626',
  'Hemija': '#0891B2',
  'IT': '#7C3AED' // Dodano i 'IT' pošto smo vidjeli da ga imaš u bazi kod Ane Anić
}

const badgeColor = computed(() => {
  return BADGE_COLORS[props.mentor.field_of_expertise] ?? '#6B7280'
})
</script>