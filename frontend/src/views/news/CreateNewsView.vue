<template>

  <div class="max-w-2xl mx-auto p-8">

    <h1 class="text-2xl font-bold mb-6">
      Kreiranje blog objave
    </h1>

    <!-- Error -->
    <div
      v-if="serverError"
      class="bg-red-100 text-red-700 p-3 rounded mb-4"
    >
      {{ serverError }}
    </div>

    <!-- Success -->
    <div
      v-if="successMessage"
      class="bg-green-100 text-green-700 p-3 rounded mb-4"
    >
      {{ successMessage }}
    </div>

    <!-- Naslov -->
    <div class="mb-4">

      <label class="block mb-2 font-medium">
        Naslov<span class="text-red-500">*</span>
      </label>

      <input
         v-model="form.title"
         type="text"
         class="w-full border rounded p-2 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
        :class="{ 'border-red-500': errors.title }"
   
      />

      <p
        v-if="errors.title"
        class="text-red-500 text-sm mt-1"
      >
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
        rows="6"
        class="w-full border rounded p-2 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
        :class="{ 'border-red-500': errors.content }"
      ></textarea>

      <p
        v-if="errors.content"
        class="text-red-500 text-sm mt-1"
      >
        {{ errors.content }}
      </p>

    </div>

    <!-- Slika -->
    <div class="mb-6">

      <label class="block mb-2 font-medium">
        URL slike
      </label>

      <input
        v-model="form.image_url"
        type="text"
        class="w-full border rounded p-2 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
      />

    </div>
<div class="mb-6">
  <label class="block mb-2 font-medium">
    Povezani profili
  </label>

  <Multiselect
    v-model="form.role_model_ids"
    mode="tags"
    :options="profileOptions"
    valueProp="id"
    label="full_name"
    trackBy="full_name"
    :searchable="true"
    placeholder="Pretraži i odaberi profile"
  />
</div>

<div class="mb-6">
  <label class="block mb-2 font-medium">Kategorije</label>
  <div class="flex flex-wrap gap-2">
    <button
      v-for="category in categories"
      :key="category.id"
      @click="toggleCategory(category.id)"
      :class="form.category_ids.includes(category.id) ? 'bg-violet-600 text-white' : 'bg-gray-100 text-gray-700'"
      class="px-3 py-1 rounded-full text-sm font-medium transition"
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

</template>

<script setup>

import { onMounted, ref } from 'vue'

import { useRouter } from 'vue-router'

import { createNewsPost,getRoleModels, getCategories } from '../../services/api.js'
import Multiselect from '@vueform/multiselect'

import '@vueform/multiselect/themes/default.css'

const form = ref({
  title: '',
  content: '',
  image_url: '',
  role_model_ids: [],
  category_ids: []
})

const errors = ref({})

const successMessage = ref('')

const serverError = ref('')

const router = useRouter()

const roleModels=ref([])

const categories = ref([])

import { computed } from 'vue'

const profileOptions = computed(() =>
  roleModels.value.map(model => ({
    id: model.id,
    full_name: `${model.first_name} ${model.last_name}`
  }))
)
onMounted(async() => {
  roleModels.value=await getRoleModels()
  const cats = await getCategories()
  categories.value = Array.isArray(cats) ? cats : []
})

function validate() {

  const e = {}

  if (!form.value.title.trim()) {
    e.title = 'Naslov je obavezan'
  }

  if (!form.value.content.trim()) {
    e.content = 'Sadržaj je obavezan'
  }

  errors.value = e

  return Object.keys(e).length === 0
}

function toggleCategory(id) {
  if (form.value.category_ids.includes(id)) {
    form.value.category_ids = form.value.category_ids.filter(c => c !== id)
  } else {
    form.value.category_ids.push(id)
  }
}


async function handleSubmit() {

  serverError.value = ''

  successMessage.value = ''

  if (!validate()) return

  try {

    const token = localStorage.getItem('token')

    const result = await createNewsPost(
      form.value,
      token
    )
  if (result.id) {

   successMessage.value =
    'Objava uspješno kreirana'

   setTimeout(() => {
    router.push('/news')
  }, 2000)

} else {

  serverError.value =
    result.detail || 'Greška pri kreiranju objave'

}

  } catch {

    serverError.value =
      'Greška pri komunikaciji sa serverom'

  }

}

</script>