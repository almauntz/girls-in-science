<template>
  <div class="min-h-screen bg-gray-50 flex">

    <ProfileSidebar
      :activeTab="activeTab"
      :fullName="profileData.full_name"
      :field="profileData.field"
      :avatarUrl="avatarUrl"
      @tab-change="activeTab = $event"
      @avatar-uploaded="avatarUrl = $event"
    />

    <main class="flex-1 p-8 overflow-y-auto">

      <div v-if="isLoading" class="flex justify-center items-center py-20">
        <div class="text-gray-400 text-sm">Učitavanje...</div>
      </div>

      <div v-else>
        <ProfileForm
          v-if="activeTab === 'profil'"
          @profile-updated="profileData = $event"
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
import axios from 'axios'
import ProfileSidebar from '../../components/ProfileSidebar.vue'
import ProfileForm from '../../components/ProfileForm.vue'
import DashboardTab from '../../components/DashboardTab.vue'
import AktivnostiTab from '../../components/AktivnostiTab.vue'

export default {
  name: 'ProfilesView',

  components: {
    ProfileSidebar,
    ProfileForm,
    DashboardTab,
    AktivnostiTab
  },

  data() {
    return {
      activeTab: 'profil',
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
    await this.fetchDashboardData()
    this.isLoading = false
  },

  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('token')
      return { headers: { Authorization: `Bearer ${token}` } }
    },

    async fetchDashboardData() {
      this.dashboardError = null
      try {
        const response = await axios.get(
          'http://localhost:8000/profiles/dashboard',
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
          `http://localhost:8000/profiles/dashboard/register?workshop_id=${workshopId}`,
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

<style scoped>
.profiles-fullwidth {
  margin: -2rem -2rem -2rem -2rem;
  width: calc(100% + 4rem);
}
</style>