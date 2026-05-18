<template>
<div class="bg-gray-50 flex gap-8 items-stretch p-8">
    <ProfileSidebar
      :activeTab="activeTab"
      :fullName="profileData.full_name"
      :field="profileData.field"
      :avatarUrl="avatarUrl"
      @tab-change="activeTab = $event"
      @avatar-uploaded="avatarUrl = $event"
      @avatar-deleted="avatarUrl = null"
    />

    <main class="flex-1 overflow-y-auto h-full">

      <div v-if="isLoading" class="flex justify-center items-center py-20">
        <div class="text-gray-400 text-sm">Učitavanje...</div>
      </div>

      <div v-else>
      <ProfileForm
        v-if="activeTab === 'profil'"
        :fullName="profileData.full_name"
        :field="profileData.field"
        :avatarUrl="avatarUrl"
        @profile-updated="profileData = $event"
        @avatar-uploaded="avatarUrl = $event"
        @avatar-deleted="avatarUrl = null"
      />
        <DashboardTab
          v-if="activeTab === 'dashboard'"
          :myWorkshops="myWorkshops"
          :newWorkshops="newWorkshops"
          :availableWorkshops="availableWorkshops"
          :dashboardError="dashboardError"
          @register="handleRegister"
        />
        <AktivnostiTab v-if="activeTab === 'aktivnosti'" />
      </div>

    </main>
  </div>
</template>

<script>
// import axios from 'axios'
import ProfileSidebar from '../../components/ProfileSidebar.vue'
import ProfileForm from '../../components/ProfileForm.vue'
import DashboardTab from '../../components/DashboardTab.vue'
// import AktivnostiTab from '../../components/AktivnostiTab.vue'
import { getMyProfile } from '../../services/api.js'

export default {
  name: 'ProfilesView',

  components: {
    ProfileSidebar,
    ProfileForm,
    DashboardTab
    // AktivnostiTab
  },

  data() {
    return {
      activeTab: 'dashboard',
      avatarUrl: null,
      profileData: { full_name: '', field: '' },
      myWorkshops: [],
      newWorkshops: [],
      availableWorkshops: [],
      dashboardError: null,
      isLoading: false
    }
  },

  async mounted() {
  this.isLoading = true
  await this.loadProfile()
  await this.fetchDashboardData()
  this.isLoading = false
},

  methods: {

    async loadProfile() {
    try {
      const token = localStorage.getItem('token')
      const data = await getMyProfile(token)
      this.profileData = {
        full_name: data.full_name || '',
        field: data.field || ''
      }
      if (data.avatar) {
        this.avatarUrl = `http://localhost:8000${data.avatar}`
      }
    } catch (error) {
      console.error('Greška pri učitavanju profila.')
    }
  },
    getAuthHeaders() {
      const token = localStorage.getItem('token')
      return { headers: { Authorization: `Bearer ${token}` } }
    },

    async fetchDashboardData() {
      this.dashboardError = null
      try {
        const response = await axios.get(
          'http://localhost:8000/dashboard',
          this.getAuthHeaders()
        )
        this.myWorkshops = response.data.my_workshops
        this.newWorkshops = response.data.new_workshops
        this.availableWorkshops = response.data.available_workshops
      } catch (err) {
        this.dashboardError = 'Nije moguće učitati podatke. Provjerite jeste li prijavljeni.'
      }
    },

    async handleRegister(workshopId) {
      try {
        const response = await axios.post(
          `http://localhost:8000/dashboard/register?workshop_id=${workshopId}`,
          {},
          this.getAuthHeaders()
        )
        alert(response.data.message || 'Uspješno ste se prijavili!')
        this.fetchDashboardData()
      } catch (err) {
        alert(err.response?.data?.detail || 'Greška pri prijavi.')
      }
    }
  }
}
</script>

