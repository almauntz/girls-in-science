<template>
  <div class="min-h-screen bg-gray-50 py-10 px-4">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-8">
        <div class="text-5xl mb-3">👩‍💻</div>

        <h1 class="text-3xl font-bold text-gray-900">Dodaj novi profil</h1>

        <p class="text-gray-500 mt-2">
          Kreiraj novi profil u direktoriju uzora
        </p>
      </div>
      <div class="bg-white rounded-3xl shadow-xl p-10 border border-gray-100">
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
        <div class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Profilna fotografija
          </h2>

          <div class="flex justify-center mb-8">
            <label class="cursor-pointer">
              <div
                v-if="!imagePreview"
                class="w-32 h-32 rounded-full bg-primary/10 text-primary flex items-center justify-center text-4xl hover:bg-primary/20 transition"
              >
                📷
              </div>

              <img
                v-else
                :src="imagePreview"
                class="w-28 h-28 rounded-full object-cover border-4 border-primary/30"
              />

              <input
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageChange"
              />
            </label>
          </div>
        </div>
        <h2 class="text-lg font-semibold text-gray-900 mb-4">
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
              maxlength="20"
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
              maxlength="20"
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
            maxlength="35"
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
            maxlength="30"
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
            maxlength="30"
            class="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            :class="{ 'border-red-400': errors.position }"
          />
          <p v-if="errors.position" class="text-red-500 text-xs mt-1">
            {{ errors.position }}
          </p>
        </div>
        <h2 class="text-lg font-semibold text-gray-900 mb-4 mt-8">
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
            maxlength="750"
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
            maxlength="750"
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
        <div class="flex gap-4">
          <button
          :key="submitKey"
          @click.once="handleSubmit"
          :disabled="isLoading"
          class="bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 text-white font-medium px-6 py-3 rounded-xl transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isLoading ? "Kreiranje..." : "➕ Kreiraj profil" }}
        </button>
          <button
            @click="$router.push('/role-models')"
            class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-6 py-2 rounded-lg text-sm transition"
          >
            ↩ Otkaži
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { addRoleModel } from "../../services/api.js";
import { uploadRoleModelImage } from "../../services/api";
import { ref } from "vue";
const router = useRouter();

const form = ref({
  first_name: "",
  last_name: "",
  stem_field: "",
  institution: "",
  position: "",
  biography: "",
  achievements: "",
});

const errors = ref({});
const serverError = ref("");
const successMessage = ref("");
const isLoading = ref(false);
const selectedImage = ref(null);
const imagePreview = ref(null);
const submitKey = ref(0)

function handleImageChange(event) {
  const file = event.target.files[0];

  if (!file) return;

  selectedImage.value = file;
  imagePreview.value = URL.createObjectURL(file);
}

function validate() {
  const e = {};
  
  if (!form.value.first_name.trim()) {
    e.first_name = "Ime je obavezno";
  } else if (form.value.first_name.trim().length < 2) {
    e.first_name = "Ime mora imati najmanje 2 karaktera";
  } else if (!/^[\p{L}\s-]+$/u.test(form.value.first_name.trim())) {
    e.first_name = "Ime smije sadržavati samo slova, razmake i crtice";
  }

  if (!form.value.last_name.trim()) {
    e.last_name = "Prezime je obavezno";
  } else if (form.value.last_name.trim().length < 2) {
    e.last_name = "Prezime mora imati najmanje 2 karaktera";
  } else if (!/^[\p{L}\s-]+$/u.test(form.value.last_name.trim())) {
    e.last_name = "Prezime smije sadržavati samo slova, razmake i crtice";
  }

  if (!form.value.stem_field.trim()) {
    e.stem_field = "STEM oblast je obavezna";
  } else if (form.value.stem_field.trim().length < 3) {
    e.stem_field = "STEM oblast mora imati najmanje 3 karaktera";
  }

  if (!form.value.institution.trim()) {
    e.institution = "Institucija je obavezna";
  } else if (form.value.institution.trim().length < 3) {
    e.institution = "Institucija mora imati najmanje 3 karaktera";
  }

  if (!form.value.position.trim()) {
    e.position = "Pozicija/Zvanje je obavezno";
  } else if (form.value.position.trim().length < 2) {
    e.position = "Pozicija mora imati najmanje 2 karaktera";
  }

  if (!form.value.biography.trim()) {
    e.biography = "Biografija je obavezna";
  } else if (form.value.biography.trim().length < 20) {
    e.biography = "Biografija mora imati najmanje 20 karaktera";
  }

  if (!form.value.achievements.trim()) {
    e.achievements = "Postignuća su obavezna";
  } else if (form.value.achievements.trim().length < 10) {
    e.achievements = "Postignuća moraju imati najmanje 10 karaktera";
  } else if (form.value.achievements.trim().split("\n").filter(a => a.trim()).length < 1) {
    e.achievements = "Unesite najmanje jedno postignuće";
  }

  errors.value = e;
  return Object.keys(e).length === 0;
}

async function handleSubmit() {
  if (isLoading.value) return
  isLoading.value = true
  serverError.value = "";
  successMessage.value = "";

  if (!validate()) {
  isLoading.value = false;
  submitKey.value++
  return;
}
  try {
    const token = localStorage.getItem("token");
    if (selectedImage.value) {
      const formData = new FormData();
      formData.append("file", selectedImage.value);
      const uploadResponse = await uploadRoleModelImage(formData);
      form.value.image_url = uploadResponse.image_url;
    }
    const result = await addRoleModel(form.value, token);
    if (result.id) {
      successMessage.value = "Profil je uspješno dodan u direktorij!";
      setTimeout(() => router.push("/role-models"), 1500);
    } else {
      serverError.value = result.detail || "Došlo je do greške. Pokušajte ponovo.";
    }
  } catch (err) {
    serverError.value = "Greška pri komunikaciji sa serverom.";
  } finally {
    isLoading.value = false;
  }
}
</script>
