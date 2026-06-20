<template>
  <div class="p-8 bg-gray-50 min-h-screen">

    <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      
      <div class="mb-6 border-b border-gray-100 pb-4">
        <h1 class="text-2xl font-bold text-gray-900">Admin Panel</h1>
        <p class="text-sm text-gray-500 mt-1">Upravljanje korisničkim nalozima</p>
      </div>

      <div class="mb-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Pretraži po imenu..."
          class="w-full sm:w-72 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
        />
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
                E-mail
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
            <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ user.full_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ user.email }}
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
  <div v-if="isModalOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <div class="relative p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100 text-yellow-600 mb-4">
            ⚠️
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            {{ pendingAction.type === 'role' ? 'Potvrda promjene uloge' : 'Potvrda promjene statusa' }}
        </h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
            {{ pendingAction.type === 'role' 
              ? 'Jeste li sigurni da želite promijeniti ulogu ovoj korisnici? Ova akcija će odmah stupiti na snagu.' 
              : 'Jeste li sigurni da želite promijeniti status računa (Aktivna/Deaktivirana) ovoj korisnici?' 
            }}            
            </p>
          </div>
          <div class="items-center px-4 py-3 flex justify-center space-x-4">
            <button 
            @click="cancelAction" 
            class="px-4 py-2 bg-gray-100 text-gray-700 text-base font-medium rounded-md w-full shadow-sm hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-300"
          >
            Odustani
          </button>
          <button 
            @click="confirmAction" 
            class="px-4 py-2 bg-blue-600 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Potvrdi
          </button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import StatusToggle from '../../components/StatusToggle.vue'
import { updateUserStatus, getAllUsers, updateUserRole } from '../../services/api.js'

export default {
  name: 'AdminView',
  
  components: {
    StatusToggle
  },

data() {
    return {
      users: [],
      isLoading: false,
      searchQuery: '',
      // Stanja za modal
      isModalOpen: false,
      pendingAction: {
      type: null,    // 'role' ili 'status'
      userId: null,
      newValue: null
    }
    }
  },

  computed: {
    filteredUsers() {
      if (!this.searchQuery.trim()) return this.users
      const q = this.searchQuery.toLowerCase()
      return this.users.filter(u => u.full_name.toLowerCase().includes(q))
    }
  },

  mounted() {
    this.loadAllUsers()
  },

  methods: {
    async loadAllUsers() {
      console.log("LOAD USERS POZVAN");
      this.isLoading = true;
      try {
        const token = localStorage.getItem('token');
        this.users = await getAllUsers(token); 
        console.log("DOBIJENI PODACI:", this.users);     
      } catch (err) {
        console.error('Uhvaćena greška na frontendu:', err.message);
    
        // Ako je api.js ispalio naš alarm za deaktiviran nalog
        if (err.message === 'DEAKTIVIRAN_NALOG') {
          alert("Vaš nalog je deaktiviran! Pristup odbijen.");
          localStorage.removeItem('token'); // Brišemo token iz browsera
          this.$router.push('/login');      // Izbacujemo je na login ekran
        }
      } finally {
        this.isLoading = false;
      }
    },
    
    handleStatusChange(userId, newStatus) {
      this.pendingAction = { type: 'status', userId, newValue: newStatus };
      this.isModalOpen = true;
    },

    // Kada admin promijeni ulogu u DROPDOWN-u
    onRoleChange(userId, newRole) {
      this.pendingAction = { type: 'role', userId, newValue: newRole };
      this.isModalOpen = true;
    },

    // GLAVNA POTVRDA (Kada se klikne na dugme "Potvrdi" u modalu)
    async confirmAction() {
      this.isModalOpen = false;
      const { type, userId, newValue } = this.pendingAction;
      const token = localStorage.getItem('token');
      
      try {
        if (type === 'role') {
          console.log(`Šaljem izmjenu uloge: korisnica ${userId} -> ${newValue}`);
          await updateUserRole(token, userId, newValue);
          //alert("Uloga je uspješno promijenjena!");
        } else if (type === 'status') {
          console.log(`Šaljem izmjenu statusa: korisnica ${userId} -> ${newValue}`);
          await updateUserStatus(token, userId, newValue);
          //alert("Status računa je uspješno promijenjen!");
        }
      } catch (error) {
        console.error(`Greška pri promjeni ${type}:`, error);
        alert("Greška sa servera: " + error.message);
      } finally {
        // Resetujemo akciju i punimo tabelu svježim podacima sa servera
        this.pendingAction = { type: null, userId: null, newValue: null };
        await this.loadAllUsers();
      }
    },

    // OTKAZIVANJE (Kada admin klikne "Odustani")
    async cancelAction() {
      this.isModalOpen = false;
      this.pendingAction = { type: null, userId: null, newValue: null };
      
      // Osvježavamo tabelu kako bi se toggle ili dropdown vratili na stvarno stanje iz baze
      await this.loadAllUsers();
      console.log("Akcija otkazana.");
    }
  }
}
</script>