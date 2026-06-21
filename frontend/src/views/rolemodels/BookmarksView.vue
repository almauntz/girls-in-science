<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <router-link
      to="/role-models"
      class="inline-flex items-center gap-2 px-4 py-2 bg-white text-primary rounded-xl shadow-sm hover:shadow-md border border-gray-100 transition mb-8"
    >
      ← Nazad na direktorij
    </router-link>
    <div
      class="bg-gradient-to-r from-primary to-secondary rounded-3xl p-10 text-center text-white mb-10 shadow-lg"
    >
      <h1 class="text-4xl font-bold mb-3">Moji favoriti</h1>

      <p class="text-lg text-white/80 max-w-2xl mx-auto">
        Profili koje ste sačuvali za kasnije pregledavanje.
      </p>
    </div>

    <div v-if="loading" class="text-center text-gray-500">Učitavanje...</div>

    <div
      v-else-if="bookmarks.length === 0"
      class="text-center text-gray-500 py-12"
    >
      Nemate sačuvanih profila.
    </div>

    <div v-else class="grid md:grid-cols-2 gap-6">
      <div
        v-for="model in bookmarks"
        :key="model.id"
        @click="router.push({ path: `/role-models/${model.id}`, query: { from: 'bookmarks' } })"
        class="bg-white border border-gray-100 rounded-2xl p-6 cursor-pointer hover:shadow-lg transition"
      >
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 flex-shrink-0">
            <img
              v-if="model.image_url"
              :src="`http://localhost:8000${model.image_url}`"
              class="w-14 h-14 rounded-full object-cover"
            />
            <div
              v-else
              class="w-14 h-14 rounded-full bg-violet-600 text-white flex items-center justify-center font-bold text-lg"
            >
              {{ getInitials(model.first_name, model.last_name) }}
            </div>
          </div>
          <div>
            <p class="font-semibold text-gray-900">
              {{ model.first_name }} {{ model.last_name }}
            </p>
            <p class="text-sm text-violet-600 font-medium">
              {{ model.stem_field }}
            </p>
            <p class="text-sm text-gray-500">{{ model.institution }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getBookmarks } from "../../services/api.js";

const router = useRouter();
const bookmarks = ref([]);
const loading = ref(true);

function getInitials(first, last) {
  return `${first?.[0] || ""}${last?.[0] || ""}`.toUpperCase();
}

onMounted(async () => {
  try {
    const data = await getBookmarks();
    bookmarks.value = Array.isArray(data) ? data : [];
  } catch {
    bookmarks.value = [];
  } finally {
    loading.value = false;
  }
});
</script>
