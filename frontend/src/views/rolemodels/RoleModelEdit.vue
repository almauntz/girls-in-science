<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-10">
        <div class="text-5xl mb-4">✏️</div>

        <h1 class="text-4xl font-bold text-gray-900 mb-2">Uredi profil</h1>

        <p class="text-gray-500 text-lg">Ažuriraj informacije o uzoru</p>
      </div>

      <div class="bg-white rounded-3xl shadow-lg p-8">
        <!-- Greška sa servera -->
        <div
          v-if="serverError"
          class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
        >
          {{ serverError }}
        </div>

        <!-- Uspjeh -->
        <div
          v-if="successMessage"
          class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm"
        >
          {{ successMessage }}
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-8">
          Profilna fotografija
        </h2>
        <div class="flex justify-center mb-8">
          <label class="cursor-pointer relative">
            <img
              v-if="imagePreview"
              :src="imagePreview"
              class="w-32 h-32 rounded-full object-cover border-4 border-primary/30 shadow-md"
            />

            <button
              v-if="imagePreview"
              type="button"
              @click.stop="removeImage"
              class="absolute top-0 right-0 w-6 h-6 rounded-full bg-red-500 text-white text-xs flex items-center justify-center hover:bg-red-600 shadow-md border-2 border-white"
            >
              ✕
            </button>

            <div
              v-else
              class="w-32 h-32 rounded-full bg-primary/10 text-primary flex items-center justify-center text-4xl hover:bg-primary/20 transition"
            >
              📷
            </div>

            <input
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleImageChange"
            />
          </label>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-8">
          Osnovne informacije
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <!-- Ime -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Ime <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.first_name"
              type="text"
              placeholder="Unesite ime"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              :class="{ 'border-red-400': errors.first_name }"
            />
            <p v-if="errors.first_name" class="text-red-500 text-xs mt-1">
              {{ errors.first_name }}
            </p>
          </div>

          <!-- Prezime -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Prezime <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.last_name"
              type="text"
              placeholder="Unesite prezime"
              class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              :class="{ 'border-red-400': errors.last_name }"
            />
            <p v-if="errors.last_name" class="text-red-500 text-xs mt-1">
              {{ errors.last_name }}
            </p>
          </div>
        </div>

        <!-- STEM oblast -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            STEM oblast <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.stem_field"
            type="text"
            placeholder="npr. Računarstvo i softverski inženjering"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            :class="{ 'border-red-400': errors.stem_field }"
          />
          <p v-if="errors.stem_field" class="text-red-500 text-xs mt-1">
            {{ errors.stem_field }}
          </p>
        </div>

        <!-- Institucija -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Institucija <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.institution"
            type="text"
            placeholder="npr. Fakultet elektrotehnike, Univerzitet u Tuzli"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            :class="{ 'border-red-400': errors.institution }"
          />
          <p v-if="errors.institution" class="text-red-500 text-xs mt-1">
            {{ errors.institution }}
          </p>
        </div>

        <!-- Pozicija/Zvanje -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Pozicija/Zvanje <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.position"
            type="text"
            placeholder="npr. Docent, Vanredni profesor"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            :class="{ 'border-red-400': errors.position }"
          />
          <p v-if="errors.position" class="text-red-500 text-xs mt-1">
            {{ errors.position }}
          </p>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-8 mt-10">
          Profesionalni podaci
        </h2>
        <!-- Biografija -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Biografija <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="form.biography"
            placeholder="Unesite biografiju"
            rows="5"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-y"
            :class="{ 'border-red-400': errors.biography }"
          ></textarea>
          <p v-if="errors.biography" class="text-red-500 text-xs mt-1">
            {{ errors.biography }}
          </p>
        </div>

        <!-- Postignuća -->
        <div class="mb-8">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Postignuća <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="form.achievements"
            placeholder="Unesite postignuća (svako postignuće u novom redu)"
            rows="5"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary resize-y"
            :class="{ 'border-red-400': errors.achievements }"
          ></textarea>
          <p class="text-gray-400 text-xs mt-1">
            Unesite svako postignuće u novi red
          </p>
          <p v-if="errors.achievements" class="text-red-500 text-xs mt-1">
            {{ errors.achievements }}
          </p>
        </div>

        <!-- Dugmad -->
        <div class="flex gap-4 mt-8">
          <button
            @click.once="handleSubmit"
            :disabled="isLoading"
            class="bg-gradient-to-r from-primary to-secondary text-white font-medium px-8 py-3 rounded-xl hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? "Čuvanje..." : "Sačuvaj izmjene" }}
          </button>
          <button
            @click="$router.push(`/role-models/${route.params.id}`)"
            class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-6 py-2 rounded-lg text-sm transition"
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
  getRoleModel,
  updateRoleModel,
  uploadRoleModelImage,
} from "../../services/api.js";

