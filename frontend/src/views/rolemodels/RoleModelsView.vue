<script setup>
import { ref, onMounted, computed } from "vue";
import { getRoleModels, getMe } from "../../services/api";
import { useRouter } from "vue-router";

const router = useRouter();
const roleModels = ref([]);
const search = ref("");

const isAdmin = ref(false);
onMounted(async () => {
  roleModels.value = await getRoleModels();
  const token = localStorage.getItem("token");
  if (token) {
    const user = await getMe(token);
    isAdmin.value = user.role === "admin";
  }
});

const filteredRoleModels = computed(() => {
  if (!search.value.trim()) return roleModels.value;
  const q = search.value.toLowerCase();
  return roleModels.value.filter(
    (m) =>
      `${m.first_name} ${m.last_name}`.toLowerCase().includes(q) ||
      m.stem_field?.toLowerCase().includes(q) ||
      m.institution?.toLowerCase().includes(q),
  );
});

function getInitials(first, last) {
  return `${first?.[0] || ""}${last?.[0] || ""}`.toUpperCase();
}

function resetFilter() {
  search.value = "";
}
</script>

<template>
  <div class="max-w-6xl mx-auto px-6 py-10">
    <div
      class="bg-gradient-to-r from-primary to-secondary rounded-3xl p-10 text-center text-white mb-10 shadow-lg"
    >
      <div class="text-center mb-10">
        <h1 class="text-4xl font-bold text-white mb-3">
          Direktorij žena u nauci
        </h1>

        <p class="text-lg text-white/80 max-w-2xl mx-auto mb-8">
          Pronađite inspirativne uzore iz STEM oblasti i upoznajte njihove
          karijerne puteve.
        </p>
      </div>
      <div class="max-w-2xl mx-auto mb-8 flex gap-3">
        <input
          v-model="search"
          type="text"
          placeholder="Pretraži po imenu, oblasti ili instituciji"
          class="flex-1 border border-gray-300 rounded-xl px-5 py-3 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white"
        />

        <button
          v-if="search"
          @click="resetFilter"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 rounded-xl transition"
        >
          Reset
        </button>
      </div>
    </div>

    <div v-if="isAdmin" class="flex justify-center mb-10">
      <button
        @click="router.push('/role-models/add')"
        class="bg-primary hover:bg-primary/90 text-white font-medium px-6 py-3 rounded-xl transition"
      >
        Dodaj novi profil
      </button>
    </div>

    <div
      v-if="filteredRoleModels.length === 0 && search"
      class="text-center text-gray-500 py-12"
    >
      Nema rezultata.
    </div>

    <div
      v-else-if="filteredRoleModels.length === 0"
      class="text-center text-gray-500 py-12"
    >
      Trenutno nema dostupnih profila.
    </div>

    <div class="grid md:grid-cols-2 gap-6">
      <div
        v-for="model in filteredRoleModels"
        :key="model.id"
        @click="router.push(`/role-models/${model.id}`)"
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
              class="w-14 h-14 rounded-full bg-primary text-white flex items-center justify-center font-bold"
            >
              {{ getInitials(model.first_name, model.last_name) }}
            </div>
          </div>

          <div>
            <p class="font-semibold text-gray-900">
              {{ model.first_name }} {{ model.last_name }}
            </p>

            <p class="text-sm text-primary font-medium">
              {{ model.stem_field }}
            </p>

            <p class="text-sm text-gray-500">
              {{ model.institution }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
