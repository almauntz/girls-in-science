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

       <!-- Datum početka -->
        <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
          <div class="flex-1">
            <p class="font-medium text-gray-800">Datum početka</p>
            <p class="text-sm text-gray-400">{{ formatDate(workshop.date) }}</p>
          </div>
          <p class="font-bold text-gray-700">{{ formatTime(workshop.date) }}</p>
        </div>

        <!-- Datum završetka -->
        <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
          <div class="flex-1">
            <p class="font-medium text-gray-800">Datum završetka</p>
            <p class="text-sm text-gray-400">{{ formatDate(workshop.end_time) }}</p>
          </div>
          <p class="font-bold text-gray-700">{{ formatTime(workshop.end_time) }}</p>
        </div>

        <!-- Lokacija -->
        <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
          <div class="flex-1">
            <p class="font-medium text-gray-800">Lokacija</p>
            <p class="text-sm text-gray-400">{{ workshop.location }}</p>
          </div>
        </div>

        <!-- Kapacitet -->
        <div class="flex items-center gap-4 border-b border-gray-300 pb-4">
          <div class="flex-1">
            <p class="font-medium text-gray-800">Kapacitet</p>
            <p class="text-sm text-gray-400">Broj mjesta</p>
          </div>
          <p class="font-bold text-gray-700">{{ workshop.capacity }} polaznica</p>
        </div>

        <!-- Slobodna mjesta -->
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <p class="font-medium text-gray-800">Slobodna mjesta</p>
            <p class="text-sm text-gray-400">Još uvijek dostupno</p>
          </div>
          <p
            class="font-bold"
            :class="workshop.free_spots === 0 ? 'text-red-500' : 'text-green-600'"
          >
            {{ workshop.free_spots === 0 ? 'Popunjeno' : workshop.free_spots + ' mjesta' }}
          </p>
        </div>

        <!-- Dugmad -->
        <div class="flex gap-4 mt-4">
          <button class="px-5 py-2 rounded-lg border border-gray-400 text-gray-600 hover:bg-gray-200">
            Nazad
          </button>
          <button class="px-5 py-2 rounded-lg bg-primary text-white font-bold hover:bg-purple-700">
            Prijavi se
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

