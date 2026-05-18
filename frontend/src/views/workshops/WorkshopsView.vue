<template>
  <div class="min-h-screen bg-purple-100">
    
    <!-- Hero sekcija -->
    <div class="text-center py-16 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">Pronađi edukativne radionice</h1>
      <p class="text-gray-500 text-lg">Izaberi radionicu i prijavi se u par klikova.</p>
    </div>

    <hr class="border-gray-200" />

    <!-- Lista radionica -->
    <div class="py-12 px-4">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">Aktivne radionice</h2>
      <p class="text-center text-gray-500 mb-10">Klikom na Saznaj više pogledajte detaljne informacije o radionici</p>

      <!-- Poruka ako nema radionica -->
      <p v-if="error" class="text-center text-gray-500 text-lg">{{ error }}</p>

      <!-- Lista kartica -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
        <div
          v-for="workshop in workshops"
          :key="workshop.ID_workshop"
          class="flex flex-row items-center gap-6 bg-white rounded-xl shadow p-6"
        >
          <!-- Sadržaj -->
          <div class="flex flex-col">
            <p class="font-medium text-gray-800">{{ workshop.title }}</p>
            <p class="text-sm text-gray-400 mt-1">
              Datum: {{ formatDate(workshop.date) }} • Lokacija: {{ workshop.location }}
            </p>
            <router-link :to="`/workshops/${workshop.ID_workshop}`"
              class="mt-2 font-bold text-primary hover:underline"> Saznaj više
            </router-link>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getActiveWorkshops } from '../../services/api.js'

const workshops = ref([])
const error = ref(null)

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('bs-BA', {
    day: '2-digit', month: '2-digit', year: 'numeric'
  })
}

onMounted(async () => {
  const data = await getActiveWorkshops()
  if (data.detail) {
    error.value = "Trenutno nema dostupnih radionica."
  } else {
    workshops.value = data
  }
})
</script