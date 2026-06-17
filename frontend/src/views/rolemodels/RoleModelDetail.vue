<template>
  <div class="max-w-3xl mx-auto px-6 py-10">
    <div v-if="loading" class="text-center text-gray-500">Učitavanje...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else-if="roleModel">
      <div class="bg-white rounded-3xl shadow-lg p-8 mb-8">
        <router-link
          to="/role-models"
          class="inline-flex items-center gap-2 px-4 py-2 bg-white text-primary rounded-xl shadow-sm hover:shadow-md border border-gray-100 transition mb-8"
        >
          ← Nazad na direktorij
        </router-link>

        <div class="flex items-start justify-between gap-12">
          <div class="flex items-center gap-8 mb-8">
            <img
              v-if="roleModel.image_url"
              :src="`http://localhost:8000${roleModel.image_url}`"
              class="w-28 h-28 rounded-full object-cover"
            />

            <div
              v-else
              class="w-28 h-28 rounded-full bg-primary text-white flex items-center justify-center text-2xl font-bold"
            >
              {{ getInitials(roleModel.first_name, roleModel.last_name) }}
            </div>
            <div>
              <h1 class="text-4xl font-bold text-gray-900">
                {{ roleModel.first_name }} {{ roleModel.last_name }}
              </h1>
              <p class="text-primary font-medium mt-2">
                {{ roleModel.stem_field }}
              </p>
              <p class="text-gray-500 mt-2">
                {{ roleModel.institution }} • {{ roleModel.position }}
              </p>
            </div>
          </div>

          <div class="flex gap-3 mt-5" v-if="isAdmin">
            <router-link
              :to="`/role-models/${roleModel.id}/edit`"
              class="bg-primary hover:bg-primary/90 text-white px-5 py-2 rounded-xl font-medium transition"
            >
              Uredi
            </router-link>
            <button
              @click="handleDelete"
              class="bg-red-600 hover:bg-red-700 text-white font-medium px-5 py-2 rounded-xl font-medium transition"
            >
              Obriši
            </button>
          </div>
        </div>

        <div
          class="bg-white border border-gray-100 rounded-2xl p-6 hover:shadow-sm transition mt-8"
        >
          <h2 class="text-xl font-bold text-gray-900 mb-4">Biografija</h2>

          <p class="text-gray-700 leading-relaxed whitespace-pre-line">
            {{ roleModel.biography }}
          </p>
        </div>

        <div
          class="bg-white border border-gray-100 rounded-2xl p-6 hover:shadow-sm transition mt-6"
        >
          <h2 class="text-xl font-bold text-gray-900 mb-4">Postignuća</h2>

          <ul class="space-y-2">
            <li
              v-for="(achievement, index) in achievements"
              :key="index"
              class="text-gray-700"
            >
              • {{ achievement }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getRoleModel, deleteRoleModel, getMe } from "../../services/api.js";
import Swal from 'sweetalert2'

const route = useRoute();
const router = useRouter();
const roleModel = ref(null);
const loading = ref(true);
const error = ref(null);
const isAdmin = ref(false);

const achievements = computed(() => {
  if (!roleModel.value?.achievements) return [];
  return roleModel.value.achievements.split("\n").filter((a) => a.trim());
});

function getInitials(first, last) {
  return `${first?.[0] || ""}${last?.[0] || ""}`.toUpperCase();
}

async function handleDelete() {
  const result = await Swal.fire({
    title: 'Obriši profil',
    text: 'Da li ste sigurni da želite obrisati ovaj profil?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#7c3aed',
    cancelButtonColor: '#6b7280',
    confirmButtonText: 'Obriši',
    cancelButtonText: 'Odustani'
  })
  if (!result.isConfirmed) return;
  const token = localStorage.getItem("token");
  const deleteResult = await deleteRoleModel(roleModel.value.id, token);
  if (deleteResult.message) {
    router.push("/role-models");
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem("token");
    if (token) {
      const user = await getMe(token);
      isAdmin.value = user.role === "admin";
    }
    const data = await getRoleModel(route.params.id);
    if (data.detail) {
      error.value = "Profil nije pronađen.";
    } else {
      roleModel.value = data;
    }
  } catch {
    error.value = "Došlo je do greške pri učitavanju profila.";
  } finally {
    loading.value = false;
  }
});
</script>
