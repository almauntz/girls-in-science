<template>
  <div class="min-h-screen bg-purple-100">

    <div class="text-center py-12 px-4">
      <h1 class="text-4xl font-bold text-gray-800 mb-2">{{ workshop.title }}</h1>
    </div>

    <hr class="border-gray-300" />

    <!-- Glavni sadržaj -->
    <div class="max-w-5xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-2 gap-12">

      <!-- Opis -->
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Opis radionice</h2>
        <p class="text-gray-600 leading-relaxed whitespace-pre-line">{{ workshop.description }}</p>

        <!-- Organizator -->
        <div class="mt-8">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Organizator</h2>
          <p class="text-gray-800"><span class="font-medium">Ime i prezime:</span> {{ workshop.organizer_name }}</p>
          <p class="text-gray-800"><span class="font-medium">Email:</span> {{ workshop.organizer_email }}</p>
        </div>
      </div>

      <!-- Ključne informacije -->
      <div class="flex flex-col gap-6">
        <h2 class="text-2xl font-bold text-gray-800">Detalji radionice</h2>
        <p class="text-gray-500">Važne informacije na jednom mjestu prije prijave.</p>

            </div>

    </div>
  </div>
</template>

