<template>
  <div>
    <!-- HEADER KARTICA -->
    <div class="bg-violet-600 rounded-xl p-6 mb-6 flex items-center gap-5 max-w-full relative">
      <div class="relative cursor-pointer group flex-shrink-0" @click="$refs.fileInput.click()">
        <div class="w-20 h-20 rounded-full bg-violet-400 flex items-center justify-center overflow-hidden">
          <img v-if="avatarUrl" :src="avatarUrl" alt="Avatar" class="w-full h-full object-cover" />
          <span v-else class="text-4xl">👤</span>
        </div>
        <div class="absolute inset-0 rounded-full bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center">
          <span class="text-white text-xl opacity-0 group-hover:opacity-100">📷</span>
        </div>
        <div v-if="isUploading" class="absolute inset-0 rounded-full bg-black bg-opacity-40 flex items-center justify-center">
          <span class="text-white text-xs">...</span>
        </div>
        <button
          v-if="avatarUrl"
          type="button"
          @click.stop="handleDeleteAvatar"
          class="absolute -top-1 -right-1 w-6 h-6 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center text-xs transition-colors"
        >
          ✕
        </button>
      </div>

      <input ref="fileInput" type="file" accept=".jpg,.jpeg,.png" class="hidden" @change="handleAvatarChange" />

      <div>
        <h2 class="text-2xl font-bold text-white">{{ fullName || 'Korisnice' }}</h2>
        <p class="text-violet-200 text-sm mt-1">{{ field || 'Oblast nije unesena' }}</p>
        <p v-if="avatarError" class="text-red-200 text-xs mt-2">{{ avatarError }}</p>
      </div>

          <!-- UREDI DUGME U HEADERU -->
          <button
           v-if="!isEditMode && activeTab === 'info'"
            type="button"
           @click="isEditMode = true"
          class="absolute bottom-4 right-4 text-sm text-violet-600 bg-white hover:bg-violet-50 font-medium px-4 py-2 rounded-lg transition-colors"
        >
         ✏️ Uredi
        </button>
 
    </div>

    <!-- TABOVI -->
    <div class="flex border-b border-gray-200 mb-6">
      <button
        @click="activeTab = 'info'"
        :class="[
          'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
          activeTab === 'info'
            ? 'border-violet-600 text-violet-600'
            : 'border-transparent text-gray-500 hover:text-gray-700'
        ]"
      >
        Lični podaci
      </button>
      <button
        @click="activeTab = 'security'"
        :class="[
          'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
          activeTab === 'security'
            ? 'border-violet-600 text-violet-600'
            : 'border-transparent text-gray-500 hover:text-gray-700'
        ]"
      >
        Sigurnost
      </button>
    </div>

    <!-- LIČNI PODACI TAB -->
    <div v-if="activeTab === 'info'">
      <div class="bg-white rounded-xl shadow-sm p-6 max-w-full min-h-96">

        <div v-if="successMessage" class="bg-green-50 text-green-700 border border-green-200 rounded-lg px-4 py-3 mb-4 text-sm">
          {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 mb-4 text-sm">
          {{ errorMessage }}
        </div>


        <form @submit.prevent="saveProfile" class="space-y-5">

          <!-- IME I PREZIME -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Ime i prezime</label>
            <p v-if="!isEditMode" class="text-sm text-gray-800 px-3 py-2 bg-gray-50 rounded-lg">
              {{ form.full_name || 'Nije uneseno' }}
            </p>
            <input
              v-else
              v-model="form.full_name"
              type="text"
              placeholder="Unesite ime i prezime (obavezno polje)"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
            />
            <p v-if="errors.full_name" class="text-red-500 text-xs mt-1">{{ errors.full_name }}</p>
          </div>

          <!-- OBLAST -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Oblast</label>
            <p v-if="!isEditMode" class="text-sm text-gray-800 px-3 py-2 bg-gray-50 rounded-lg">
              {{ form.field || 'Nije uneseno' }}
            </p>
            <input
              v-else
              v-model="form.field"
              type="text"
              placeholder="Npr. Softversko inženjerstvo"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
            />
          </div>

          <!-- BIOGRAFIJA -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Biografija</label>
            <p v-if="!isEditMode" class="text-sm text-gray-800 px-3 py-2 bg-gray-50 rounded-lg whitespace-pre-wrap">
              {{ form.biography || 'Nije uneseno' }}
            </p>
            <textarea
              v-else
              v-model="form.biography"
              placeholder="Napišite nešto o sebi..."
              rows="8"
              spellcheck="false"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent resize-none"
            ></textarea>
            <div v-if="isEditMode" class="flex justify-between mt-1">
              <p v-if="errors.biography" class="text-red-500 text-xs">{{ errors.biography }}</p>
              <span class="text-xs text-gray-400 ml-auto">{{ form.biography?.length || 0 }}/500</span>
            </div>
          </div>

          <!-- DUGMAD — samo u edit modu -->
          <div v-if="isEditMode" class="flex gap-3 pt-2">
            <button
              type="submit"
              :disabled="!isFormValid"
              class="flex-1 bg-violet-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-violet-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Spremi promjene
            </button>
            <button
              type="button"
              @click="cancelEdit"
              class="flex-1 border border-gray-300 text-gray-600 py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
            >
              Odustani
            </button>
          </div>

        </form>
      </div>
    </div>

    <!-- SIGURNOST TAB -->
    <div v-if="activeTab === 'security'">
      <div class="bg-white rounded-xl shadow-sm p-6 max-w-full min-h-96">
        <div v-if="passwordSuccess" class="bg-green-50 text-green-700 border border-green-200 rounded-lg px-4 py-3 mb-4 text-sm">
          {{ passwordSuccess }}
        </div>
        <div v-if="passwordError" class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 mb-4 text-sm">
          {{ passwordError }}
        </div>

        <form @submit.prevent="changePassword" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Trenutna lozinka</label>
            <input
              v-model="passwordForm.old_password"
              type="password"
              placeholder="••••••••"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nova lozinka</label>
            <input
              v-model="passwordForm.new_password"
              type="password"
              placeholder="••••••••"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Potvrda nove lozinke</label>
            <input
              v-model="passwordForm.confirm_new_password"
              type="password"
              placeholder="••••••••"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
            />
          </div>

          <div class="pt-2">
            <button
              type="submit"
              :disabled="passwordLoading"
              class="w-full bg-violet-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-violet-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ passwordLoading ? 'Spremanje...' : 'Promijeni lozinku' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import { updateProfile } from '../services/api.js'

export default {
  name: 'ProfileForm',

  props: {
    fullName: String,
    field: String,
    biography: String,
    avatarUrl: String
  },

  emits: ['profile-updated', 'avatar-uploaded', 'avatar-deleted'],

  data() {
    return {
      activeTab: 'info',
      isEditMode: false,
      passwordForm: {
        old_password: '',
        new_password: '',
        confirm_new_password: ''
      },
      passwordLoading: false,
      passwordSuccess: '',
      passwordError: '',
      form: {
        full_name: '',
        biography: '',
        field: ''
      },
      errors: {
        full_name: '',
        biography: ''
      },
      successMessage: '',
      errorMessage: '',
      isUploading: false,
      avatarError: ''
    }
  },

  computed: {
    isFormValid() {
      return (
        this.form.full_name && this.form.full_name.trim() !== '' &&
        (this.form.biography?.length || 0) <= 500
      )
    }
  },

watch: {
  fullName: {
    immediate: true,
    handler(val) {
      this.form.full_name = val || ''
    }
  },
  field: {
    immediate: true,
    handler(val) {
      this.form.field = val || ''
    }
  },
  biography: {
    immediate: true,
    handler(val) {
      this.form.biography = val || ''
    }
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

    async saveProfile() {
      if (!this.validateForm()) return
      this.successMessage = ''
      this.errorMessage = ''
      try {
        const token = localStorage.getItem('token')
        await updateProfile(token, {
          full_name: this.form.full_name,
          biography: this.form.biography,
          field: this.form.field
        })
        this.successMessage = 'Promjene su uspješno sačuvane!'
        this.isEditMode = false;
        this.$emit('profile-updated', this.form)
        setTimeout(() => { this.successMessage = '' }, 3000)
      } catch (error) {
        this.errorMessage = 'Greška pri čuvanju. Pokušajte ponovo.'
        setTimeout(() => { this.errorMessage = '' }, 3000)
      }
    },

        cancelEdit() {
      this.isEditMode = false
      // Resetuj formu na originalne vrijednosti
      this.form.full_name = this.fullName || ''
      this.form.field = this.field || ''
      this.form.biography = this.biography || ''
      this.errors = { full_name: '', biography: '' }
    },

    async handleAvatarChange(event) {
      const file = event.target.files[0]
      if (!file) return

      this.isUploading = true
      this.avatarError = ''

      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']
      if (!allowedTypes.includes(file.type)) {
        this.avatarError = 'Neispravan format! Dozvoljeni su samo JPG i PNG.'
        this.isUploading = false
        event.target.value = ''
        return
      }

      const maxSizeInBytes = 2 * 1024 * 1024
      if (file.size > maxSizeInBytes) {
        this.avatarError = 'Slika je prevelika! Maksimalna veličina je 2MB.'
        this.isUploading = false
        event.target.value = ''
        return
      }

      try {
        const token = localStorage.getItem('token')
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('http://localhost:8000/profiles/me/avatar', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail)
        }

        const data = await response.json()
        this.$emit('avatar-uploaded', `http://localhost:8000${data.avatar_url}`)

      } catch (error) {
        this.avatarError = error.message || 'Greška pri uploadu slike.'
      } finally {
        this.isUploading = false
        event.target.value = ''
      }
    },

    async changePassword() {
      this.passwordSuccess = ''
      this.passwordError = ''

      if (!this.passwordForm.old_password || !this.passwordForm.new_password || !this.passwordForm.confirm_new_password) {
        this.passwordError = 'Sva polja su obavezna.'
        return
      }

      if (this.passwordForm.new_password !== this.passwordForm.confirm_new_password) {
        this.passwordError = 'Nova lozinka i potvrda se ne poklapaju.'
        return
      }

      if (this.passwordForm.new_password.length < 8) {
        this.passwordError = 'Nova lozinka mora imati najmanje 8 karaktera.'
        return
      }

      try {
        this.passwordLoading = true
        const token = localStorage.getItem('token')

        const response = await fetch('http://localhost:8000/profiles/me/change-password', {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.passwordForm)
        })

        const data = await response.json()

        if (response.ok) {
          this.passwordSuccess = data.message || 'Lozinka uspješno promijenjena.'
          this.passwordForm = { old_password: '', new_password: '', confirm_new_password: '' }
          setTimeout(() => { this.passwordSuccess = '' }, 3000)
        } else {
          this.passwordError = data.detail || 'Greška pri promjeni lozinke.'
        }
      } catch (e) {
        this.passwordError = 'Backend ne radi.'
      } finally {
        this.passwordLoading = false
      }
    },

    async handleDeleteAvatar() {
      if (!confirm('Jeste li sigurni da želite obrisati profilnu sliku?')) return

      this.avatarError = ''
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/profiles/me/avatar', {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Greška pri brisanju.')
        }

        this.$emit('avatar-deleted')
      } catch (error) {
        this.avatarError = error.message || 'Nije moguće obrisati profilnu sliku.'
      }
    }
  }
}
</script>