<script setup>
import { ref, onMounted, computed } from "vue"
import { getRoleModels, getMe } from "../../services/api"
import { useRouter } from "vue-router"

const router = useRouter()
const roleModels = ref([])
const search = ref("")

const isAdmin = ref(false)
onMounted(async () => {
  roleModels.value = await getRoleModels()
  const token = localStorage.getItem('token')
  if (token) {
    const user = await getMe(token)
    isAdmin.value = user.role === 'admin'
  }
})

const filteredRoleModels = computed(() => {
  if (!search.value.trim()) return roleModels.value
  const q = search.value.toLowerCase()
  return roleModels.value.filter(m =>
    `${m.first_name} ${m.last_name}`.toLowerCase().includes(q) ||
    m.stem_field?.toLowerCase().includes(q) ||
    m.institution?.toLowerCase().includes(q)
  )
})

function getInitials(first, last) {
  return `${first?.[0] || ''}${last?.[0] || ''}`.toUpperCase()
}

function resetFilter() {
  search.value = ""
}

</script>

<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-3xl font-bold text-gray-900 mb-1">Direktorij žena u nauci</h1>
    <p class="text-gray-500 mb-6">Pronađite inspirativne uzore iz STEM oblasti</p>

    <div class="flex gap-4 mb-8">
      <input
        v-model="search"
        type="text"
        placeholder="Pretraži po imenu, oblasti ili instituciji"
        class="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
      />

      <button
        v-if="search"
        @click="resetFilter"
        class="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-5 py-2 rounded-lg text-sm transition"
      >
        Reset
      </button>

      <button
        v-if="isAdmin"
        @click="router.push('/role-models/add')"
        class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-5 py-2 rounded-lg text-sm transition"
      >
        Dodaj novi profil
      </button>
    </div>

    <div v-if="filteredRoleModels.length === 0 && search" class="text-center text-gray-500 py-12">
      Nema rezultata.
    </div>

    <div v-else-if="filteredRoleModels.length === 0" class="text-center text-gray-500 py-12">
      Trenutno nema dostupnih profila.
    </div>

    <div class="flex flex-col gap-4">
      <div
        v-for="model in filteredRoleModels"
        :key="model.id"
        @click="router.push(`/role-models/${model.id}`)"
        class="flex items-center gap-4 bg-white border border-gray-200 rounded-xl px-6 py-4 cursor-pointer hover:shadow-md transition"
      >
        <div class="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-lg flex-shrink-0">
          {{ getInitials(model.first_name, model.last_name) }}
        </div>
        <div>
          <p class="font-semibold text-gray-900">{{ model.first_name }} {{ model.last_name }}</p>
          <p class="text-sm text-blue-600">{{ model.stem_field }}</p>
          <p class="text-sm text-gray-500">{{ model.institution }}</p>
        </div>
      </div>
    </div>
  </div>
</template>