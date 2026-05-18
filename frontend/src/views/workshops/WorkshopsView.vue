<template>
  <div class="min-h-screen bg-purple-100">
    <div class="text-center py-16 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">Pronađi edukativne radionice</h1>
      <p class="text-gray-500 text-lg">Izaberi radionicu i prijavi se u par klikova.</p>
    </div>
    <hr class="border-gray-200" />

    <!-- Lista radionica -->
    <div class="py-12 px-4">
      <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">Aktivne radionice</h2>
      <p class="text-center text-gray-500 mb-10">Klikom na Saznaj više pogledajte detaljne informacije o radionici</p>

     <!-- Poruka-->
    <p v-if="error" class="text-center text-gray-500 text-lg">{{ error }}</p>

    <!-- Lista kartica -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
      <div
        v-for="workshop in workshops"
         :key="workshop.ID_workshop"
         class="flex flex-row items-center gap-6 bg-white rounded-xl shadow p-6"
            >
             </div>
  </div>

    </div>
  </div>
</template>
