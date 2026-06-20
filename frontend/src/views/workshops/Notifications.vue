<template>
  <div class="hidden-notifications"></div>
</template>

<script>
import Swal from 'sweetalert2';

export default {
  name: 'Notifications',
  data() {
    return {
      pollingInterval: null
    };
  },
  methods: {
    async checkNotifications() {
      try {
        const token = localStorage.getItem('token'); 
        if (!token) return;

        const response = await fetch(`${import.meta.env.VITE_API_URL}/workshops/unread-notifications`, {

          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          console.error(`Problem na serveru: ${response.status}`);
          return;
        }

        const data = await response.json();

        if (data && data.length > 0) {
          data.forEach(notif => {
            Swal.fire({
              title: notif.title, 
              html: `<p style="margin: 5px 0 0 0; line-height: 1.4; font-size: 13px;">${notif.body}</p>`,
              icon: 'info',
              iconColor: '#c4b5fd',  
              toast: true,          
              position: 'top-end',  
              showConfirmButton: false, 
              timer: 5000,          
              timerProgressBar: true, 
              background: '#7c3aed',  
              color: '#ffffff',       
              customClass: {
                popup: 'prelijepi-zaobljeni-toast'
              }
            });
          });
        }
      } catch (error) {
        console.error("Greška pri preuzimanju notifikacija preko fetch-a:", error);
      }
    }
  },
  mounted() {
    this.checkNotifications();
    this.pollingInterval = setInterval(this.checkNotifications, 10000);
  },
  beforeUnmount() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }
  }
};
</script>

<style>
.prelijepi-zaobljeni-toast {
  border-radius: 12px !important;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3) !important; 
  padding: 14px 20px !important;
  font-family: sans-serif !important;
}

.prelijepi-zaobljeni-toast .swal2-title {
  color: #ffffff !important;
  font-size: 15px !important;
  font-weight: 600 !important;
}

.prelijepi-zaobljeni-toast .swal2-timer-progress-bar {
  background: #c4b5fd !important;
}

.hidden-notifications {
  display: none;
}
</style>