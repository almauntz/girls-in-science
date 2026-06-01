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
         class="w-full border rounded p-2"
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
        class="w-full border rounded p-2"
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
        class="w-full border rounded p-2"
      />

    </div>
  <div class="mb-6">
      <label class="block mb-2 font-medium">
        Povezani profili
      </label>

    <div
        v-for="model in roleModels"
      :key="model.id"
      class="mb-2"
      >
      <label class="flex items-center gap-2">
       <input
        type="checkbox"
        :value="model.id"
        v-model="form.role_model_ids"
      >

       {{ model.first_name }} {{ model.last_name }}
      </label>
    </div>
   </div>

    <!-- Dugme -->
    <button
      @click="handleSubmit"
      class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
    >
      Kreiraj objavu
    </button>

  </div>

</template>

<script setup>

import { onMounted, ref } from 'vue'

import { createNewsPost } from '../../services/api'

import { useRouter } from 'vue-router'

import { getRoleModels } from '../../services/api'

const form = ref({
  title: '',
  content: '',
  image_url: '',
  role_model_ids: []
})

const errors = ref({})

const successMessage = ref('')

const serverError = ref('')

const router = useRouter()

const roleModels=ref([])

onMounted(async() => {
  roleModels.value=await getRoleModels()
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
    successMessage.value='Objava uspjesno kreirana'
    router.push('/news')

    if (result.id) {

      successMessage.value =
        'Objava uspješno kreirana'

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