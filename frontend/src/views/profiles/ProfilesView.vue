<template>
  <div>
    <h1>Profili & Dashboard</h1>
    <p>Tim 4 gradi ovdje.</p>
  </div>
</template>

<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-2xl mx-auto">
      
      <h2 class="text-2xl font-bold text-gray-800 mb-6">
        Moj profil
      </h2>

      <div class="bg-white rounded-xl shadow-sm p-6">
        <form @submit.prevent="saveProfile" class="space-y-5">

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Ime i prezime *
            </label>
            <input
              v-model="form.full_name"
              type="text"
              placeholder="Unesite ime i prezime"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 
                     text-sm focus:outline-none focus:ring-2 
                     focus:ring-green-500 focus:border-transparent"
            />
            <p v-if="errors.full_name" 
              class="text-red-500 text-xs mt-1">
              {{ errors.full_name }}
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Oblast
            </label>
            <input
              v-model="form.field"
              type="text"
              placeholder="Npr. Softversko inženjerstvo"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 
                     text-sm focus:outline-none focus:ring-2 
                     focus:ring-green-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Biografija
            </label>
            <textarea
              v-model="form.biography"
              placeholder="Napišite nešto o sebi..."
              rows="4"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 
                     text-sm focus:outline-none focus:ring-2 
                     focus:ring-green-500 focus:border-transparent resize-none"
            ></textarea>
            <div class="flex justify-between mt-1">
                 <p v-if="errors.biography" class="text-red-500 text-xs">
                {{ errors.biography }}
                </p>
               <span class="text-xs text-gray-400 ml-auto">
                {{ form.biography?.length || 0 }}/500
              </span>
            </div>
          </div>

          <div class="pt-2">
            <button
              type="submit"
              :disabled="!isFormValid"
              class="w-full bg-green-600 text-white py-2 px-4 rounded-lg 
                     text-sm font-medium hover:bg-green-700 
                     transition-colors duration-200"
            >
              Spremi promjene
            </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfilesView',

  data() {
    return {
      form: {
        full_name: '',
        biography: '',
        field: ''
      },
      errors: { 
        full_name: '',
       biography: '' }
      
    }
  },
    computed: {
    isFormValid() {
      return (
        this.form.full_name.trim() !== '' &&
        (this.form.biography?.length || 0) <= 500
      )
    }
  },


  methods: {
    validateForm() {
    this.errors = { full_name: '', biography: '' }
    let isValid = true

    if (!this.form.full_name || this.form.full_name.trim() === '') {
      this.errors.full_name = 'Ime ne smije biti prazno.'
      isValid = false
    }

    if (this.form.biography && this.form.biography.length > 500) {
      this.errors.biography = 'Biografija ne smije biti duža od 500 karaktera.'
      isValid = false
    }

    return isValid
  },
    saveProfile() {
      
    }
  }
}
</script>