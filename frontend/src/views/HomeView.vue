<template>
  <div class="text-center py-20">
    <h1 class="text-4xl font-bold text-primary mb-4">
      Dobrodošle u Girls in Science
    </h1>
    <p class="text-lg text-gray-500 max-w-xl mx-auto mb-8">
      Platforma za mlade naučnice — pronađi mentora, prijavi se na workshop, poveži se sa zajednicom.
    </p>
    <div class="flex justify-center gap-4">
      <router-link to="/register" class="bg-primary text-white px-6 py-3 rounded-lg hover:bg-violet-700 transition font-medium">
        Pridruži se
      </router-link>
      <router-link to="/workshops" class="border border-primary text-primary px-6 py-3 rounded-lg hover:bg-primary hover:text-white transition font-medium">
        Istraži workshops
      </router-link>
    </div>
  </div>
</template>