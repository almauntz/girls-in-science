<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-8">
        <div class="text-5xl mb-3">📰</div>

        <h1 class="text-3xl font-bold text-gray-900">Kreiraj objavu</h1>

        <p class="text-gray-500 mt-2">
          Dodajte novu vijest ili blog objavu
        </p>
      </div>

      <div class="bg-white rounded-3xl shadow-xl p-10 border border-gray-100">
        <!-- Error -->
        <div v-if="serverError" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {{ serverError }}
        </div>

        <!-- Success -->
        <div v-if="successMessage" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
          {{ successMessage }}
        </div>

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
            :searchable="true"
            placeholder="Pretraži i odaberi profile"
            class="multiselect-violet"
          />
        </div>

        <!-- Slika -->
        <div class="mb-6">
          <label class="block mb-2 font-medium">Naslovna slika</label>
          <label class="cursor-pointer block">
            <img
              v-if="imagePreview"
              :src="imagePreview"
              class="w-full h-48 object-cover rounded-xl border border-gray-200"
            />
            <div
              v-else
              class="w-full h-48 rounded-xl bg-violet-50 text-violet-400 flex items-center justify-center text-4xl hover:bg-violet-100 transition"
            >
              📷
            </div>
            <input type="file" accept="image/*" class="hidden" @change="handleImageChange" />
          </label>
        </div>

        <!-- Dugme -->
        <button
          @click.once="handleSubmit"
          :disabled="isLoading"
          class="bg-violet-600 hover:bg-violet-700 text-white px-6 py-2 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Kreiraj objavu
        </button>
      </div>
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
  uploadNewsImage,
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

let isSubmitting = false
const isLoading = ref(false)

const router = useRouter();



const categories = ref([]);
const selectedImage = ref(null)
const imagePreview = ref(null)

const profileOptions = ref([])

onMounted(async () => {
  const roleModels = await getRoleModels()
  profileOptions.value = roleModels.map(m => ({
    value: m.id,
    label: `${m.first_name} ${m.last_name}`
  }))
  const cats = await getCategories()
  categories.value = Array.isArray(cats) ? cats : []
})

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

function handleImageChange(event) {
  const file = event.target.files[0]
  if (!file) return
  selectedImage.value = file
  imagePreview.value = URL.createObjectURL(file)
}

function toggleCategory(id) {
  if (form.value.category_ids.includes(id)) {
    form.value.category_ids = form.value.category_ids.filter((c) => c !== id);
  } else {
    form.value.category_ids.push(id);
  }
}

async function handleSubmit() {
  if (isSubmitting) return
  isSubmitting = true
  isLoading.value = true
  serverError.value = "";
  successMessage.value = "";
  if (!validate()) {
    isSubmitting = false
    isLoading.value = false
    return;
  }

try {
    const token = localStorage.getItem("token");

    if (selectedImage.value) {
      const formData = new FormData()
      formData.append("file", selectedImage.value)
      const uploadResponse = await uploadNewsImage(formData)
      form.value.image_url = uploadResponse.image_url
    }

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
  } finally {
    isSubmitting = false
    isLoading.value = false
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
