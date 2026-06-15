<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-8 max-w-md w-full mx-4">
      <h2 class="text-xl font-bold text-gray-900 mb-2">Potvrda brisanja</h2>
      <p class="text-gray-600 mb-6">{{ message }}</p>
      <div class="flex gap-4">
        <button
          @click="$emit('confirm')"
          class="bg-red-600 hover:bg-red-700 text-white font-medium px-6 py-2 rounded-lg text-sm transition"
        >
          Obriši
        </button>
        <button
          @click="$emit('cancel')"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-6 py-2 rounded-lg text-sm transition"
        >
          Odustani
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: 'Da li ste sigurni da želite obrisati ovu stavku?'
  }
})

defineEmits(['confirm', 'cancel'])
</script>