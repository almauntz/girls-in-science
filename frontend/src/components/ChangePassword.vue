<template>
  <div class="max-w-md bg-white p-6 rounded-xl shadow">

    <h2 class="text-2xl font-bold mb-6">
      Promjena Passworda
    </h2>

    <div class="space-y-4">

      <input
        v-model="currentPassword"
        type="password"
        placeholder="Trenutni password"
        class="w-full border rounded-lg p-3"
      />

      <input
        v-model="newPassword"
        type="password"
        placeholder="Novi password"
        class="w-full border rounded-lg p-3"
      />

      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Potvrdi novi password"
        class="w-full border rounded-lg p-3"
      />

      <button
        @click="changePassword"
        :disabled="loading"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg w-full"
      >
        {{ loading ? 'Spremanje...' : 'Promijeni Password' }}
      </button>

      <div
        v-if="message"
        :class="success ? 'text-green-600' : 'text-red-600'"
        class="text-sm font-medium"
      >
        {{ message }}
      </div>

    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ChangePassword',

  data() {
    return {
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      loading: false,
      message: '',
      success: false
    }
  },

  methods: {

    getAuthHeaders() {
      const token = localStorage.getItem('token')

      return {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    },

    async changePassword() {

      this.message = ''
      this.success = false

      if (
        !this.currentPassword ||
        !this.newPassword ||
        !this.confirmPassword
      ) {
        this.message = 'Sva polja su obavezna'
        return
      }

      if (this.newPassword !== this.confirmPassword) {
        this.message = 'Passwordi se ne poklapaju'
        return
      }

      try {

        this.loading = true

        const response = await axios.post(
          'http://localhost:8000/change-password',
          {
            currentPassword: this.currentPassword,
            newPassword: this.newPassword,
            confirmPassword: this.confirmPassword
          },
          this.getAuthHeaders()
        )

        this.success = true
        this.message = response.data.message

        this.currentPassword = ''
        this.newPassword = ''
        this.confirmPassword = ''

      } catch (err) {

        this.message =
          err.response?.data?.detail ||
          err.response?.data?.message ||
          'Greška pri promjeni passworda'

      } finally {

        this.loading = false
      }
    }
  }
}
</script>