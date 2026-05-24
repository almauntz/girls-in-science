<template>
  <div class="p-8 bg-gray-50 min-h-screen">

    <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      
      <div class="mb-6 border-b border-gray-100 pb-4">
        <h1 class="text-2xl font-bold text-gray-900">Admin Panel</h1>
        <p class="text-sm text-gray-500 mt-1">Upravljanje korisničkim nalozima</p>
      </div>

      <div v-if="isLoading" class="flex justify-center items-center py-12">
        <div class="text-primary text-sm font-medium animate-pulse">Učitavanje korisnica...</div>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ime i prezime
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Uloga
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status računa
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ user.full_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <select 
                  :value="user.role" 
                  @change="onRoleChange(user.id, $event.target.value)"
                  class="bg-white border border-gray-300 text-gray-700 text-sm rounded-md focus:ring-blue-500 focus:border-blue-500 block p-1.5 shadow-sm"
                >
                  <option value="member">Studentica</option>
                  <option value="mentor">Mentorica</option>
                  <option value="admin">Admin</option>
                </select>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <StatusToggle 
                  :model-value="!!user.is_active" 
                  @change="handleStatusChange(user.id, !user.is_active)"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script>
import StatusToggle from '../../components/StatusToggle.vue'
import { updateUserStatus, getAllUsers } from '../../services/api.js'

export default {
  name: 'AdminView',
  
  components: {
    StatusToggle
  },

data() {
    return {
      users: [],
      isLoading: false
    }
  },

  mounted() {
    this.loadAllUsers()
  },

  methods: {
    async loadAllUsers() {
      this.isLoading = true;
      try {
        const token = localStorage.getItem('token');
        this.users = await getAllUsers(token); 
      } catch (err) {
        console.error('Greška pri učitavanju korisnica', err);
      } finally {
        this.isLoading = false;
      }
    },
    
    async handleStatusChange(userId, newStatus) {
      try {
        const token = localStorage.getItem('token'); 
        console.log("Šaljem zahtjev za izmjenu statusa sa svježim tokenom...");
        
        await updateUserStatus(token, userId, newStatus);
        
        if (typeof this.loadAllUsers === 'function') {
          await this.loadAllUsers();
        }
      } catch (error) {
        console.error("Detaljna greška na frontendu:", error);
        alert("Greška sa servera: " + error.message);
      }
    },

    // GIS4-73: Testna metoda za klik na ulogu
    async onRoleChange(userId, newRole) {
      console.log(`UI Test (GIS4-73): Korisnica ${userId} prebačena na ulogu: ${newRole}`);
      alert(`Kliknut UI! Nova uloga: ${newRole}`);
    }
  }
}
</script>