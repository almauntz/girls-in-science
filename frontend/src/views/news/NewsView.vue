<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <div
      class="bg-gradient-to-r from-primary to-secondary rounded-3xl shadow-lg rounded-3xl p-10 text-center text-white mb-10 shadow-lg"
    >
      <h1 class="text-4xl font-bold mb-3">Blog i vijesti</h1>

      <p class="text-lg text-violet-100 max-w-2xl mx-auto">
        Pratite aktivnosti centra, uspjehe žena u STEM-u i najnovije događaje.
      </p>
    </div>
    <div class="flex justify-center mb-10" v-if="isAdmin">
      <router-link
        to="/news/create"
        class="bg-primary hover:bg-secondary text-white font-medium px-6 py-3 rounded-xl transition"
      >
        Kreiraj objavu
      </router-link>
    </div>

    <div v-if="isAdmin" class="flex gap-2 mb-4">
      <input
        v-model="newCategory"
        placeholder="Nova kategorija..."
        class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
      />
      <button
        @click="addCategory"
        class="bg-primary hover:bg-secondary text-white font-medium px-3 py-2 rounded-xl transition"
      >
        Dodaj kategoriju
      </button>
    </div>

    <div class="flex flex-wrap gap-2 mb-6">
      <button
        @click="selectedCategory = null"
        :class="
          selectedCategory === null
            ? 'bg-primary text-white'
            : 'bg-secondary text-white'
        "
        class="px-4 py-2 rounded-full text-sm font-medium transition"
      >
        Sve
      </button>
      <button
        v-for="category in sortedCategories"
        :key="category.id"
        @click="selectedCategory = category.name"
        :class="
          selectedCategory === category.name
            ? 'bg-primary text-white'
            : 'bg-secondary text-white'
        "
        class="px-4 py-2 rounded-full text-sm font-medium transition"
      >
        {{ category.name }}
      </button>
    </div>

    <div v-if="loading" class="text-center text-gray-500">Učitavanje...</div>

    <div
      v-else-if="filteredPosts.length === 0"
      class="text-center text-gray-500 py-12"
    >
      Trenutno nema objava.
    </div>

    <div v-else class="grid md:grid-cols-2 gap-6">
      <NewsCard v-for="post in filteredPosts" :key="post.id" :newsPost="post" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import {
  getMe,
  getNewsPosts,
  getCategories,
  createCategory,
} from "../../services/api.js";
import NewsCard from "../../components/NewsCard.vue";

const newsPosts = ref([]);
const categories = ref([]);
const loading = ref(true);
const isAdmin = ref(false);
const selectedCategory = ref(null);
const newCategory = ref("");

const sortedCategories = computed(() => {
  return [...categories.value].sort((a, b) => a.name.localeCompare(b.name));
});

const filteredPosts = computed(() => {
  if (!selectedCategory.value) return newsPosts.value;
  return newsPosts.value.filter(
    (post) =>
      post.categories &&
      post.categories.some((c) => c.name === selectedCategory.value),
  );
});

onMounted(async () => {
  const token = localStorage.getItem("token");
  if (token) {
    const user = await getMe(token);
    isAdmin.value = user.role === "admin";
  }
  newsPosts.value = await getNewsPosts();
  const cats = await getCategories();
  categories.value = Array.isArray(cats) ? cats : [];
  loading.value = false;
});

async function addCategory() {
  if (!newCategory.value.trim()) return;
  const token = localStorage.getItem("token");
  if (!token) return;
  try {
    const category = await createCategory(
      { name: newCategory.value.trim() },
      token,
    );
    categories.value.push(category);
    newCategory.value = "";
  } catch (error) {
    console.error("Greška pri kreiranju kategorije:", error);
  }
}
</script>