const router = useRouter();
const route = useRoute();

let isSubmitting = false

const form = ref({
  first_name: "",
  last_name: "",
  stem_field: "",
  institution: "",
  position: "",
  biography: "",
  achievements: "",
  image_url: "",
});

const errors = ref({});
const serverError = ref("");
const successMessage = ref("");
const isLoading = ref(false);
const selectedImage = ref(null);
const imagePreview = ref(null);

function handleImageChange(event) {
  const file = event.target.files[0];

  if (!file) return;

  selectedImage.value = file;
  imagePreview.value = URL.createObjectURL(file);
}
function removeImage() {
  imagePreview.value = null;
  selectedImage.value = null;
  form.value.image_url = null;
}

onMounted(async () => {
  try {
    const data = await getRoleModel(route.params.id);
    if (data.detail) {
      serverError.value = "Profil nije pronađen.";
      return;
    }
    if (data.image_url) {
      imagePreview.value = `http://localhost:8000${data.image_url}`;
    }
    form.value = {
      first_name: data.first_name,
      last_name: data.last_name,
      stem_field: data.stem_field,
      institution: data.institution,
      position: data.position,
      biography: data.biography,
      achievements: data.achievements,
      image_url: data.image_url,
    };
  } catch {
    serverError.value = "Greška pri učitavanju profila.";
  }
});

function validate() {
  const e = {};
  if (!form.value.first_name.trim()) e.first_name = "Ime je obavezno";
  if (!form.value.last_name.trim()) e.last_name = "Prezime je obavezno";
  if (!form.value.stem_field.trim()) e.stem_field = "STEM oblast je obavezna";
  if (!form.value.institution.trim()) e.institution = "Institucija je obavezna";
  if (!form.value.position.trim()) e.position = "Pozicija/Zvanje je obavezno";
  if (!form.value.biography.trim()) e.biography = "Biografija je obavezna";
  if (!form.value.achievements.trim())
    e.achievements = "Postignuća su obavezna";
  errors.value = e;
  return Object.keys(e).length === 0;
}

async function handleSubmit() {
  if (isSubmitting) return
  isSubmitting = true
  isLoading.value = true
  serverError.value = "";
  successMessage.value = "";
  if (!validate()) {
    isLoading.value = false;
    isSubmitting = false
    return;
  }
  try {
    if (selectedImage.value) {
      const formData = new FormData();
      formData.append("file", selectedImage.value);
      const uploadResponse = await uploadRoleModelImage(formData);
      form.value.image_url = uploadResponse.image_url;
    }
    const result = await updateRoleModel(route.params.id, form.value);
    if (result.id) {
      successMessage.value = "Profil je uspješno ažuriran!";
      setTimeout(() => router.push(`/role-models/${route.params.id}`), 1500);
    } else {
      serverError.value = result.detail || "Došlo je do greške. Pokušajte ponovo.";
    }
  } catch {
    serverError.value = "Greška pri komunikaciji sa serverom.";
  } finally {
    isLoading.value = false;
    isSubmitting = false
  }
}
</script>
