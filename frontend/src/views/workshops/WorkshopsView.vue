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

    </div>
  </div>
</template>
