<template>
  <div class="max-w-3xl mx-auto px-6 py-10">
    <div v-if="loading" class="text-center text-gray-500">Učitavanje...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else-if="roleModel">
      <div class="bg-white rounded-3xl shadow-lg p-8 mb-8">
        <div class="flex items-center justify-between mb-8">
          <router-link
            to="/role-models"
            class="inline-flex items-center gap-2 px-4 py-2 bg-white text-primary rounded-xl shadow-sm hover:shadow-md border border-gray-100 transition"
          >
            ← Nazad na direktorij
          </router-link>

          <div v-if="isAdmin" class="flex gap-3">
            <router-link
              :to="`/role-models/${roleModel.id}/edit`"
              class="bg-primary hover:bg-secondary text-white px-5 py-2 rounded-xl font-medium transition"
            >
              Uredi
            </router-link>
            <button
              @click="handleDelete"
              class="bg-red-600 hover:bg-red-700 text-white font-medium px-5 py-2 rounded-xl transition"
            >
              Obriši
            </button>
          </div>

          <button
            v-if="isLoggedIn && !isAdmin"
            @click="toggleBookmark"
            class="flex items-center gap-2 px-4 py-2 rounded-xl border hover:shadow-lg transition disabled:opacity-50"
            :class="
              isBookmarked
                ? 'bg-primary text-white border-violet-600'
                : 'bg-white text-secondary border-violet-600'
            "
          >
            {{ isBookmarked ? "♥ Ukloni iz favorita" : "♡ Dodaj u favorite" }}
          </button>
        </div>

        <div class="flex items-center gap-8 mb-8">
          <img
            v-if="roleModel.image_url"
            :src="`http://localhost:8000${roleModel.image_url}`"
            class="w-24 h-24 rounded-full object-cover"
          />
          <div
            v-else
            class="w-24 h-24 rounded-full bg-primary text-white flex items-center justify-center text-2xl font-bold"
          >
            {{ getInitials(roleModel.first_name, roleModel.last_name) }}
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ roleModel.first_name }} {{ roleModel.last_name }}
            </h1>
            <p class="text-primary font-medium mt-2">
              {{ roleModel.stem_field }}
            </p>
            <p class="text-500 mt-2">{{ roleModel.institution }}</p>
            <p class="text-500 mt-2">{{ roleModel.position }}</p>
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
import Swal from "sweetalert2";
import {
  getRoleModel,
  deleteRoleModel,
  getMe,
  addBookmark,
  removeBookmark,
  getBookmarks,
} from "../../services/api.js";

const route = useRoute();
const router = useRouter();
const roleModel = ref(null);
const loading = ref(true);
const error = ref(null);
const isAdmin = ref(false);
const isLoggedIn = ref(false);
const isBookmarked = ref(false);

const achievements = computed(() => {
  if (!roleModel.value?.achievements) return [];
  return roleModel.value.achievements.split("\n").filter((a) => a.trim());
});

function getInitials(first, last) {
  return `${first?.[0] || ""}${last?.[0] || ""}`.toUpperCase();
}

async function handleDelete() {
  const result = await Swal.fire({
    title: "Obriši profil",
    text: "Da li ste sigurni da želite obrisati ovaj profil?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#7c3aed",
    cancelButtonColor: "#6b7280",
    confirmButtonText: "Obriši",
    cancelButtonText: "Odustani",
  });
  if (!result.isConfirmed) return;
  const token = localStorage.getItem("token");
  const deleteResult = await deleteRoleModel(roleModel.value.id, token);
  if (deleteResult.message) {
    router.push("/role-models");
  }
}

async function toggleBookmark() {
  if (isBookmarked.value) {
    await removeBookmark(roleModel.value.id);
    isBookmarked.value = false;
  } else {
    await addBookmark(roleModel.value.id);
    isBookmarked.value = true;
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem("token");
    if (token) {
      const user = await getMe(token);
      isAdmin.value = user.role === "admin";
      isLoggedIn.value = true;
      const bookmarks = await getBookmarks();
      isBookmarked.value = bookmarks.some(
        (b) => b.id === parseInt(route.params.id),
      );
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
