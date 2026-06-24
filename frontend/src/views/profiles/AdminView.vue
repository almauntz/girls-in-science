<template>
  <div class="p-8 bg-gray-50 min-h-screen">

    <div class="max-w-5xl mx-auto bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      
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
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Akcije
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
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <button 
                  @click="openResetPasswordModal(user)"
                  class="flex items-center space-x-1 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-1.5 px-3 rounded-md transition-colors"
                >
                  <span>🔑</span>
                  <span>Resetuj lozinku</span>
                </button>
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

  <div v-if="isResetModalOpen" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
    <div class="relative p-6 border w-96 shadow-xl rounded-lg bg-white">
      <div class="mt-1">
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-violet-100 text-violet-600 mb-4 text-xl">
          🔑
        </div>
        <h3 class="text-lg font-bold text-gray-900 text-center">
          Resetovanje lozinke
        </h3>
        <div class="mt-2 text-center">
          <p class="text-sm text-gray-500">
            Unesite novu lozinku za korisnicu: <br>
            <span class="font-semibold text-gray-800">{{ selectedUserForReset?.full_name }}</span>
          </p>
        </div>
        
        <form @submit.prevent="confirmResetPassword" class="mt-4">
          <div class="mb-4">
            <label class="block text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1">Nova lozinka</label>
            <input 
              v-model="newPassword"
              type="password"
              placeholder="Unesite minimalno 6 karaktera"
              required
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
            />
          </div>

          <div class="flex items-center space-x-3 pt-2">
            <button 
              type="button"
              @click="closeResetPasswordModal" 
              :disabled="isResetLoading"
              class="px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md w-full hover:bg-gray-200 transition-colors disabled:opacity-50"
            >
              Odustani
            </button>
            <button 
              type="submit"
              :disabled="isResetLoading"
              class="px-4 py-2 bg-violet-600 text-white text-sm font-medium rounded-md w-full hover:bg-violet-700 transition-colors shadow-sm disabled:opacity-50"
            >
              {{ isResetLoading ? 'Spremanje...' : 'Potvrdi' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import StatusToggle from '../../components/StatusToggle.vue'
// DODANA FUNKCIJA `resetUserPassword` U IMPORT
import { updateUserStatus, getAllUsers, updateUserRole, resetUserPassword } from '../../services/api.js'

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
      
      // Stanja za postojeci modal
      isModalOpen: false,
      pendingAction: {
        type: null,    // 'role' ili 'status'
        userId: null,
        newValue: null
      },

      // NOVI PODACI ZA RESET MODAL
      isResetModalOpen: false,
      selectedUserForReset: null,
      newPassword: '',
      isResetLoading: false
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
    
        if (err.message === 'DEAKTIVIRAN_NALOG') {
          alert("Vaš nalog je deaktiviran! Pristup odbijen.");
          localStorage.removeItem('token');
          this.$router.push('/login');
        }
      } finally {
        this.isLoading = false;
      }
    },
    
    handleStatusChange(userId, newStatus) {
      this.pendingAction = { type: 'status', userId, newValue: newStatus };
      this.isModalOpen = true;
    },

    onRoleChange(userId, newRole) {
      this.pendingAction = { type: 'role', userId, newValue: newRole };
      this.isModalOpen = true;
    },

    async confirmAction() {
      this.isModalOpen = false;
      const { type, userId, newValue } = this.pendingAction;
      const token = localStorage.getItem('token');
      
      try {
        if (type === 'role') {
          console.log(`Šaljem izmjenu uloge: korisnica ${userId} -> ${newValue}`);
          await updateUserRole(token, userId, newValue);
        } else if (type === 'status') {
          console.log(`Šaljem izmjenu statusa: korisnica ${userId} -> ${newValue}`);
          await updateUserStatus(token, userId, newValue);
        }
      } catch (error) {
        console.error(`Greška pri promjeni ${type}:`, error);
        alert("Greška sa servera: " + error.message);
      } finally {
        this.pendingAction = { type: null, userId: null, newValue: null };
        await this.loadAllUsers();
      }
    },

    async cancelAction() {
      this.isModalOpen = false;
      this.pendingAction = { type: null, userId: null, newValue: null };
      await this.loadAllUsers();
      console.log("Akcija otkazana.");
    },

    // --- NOVE METODE ZA RESET MODAL ---
    openResetPasswordModal(user) {
      this.selectedUserForReset = user;
      this.newPassword = '';
      this.isResetModalOpen = true;
    },

    closeResetPasswordModal() {
      this.isResetModalOpen = false;
      this.selectedUserForReset = null;
      this.newPassword = '';
    },

    async confirmResetPassword() {
      if (!this.newPassword.trim()) {
        alert("Lozinka ne može biti prazna.");
        return;
      }

      this.isResetLoading = true;
      try {
        // Pozivamo tvoj api servis
        const response = await resetUserPassword(this.selectedUserForReset.id, this.newPassword);
        alert(response.message); // Ispis poruke sa servera
        this.closeResetPasswordModal();
      } catch (error) {
        console.error("Greška pri resetu lozinke:", error);
        alert("Greška: " + error.message);
      } finally {
        this.isResetLoading = false;
        await this.loadAllUsers(); // Osvježi stanje
      }
    }
  }
}
</script>