<template>
  <div class="bg-gray-50 flex h-screen w-full profile-page overflow-hidden">
    
    <ProfileSidebar
      :userRole="userRole" :profileData="profileData"
      :activeTab="activeTab"
      :fullName="profileData.full_name"
      :field="profileData.field"
      :avatarUrl="avatarUrl"
      @tab-change="activeTab = $event"
      @avatar-uploaded="avatarUrl = $event"
      @avatar-deleted="avatarUrl = null"
    />

    <main class="flex-1 p-8 space-y-6 overflow-y-auto h-full">

      <div v-if="isLoading" class="flex justify-center items-center py-20">
        <div class="text-gray-400 text-sm">Učitavanje...</div>
      </div>

      <div v-else>
        <ProfileForm
          v-if="activeTab === 'profil' && userRole !== 'admin' && profileLoaded"
          :fullName="profileData.full_name"
          :field="profileData.field"
          :biography="profileData.biography"
          :avatarUrl="avatarUrl"
          :userRole="userRole"
          :location="profileData.location"
          :email="profileData.email"
          :showBiography="profileData.show_biography"
          :showField="profileData.show_field"
          :showLocation="profileData.show_location"
          :languages="profileData.languages"
          :experience="profileData.experience"
          :education="profileData.education"
          :skills="profileData.skills"
          :linkedinUrl="profileData.linkedin_url"
          :githubUrl="profileData.github_url"
          :twitterUrl="profileData.twitter_url"
          @profile-updated="handleProfileUpdated"
          @avatar-uploaded="avatarUrl = $event"
          @avatar-deleted="avatarUrl = null"
          @account-deactivated="handleDeactivated"
        />
        
        <DashboardTab
          v-if="activeTab === 'dashboard'"
          :userRole="userRole"
          :myWorkshops="myWorkshops"
          :newWorkshops="newWorkshops"
          :availableWorkshops="availableWorkshops"
          :dashboardError="dashboardError"
          :myStudents="myStudents"
          :mentorRequests="mentorRequests"
          :mentorDashboardError="mentorDashboardError"
          @register="handleRegister"
          @accept-request="handleAcceptRequest"
          @reject-request="handleRejectRequest"
        />
        
      <AdminView v-if="activeTab === 'admin_panel' && userRole === 'admin'" />

      <ActivityHistory v-if="activeTab === 'aktivnosti' && userRole !== 'admin'" />
      </div>

    </main>
  </div>
</template>

<script>
import axios from 'axios'
import ProfileSidebar from '../../components/ProfileSidebar.vue'
import ProfileForm from '../../components/ProfileForm.vue'
import DashboardTab from '../../components/DashboardTab.vue'
import ActivityHistory from '../../components/ActivityHistory.vue'
import AdminView from './AdminView.vue'
import { getMyProfile } from '../../services/api.js'

export default {
  name: 'ProfilesView',

  components: {
    ProfileSidebar,
    ProfileForm,
    DashboardTab,
    ActivityHistory,
    AdminView
  },

  data() {
    return {
      activeTab: 'dashboard',
      avatarUrl: null,
      profileData: { full_name: '', field: '' , biography: ''},
      userRole: 'member',
      myWorkshops: [],
      newWorkshops: [],
      availableWorkshops: [],
      dashboardError: null,
      isLoading: false,
      profileLoaded: false,
      myStudents: [],
      mentorRequests: [],
      mentorDashboardError: null,
    }
  },

  async mounted() {
    this.isLoading = true
    await this.loadProfile()

    if (this.userRole !== 'admin') {
        await this.fetchDashboardData()
        await this.fetchMentorData() 
    }
    this.isLoading = false
},

  methods: {

    async loadProfile() {
    try {
      const token = localStorage.getItem('token')
      const data = await getMyProfile(token)
      this.profileData = {
        full_name: data.full_name || '',
        field: data.field || '',
        biography: data.biography || '',
        location: data.location || '',
        email: data.email || '',
        show_biography: data.show_biography ?? true,
        show_field: data.show_field ?? true,
        show_location: data.show_location ?? true,
        languages:    data.languages   || [],
        experience:   data.experience  || [],
        education:    data.education   || [],
        skills:       data.skills      || [],
        linkedin_url: data.linkedin_url || '',
        github_url:   data.github_url   || '',
        twitter_url:  data.twitter_url  || '',
      }

      if (data.role) {
        this.userRole = data.role.toLowerCase()
      }

      if (data.avatar) {
        this.avatarUrl = `http://localhost:8000${data.avatar}`
      }
      this.profileLoaded = true
    } catch (error) {
      console.error('Greška pri učitavanju profila.')
    }
  },
      handleProfileUpdated(data) {
      this.profileData.full_name = data.full_name
      this.profileData.field = data.field
      this.profileData.biography = data.biography
      this.profileData.location = data.location
      this.profileData.email = data.email
      this.profileData.show_biography = data.show_biography
      this.profileData.show_field = data.show_field
      this.profileData.show_location = data.show_location
      this.profileData.languages    = data.languages   || []
      this.profileData.experience   = data.experience  || []
      this.profileData.education    = data.education   || []
      this.profileData.skills       = data.skills      || []
      this.profileData.linkedin_url = data.linkedin_url || ''
      this.profileData.github_url   = data.github_url   || ''
      this.profileData.twitter_url  = data.twitter_url  || ''
    },
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
      } catch (error) {
        console.error('Dashboard greška:', error)
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
        console.log(response.data.message || 'Uspješno ste se prijavili!')
        this.fetchDashboardData()
      } catch (err) {
        this.dashboardError = err.response?.data?.detail || 'Greška pri prijavi na radionicu.'
      }
    },
    
    handleDeactivated() {
    localStorage.removeItem('token')
    this.$router.push('/login')
},
async fetchMentorData() {
  if (this.userRole !== 'mentor') return
  this.mentorDashboardError = null
  try {
    const response = await axios.get(
      'http://localhost:8000/mentoring/my-applications',
      this.getAuthHeaders()
    )
    this.myStudents = response.data.filter(r => r.status?.toUpperCase() === 'ACCEPTED')
    this.mentorRequests = response.data.filter(r => r.status?.toUpperCase() === 'PENDING')
  } catch (error) {
    if (error.response?.status === 404) {
      this.myStudents = []
      this.mentorRequests = []
    } else {
      console.error('Mentor dashboard greška:', error)
      this.mentorDashboardError = 'Nije moguće učitati podatke o mentorstvu.'
    }
  }
},
async handleAcceptRequest(applicationId) {
  try {
    await axios.put(
      `http://localhost:8000/mentoring/applications/${applicationId}/status`,
      { status: 'ACCEPTED' },
      this.getAuthHeaders()
    )
    this.fetchMentorData()
  } catch (err) {
    this.mentorDashboardError = err.response?.data?.detail || 'Greška pri ažuriranju zahtjeva.'
  }
},

async handleRejectRequest(applicationId) {
  try {
    await axios.put(
      `http://localhost:8000/mentoring/applications/${applicationId}/status`,
      { status: 'REJECTED' },
      this.getAuthHeaders()
    )
    this.fetchMentorData()
  } catch (err) {
    this.mentorDashboardError = err.response?.data?.detail || 'Greška pri ažuriranju zahtjeva.'
  }
},
  }
}
</script>

