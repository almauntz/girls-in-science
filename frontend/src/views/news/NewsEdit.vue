<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-10">
        <div class="text-5xl mb-4">✏️</div>

        <h1 class="text-4xl font-bold text-gray-900 mb-2">Uredi objavu</h1>

        <p class="text-gray-500 text-lg">Ažuriraj informacije o objavi</p>
      </div>
      <div class="bg-white rounded-3xl shadow-lg p-8">
        <div
          v-if="serverError"
          class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
        >
          {{ serverError }}
        </div>
        <div
          v-if="successMessage"
          class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
        >
          {{ successMessage }}
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-8">
          Osnovne informacije
        </h2>
        <!-- Naslov -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Naslov <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.title"
            type="text"
            placeholder="Unesite naslov"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            :class="{ 'border-red-400': errors.title }"
          />
          <p v-if="errors.title" class="text-red-500 text-xs mt-1">
            {{ errors.title }}
          </p>
        </div>

        <!-- Sadržaj -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Sadržaj <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="form.content"
            placeholder="Unesite sadržaj"
            rows="6"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 resize-y"
            :class="{ 'border-red-400': errors.content }"
          ></textarea>
          <p v-if="errors.content" class="text-red-500 text-xs mt-1">
            {{ errors.content }}
          </p>
        </div>

        <!-- Slika -->
        <!-- Slika -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">Naslovna slika</label>
          <label class="cursor-pointer block relative">
            <img
              v-if="imagePreview"
              :src="imagePreview"
              class="w-full h-48 object-cover rounded-xl border border-gray-200"
            />
            <button
              v-if="imagePreview"
              type="button"
              @click.stop="removeImage"
              class="absolute top-2 right-2 w-7 h-7 rounded-full bg-red-500 text-white text-xs flex items-center justify-center hover:bg-red-600 shadow-md border-2 border-white"
            >
              ✕
            </button>
            <div
              v-else
              class="w-full h-48 rounded-xl bg-violet-50 text-violet-400 flex items-center justify-center text-4xl hover:bg-violet-100 transition"
            >
              📷
            </div>
            <input type="file" accept="image/*" class="hidden" @change="handleImageChange" />
          </label>
        </div>

        <!-- Povezani profili -->
        <div class="mb-6">
          <label class="block mb-2 font-medium"> Povezani profili </label>
          <div v-if="allRoleModels.length === 0" class="text-sm text-gray-400">
            Učitavanje profila...
          </div>
          <Multiselect
            v-model="form.role_model_ids"
            :options="roleModelOptions"
            mode="tags"
            searchable
            placeholder="Pretraži i odaberi profile"
            class="multiselect-violet"
          />
        </div>

        <div class="mb-8">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Kategorije
          </label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="category in allCategories"
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

        <!-- Dugmad -->
        <div class="flex gap-4">
          <button
            @click.once="handleSubmit"
            :disabled="isLoading"
            class="bg-gradient-to-r from-violet-600 to-purple-600 text-white font-medium px-8 py-3 rounded-xl hover:shadow-lg transition disabled:opacity-50"
          >
            {{ isLoading ? "Čuvanje..." : "Sačuvaj izmjene" }}
          </button>
          <button
            @click="$router.push(`/news/${route.params.id}`)"
            class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-6 py-3 rounded-xl transition"
          >
            Otkaži
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import {
  getNewsPost,
  updateNewsPost,
  getRoleModels,
  getCategories,
  uploadNewsImage,
} from "../../services/api.js";
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";

const router = useRouter();
const route = useRoute();

const form = ref({
  title: "",
  content: "",
  image_url: "",
  role_model_ids: [],
  category_ids: [],
});

const errors = ref({});
const serverError = ref("");
const successMessage = ref("");
const isLoading = ref(false);
let isSubmitting = false
const allRoleModels = ref([]);
const allCategories = ref([]);
const roleModelOptions = ref([]);
const selectedImage = ref(null)
const imagePreview = ref(null)

onMounted(async () => {
  try {
    const [newsData, roleModels, categoriesData] = await Promise.all([
      getNewsPost(route.params.id),
      getRoleModels(),
      getCategories(),
    ]);
    if (newsData.detail) {
      serverError.value = "Objava nije pronađena.";
      return;
    }
    form.value = {
      title: newsData.title,
      content: newsData.content,
      image_url: newsData.image_url || "",
      role_model_ids: newsData.role_models?.map((m) => m.id) || [],
      category_ids: newsData.categories?.map((c) => c.id) || [],
    };
    if (newsData.image_url) {
      imagePreview.value = `http://localhost:8000${newsData.image_url}`
    }
    allRoleModels.value = roleModels;
    roleModelOptions.value = roleModels.map((model) => ({
      value: model.id,
      label: `${model.first_name} ${model.last_name}`,
    }));
    allCategories.value = [...categoriesData].sort((a, b) =>
      a.name.localeCompare(b.name),
    );
  } catch {
    serverError.value = "Greška pri učitavanju objave.";
  }
});

function validate() {
  const e = {};
  if (!form.value.title.trim()) e.title = "Naslov je obavezan";
  if (!form.value.content.trim()) e.content = "Sadržaj je obavezan";
  errors.value = e;
  return Object.keys(e).length === 0;
}

function handleImageChange(event) {
  const file = event.target.files[0]
  if (!file) return
  selectedImage.value = file
  imagePreview.value = URL.createObjectURL(file)
}

function removeImage() {
  imagePreview.value = null
  selectedImage.value = null
  form.value.image_url = null
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
  serverError.value = "";
  successMessage.value = "";
  if (!validate()) {
    isSubmitting = false
    return;
  }
  isLoading.value = true;
  try {
    if (selectedImage.value) {
      const formData = new FormData()
      formData.append("file", selectedImage.value)
      const uploadResponse = await uploadNewsImage(formData)
      form.value.image_url = uploadResponse.image_url
    }

    const result = await updateNewsPost(route.params.id, form.value);
    if (result.id) {
      successMessage.value = "Objava je uspješno ažurirana!";
      setTimeout(() => router.push(`/news/${route.params.id}`), 1500);
    } else {
      serverError.value =
        result.detail || "Došlo je do greške. Pokušajte ponovo.";
    }
  } catch {
    serverError.value = "Greška pri komunikaciji sa serverom.";
  } finally {
    isLoading.value = false;
    isSubmitting = false
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
