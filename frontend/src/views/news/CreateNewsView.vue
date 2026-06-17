<template>
  <div class="max-w-2xl mx-auto p-8">
    <div class="text-center mb-10">
      <div class="text-5xl mb-4">📰</div>

      <h1 class="text-4xl font-bold text-gray-900 mb-2">Kreiraj objavu</h1>

      <p class="text-gray-500 text-lg">Dodajte novu vijest ili blog objavu</p>
    </div>
    <!-- Error -->
    <div v-if="serverError" class="bg-red-100 text-red-700 p-3 rounded mb-4">
      {{ serverError }}
    </div>

    <!-- Success -->
    <div
      v-if="successMessage"
      class="bg-green-100 text-green-700 p-3 rounded mb-4"
    >
      {{ successMessage }}
    </div>

    <div class="bg-white rounded-3xl shadow-lg p-8">
      <h2 class="text-xl font-bold text-gray-900 mb-8">Osnovne informacije</h2>
      <!-- Naslov -->
      <div class="mb-4">
        <label class="block mb-2 font-medium">
          Naslov<span class="text-red-500">*</span>
        </label>

        <input
          v-model="form.title"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          :class="{ 'border-red-500': errors.title }"
        />

        <p v-if="errors.title" class="text-red-500 text-sm mt-1">
          {{ errors.title }}
        </p>
      </div>

      <!-- Sadržaj -->
      <div class="mb-4">
        <label class="block mb-2 font-medium">
          Sadržaj<span class="text-red-500">*</span>
        </label>

        <textarea
          v-model="form.content"
          rows="8"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
        ></textarea>

        <p v-if="errors.content" class="text-red-500 text-sm mt-1">
          {{ errors.content }}
        </p>
      </div>

      <!-- Slika -->
      <div class="mb-6">
        <label class="block mb-2 font-medium"> URL slike </label>

        <input
          v-model="form.image_url"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>
      <h2 class="text-xl font-bold text-gray-900 mb-8 mt-10">
        Povezani sadržaj
      </h2>
      <div class="mb-6">
        <label class="block mb-2 font-medium"> Povezani profili </label>

        <Multiselect
          v-model="form.role_model_ids"
          mode="tags"
          :options="profileOptions"
          valueProp="id"
          label="full_name"
          trackBy="full_name"
          :searchable="true"
          placeholder="Pretraži i odaberi profile"
          class="multiselect-violet"
        />
      </div>

      <div class="mb-6">
        <label class="block mb-2 font-medium">Kategorije</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="toggleCategory(category.id)"
            :class="
              form.category_ids.includes(category.id)
                ? 'bg-violet-600 text-white'
                : 'bg-violet-100 text-violet-700'
            "
            class="px-3 py-1 rounded-full text-sm font-medium transition-all duration-200 hover:shadow-sm hover:-translate-y-0.5"
          >
            {{ category.name }}
          </button>
        </div>
      </div>

      <!-- Dugme -->
      <button
        @click="handleSubmit"
        class="bg-violet-600 hover:bg-violet-700 text-white px-6 py-2 rounded-lg transition"
      >
        Kreiraj objavu
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

import { useRouter } from "vue-router";

import {
  createNewsPost,
  getRoleModels,
  getCategories,
} from "../../services/api.js";
import Multiselect from "@vueform/multiselect";

import "@vueform/multiselect/themes/default.css";

const form = ref({
  title: "",
  content: "",
  image_url: "",
  role_model_ids: [],
  category_ids: [],
});

const errors = ref({});

const successMessage = ref("");

const serverError = ref("");

const router = useRouter();

const roleModels = ref([]);

const categories = ref([]);

import { computed } from "vue";

const profileOptions = computed(() =>
  roleModels.value.map((model) => ({
    id: model.id,
    full_name: `${model.first_name} ${model.last_name}`,
  })),
);
onMounted(async () => {
  roleModels.value = await getRoleModels();
  const cats = await getCategories();
  categories.value = Array.isArray(cats) ? cats : [];
});

function validate() {
  const e = {};

  if (!form.value.title.trim()) {
    e.title = "Naslov je obavezan";
  }

  if (!form.value.content.trim()) {
    e.content = "Sadržaj je obavezan";
  }

  errors.value = e;

  return Object.keys(e).length === 0;
}

function toggleCategory(id) {
  if (form.value.category_ids.includes(id)) {
    form.value.category_ids = form.value.category_ids.filter((c) => c !== id);
  } else {
    form.value.category_ids.push(id);
  }
}

async function handleSubmit() {
  serverError.value = "";

  successMessage.value = "";

  if (!validate()) return;

  try {
    const token = localStorage.getItem("token");

    const result = await createNewsPost(form.value, token);
    if (result.id) {
      successMessage.value = "Objava uspješno kreirana";

      setTimeout(() => {
        router.push("/news");
      }, 2000);
    } else {
      serverError.value = result.detail || "Greška pri kreiranju objave";
    }
  } catch {
    serverError.value = "Greška pri komunikaciji sa serverom";
  }
}
</script>

<style scoped>
:deep(.multiselect-violet) {
  --ms-ring-color: rgb(139 92 246);
  --ms-border-color: #d1d5db;

  --ms-tag-bg: rgb(139 92 246);
  --ms-tag-color: white;

  --ms-option-bg-selected: rgb(139 92 246);
  --ms-option-color-selected: white;

  --ms-option-bg-pointed: rgb(237 233 254);
  --ms-option-color-pointed: rgb(109 40 217);
}

:deep(.multiselect-violet .multiselect) {
  border-radius: 12px;
  min-height: 48px;
}

:deep(.multiselect-violet .multiselect:hover) {
  border-color: rgb(139 92 246);
}

:deep(.multiselect-violet .multiselect.is-active) {
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
}
:deep(.multiselect-tag) {
  border-radius: 9999px !important;
  padding: 4px 10px !important;
}
</style>
