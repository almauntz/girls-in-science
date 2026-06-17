<template>
  <div class="bg-white rounded-2xl shadow-xl border border-purple-100 overflow-hidden font-sans">
    <div class="p-6 text-white" style="background-color: #7c3aed">
      <div class="flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-3">
          <button @click="updateYear(-1)" class="hover:text-purple-200 transition-colors text-xl">«</button>
          <span class="text-lg font-bold tracking-wider">{{ currentYear }}</span>
          <button @click="updateYear(1)" class="hover:text-purple-200 transition-colors text-xl">»</button>
        </div>

        <div class="relative w-full md:w-64">
          <span class="absolute left-3 top-1/2 -translate-y-1/2 text-purple-300">🔍</span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Pretraži radionice..." 
            class="w-full bg-white/10 border border-white/20 rounded-full py-1.5 pl-9 pr-4 text-sm placeholder:text-purple-200 focus:outline-none focus:bg-white/20 transition-all"
          />
        </div>

        <div class="flex flex-col items-end">
          <p class="text-purple-100 text-[10px] uppercase font-bold italic tracking-widest">Girls in Science</p>
        </div>
      </div>
      
      <div class="flex justify-between items-center mt-4 h-12 relative">
        <button @click="updateMonth(-1)" class="text-2xl hover:scale-125 transition-transform p-2">←</button>
        
        <div class="relative flex-1 flex justify-center overflow-hidden">
          <Transition name="month-fade" mode="out-in">
            <h2 :key="currentMonth + '-' + currentYear" class="text-3xl font-extrabold capitalize">
              {{ currentMonthName }}
            </h2>
          </Transition>
        </div>

        <button 
          @click="goToToday" 
          class="absolute right-10 text-xs font-bold px-3 py-1 rounded-full bg-white/20 hover:bg-white/30 transition-all border border-white/30"
        >
          Danas
        </button>

        <button @click="updateMonth(1)" class="text-2xl hover:scale-125 transition-transform p-2">→</button>
      </div>
    </div>

    <div class="flex justify-center bg-purple-50 border-b border-purple-100">
      <div class="p-3 text-center">
        <p class="text-[10px] text-purple-500 uppercase font-bold tracking-tighter">Moje prijave</p>
        <p class="text-xl font-black text-purple-600">{{ stats.registeredCount }}</p>
      </div>
    </div>

    <Transition name="banner-fade">
      <div v-if="upcomingWarnings.length > 0" class="bg-amber-50 border-b border-amber-200 px-4 py-3">
        <div
          v-for="w in upcomingWarnings"
          :key="w.ID_workshop"
          class="flex items-center gap-3 py-1"
        >
          <span class="relative flex h-3 w-3 shrink-0">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-amber-500"></span>
          </span>
          <p class="text-amber-800 text-xs font-semibold">
            ⚠️ Podsjetnik: Radionica počinje
            <span class="font-black">
              {{ getDaysUntil(w.date) === 0 ? 'danas!' : 'za ' + getDaysUntil(w.date) + ' dan(a)!' }}
            </span>
            — <span class="italic">{{ w.title }}</span>, 📍 {{ w.location }}
          </p>
        </div>
      </div>
    </Transition>

    <div class="flex flex-wrap gap-4 p-3 bg-gray-50 border-b text-[9px] uppercase font-bold text-gray-500 justify-center">
      <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-green-500 rounded-full"></span> Slobodno</div>
      <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-red-500 rounded-full"></span> Popunjeno</div>
      <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full border-2 border-[#5b21b6]" style="background-color: #7c3aed"></span> Prijava</div>
      <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-gray-400 rounded-full"></span> Isteklo</div>
      <div class="flex items-center gap-1 italic opacity-70 border-l pl-3 border-gray-300">
        <span class="relative flex h-2 w-2 mr-1">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
        </span>
        Danas
      </div>
    </div>

    <div class="relative overflow-hidden bg-purple-100">
      <div class="grid grid-cols-7 gap-px border-b border-purple-100 relative z-10">
        <div
          v-for="day in ['Pon', 'Uto', 'Sre', 'Čet', 'Pet', 'Sub', 'Ned']"
          :key="day"
          class="py-2 text-center text-[10px] font-bold uppercase text-purple-700 bg-purple-50"
        >
          {{ day }}
        </div>
      </div>

      <Presence :initial="false">
        <Motion
          :key="currentMonth + '-' + currentYear + '-grid'"
          :initial="{ opacity: 0, x: direction * 40 }"
          :animate="{ opacity: 1, x: 0 }"
          :exit="{ opacity: 0, x: direction * -40 }"
          :transition="{ duration: 0.3 }"
          class="grid grid-cols-7 gap-px"
        >
          <div v-for="empty in firstDayOffset" :key="'empty-' + empty" class="bg-gray-50/30 min-h-[120px]"></div>

          <div v-for="n in daysInMonth" :key="n" class="bg-white min-h-[120px] p-2 border-t border-l border-purple-50">
            <span
              class="text-sm font-semibold mb-1 block transition-all"
              :class="{ 'today-badge': isToday(n) }"
              :style="!isToday(n) ? 'color: #9ca3af;' : ''"
            >
              {{ n }}
            </span>

            <div class="mt-1 space-y-1">
              <Motion
                v-for="workshop in filteredWorkshopsForDay(n)"
                :key="workshop.ID_workshop"
                :style="getFinalStyle(workshop, n)"
                :hover="{ scale: 1.04, x: 2 }"
                class="p-2 text-[10px] leading-tight rounded shadow-sm cursor-pointer border-l-[5px] border-solid transition-all relative"
                @click="handleWorkshopClick(workshop)"
              >
                <span v-if="isFree(workshop)" class="ping-green"></span>
                <span v-else-if="checkIsRegistered(workshop.ID_workshop)" class="ping-purple"></span>

                <div class="flex justify-between items-start">
                  <div class="flex items-center gap-1 min-w-0">
                    <p
                      class="font-bold truncate"
                      :style="{ color: checkIsRegistered(workshop.ID_workshop) ? 'white' : '#1f2937' }"
                    >
                      {{ workshop.title }}
                    </p>
                  </div>
                </div>
                <p
                  class="truncate opacity-80 mt-0.5"
                  :style="{ color: checkIsRegistered(workshop.ID_workshop) ? '#e9d5ff' : '#6b7280' }"
                >
                  📍 {{ workshop.location }}
                </p>
              </Motion>
            </div>
          </div>
        </Motion>
      </Presence>

      <div
        v-if="noWorkshopsInMonth"
        class="flex flex-col items-center justify-center py-16 text-center bg-white"
      >
        <div class="text-5xl mb-4">📭</div>
        <p class="text-purple-400 font-bold text-sm">Nema radionica u ovom mjesecu</p>
        <p class="text-gray-400 text-xs mt-1">Pokušaj pregledati drugi mjesec</p>
      </div>

      <div
        v-if="noSearchResults"
        class="flex flex-col items-center justify-center py-16 text-center bg-white"
      >
        <div class="text-5xl mb-4">🔍</div>
        <p class="text-purple-400 font-bold text-sm">Nema rezultata za "{{ searchQuery }}"</p>
        <p class="text-gray-400 text-xs mt-1">Pokušaj drugi naziv ili lokaciju</p>
      </div>
    </div>

    <Transition name="modal-fade">
      <div v-if="showExpiredModal" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showExpiredModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl p-8 max-w-sm mx-4 text-center">
          <div class="text-5xl mb-4">😔</div>
          <h3 class="text-xl font-black text-gray-800 mb-2">Radionica je istekla</h3>
          <p class="text-gray-500 text-sm mb-6">Izvinjavamo se, ova radionica je već završena i nije više dostupna za prijavu.</p>
          <button 
            @click="showExpiredModal = false"
            class="px-6 py-2 rounded-full text-white font-bold text-sm transition-all hover:opacity-90"
            style="background-color: #7c3aed"
          >
            Zatvori
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Motion, Presence } from "@motionone/vue"

const router = useRouter()

const props = defineProps({
  workshops: { type: Array, default: () => [] },
  registrations: { type: Object, default: () => ({}) }
})

const searchQuery = ref('')
const direction = ref(1)
const showExpiredModal = ref(false)

const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())

const monthNames = ["Januar", "Februar", "Mart", "April", "Maj", "Juni", "Juli", "August", "Septembar", "Oktobar", "Novembar", "Decembar"]

const currentMonthName = computed(() => monthNames[currentMonth.value])

const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate())

const firstDayOffset = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
  return firstDay === 0 ? 6 : firstDay - 1
})

const stats = computed(() => {
  const inMonth = props.workshops.filter(w => {
    const d = new Date(w.date)
    return d.getMonth() === currentMonth.value && d.getFullYear() === currentYear.value
  })
  const registered = Object.values(props.registrations).filter(r => r === true).length
  const freeSpots = inMonth.reduce((acc, curr) => acc + (curr.free_spots || 0), 0)
  return {
    totalInMonth: inMonth.length,
    registeredCount: registered,
    freeSpotsInMonth: freeSpots
  }
})

const getDaysUntil = (date) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const workshopDate = new Date(date)
  workshopDate.setHours(0, 0, 0, 0)
  return Math.ceil((workshopDate - today) / (1000 * 60 * 60 * 24))
}

const upcomingWarnings = computed(() => {
  return props.workshops.filter(w => {
    if (!checkIsRegistered(w.ID_workshop)) return false
    const diff = getDaysUntil(w.date)
    return diff >= 0 && diff <= 3
  })
})

const noWorkshopsInMonth = computed(() => {
  if (searchQuery.value) return false
  return props.workshops.filter(w => {
    const d = new Date(w.date)
    return d.getMonth() === currentMonth.value && d.getFullYear() === currentYear.value
  }).length === 0
})

const noSearchResults = computed(() => {
  if (!searchQuery.value) return false
  return props.workshops.filter(w => {
    const d = new Date(w.date)
    const matchesMonth = d.getMonth() === currentMonth.value && d.getFullYear() === currentYear.value
    const matchesSearch = w.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          w.location.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesMonth && matchesSearch
  }).length === 0
})

const filteredWorkshopsForDay = (n) => {
  return props.workshops.filter(w => {
    const d = new Date(w.date)
    const matchesDay = d.getDate() === n && d.getMonth() === currentMonth.value && d.getFullYear() === currentYear.value
    const matchesSearch = w.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          w.location.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesDay && matchesSearch
  })
}

const isFree = (workshop) => {
  const free = workshop.free_spots ?? (workshop.capacity - (workshop.registered_count || 0))
  return free > 0 && !checkIsRegistered(workshop.ID_workshop)
}

const handleWorkshopClick = (workshop) => {
  const isExpired = new Date(workshop.date) < new Date(new Date().setHours(0, 0, 0, 0))
  if (isExpired) {
    showExpiredModal.value = true
  } else {
    router.push(`/workshops/${workshop.ID_workshop}`)
  }
}

const updateMonth = (v) => {
  direction.value = v
  let newMonth = currentMonth.value + v
  if (newMonth > 11) {
    currentMonth.value = 0
    currentYear.value++
  } else if (newMonth < 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value = newMonth
  }
}

const updateYear = (v) => {
  direction.value = v
  currentYear.value += v
}

const goToToday = () => {
  const today = new Date()
  direction.value = today.getMonth() > currentMonth.value ? 1 : -1
  currentMonth.value = today.getMonth()
  currentYear.value = today.getFullYear()
}

const isToday = (n) => {
  const t = new Date()
  return t.getDate() === n && t.getMonth() === currentMonth.value && t.getFullYear() === currentYear.value
}

const checkIsRegistered = (id) => {
  return props.registrations && (props.registrations[id] === true || props.registrations[String(id)] === true)
}

const getFinalStyle = (workshop, n) => {
  const isPrijavljena = checkIsRegistered(workshop.ID_workshop)
  const free = workshop.free_spots ?? (workshop.capacity - (workshop.registered_count || 0))
  const isExpired = new Date(workshop.date) < new Date(new Date().setHours(0, 0, 0, 0))
  let style = { borderLeftWidth: '5px' }

  if (isExpired) {
    style.backgroundColor = '#f3f4f6'
    style.borderColor = '#9ca3af'
    style.color = '#9ca3af'
  } else if (isPrijavljena) {
    style.backgroundColor = '#7c3aed'
    style.borderColor = '#5b21b6'
    style.color = 'white'
  } else if (free <= 0) {
    style.backgroundColor = '#fee2e2'
    style.borderColor = '#ef4444'
    style.color = '#b91c1c'
  } else {
    style.backgroundColor = '#dcfce7'
    style.borderColor = '#22c55e'
    style.color = '#15803d'
  }

  if (isToday(n)) {
    style.boxShadow = '0 0 10px rgba(124, 58, 237, 0.3)'
  }

  return style
}
</script>

<style scoped>
.month-fade-enter-active,
.month-fade-leave-active {
  transition: all 0.25s ease-out;
}

.month-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.month-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.banner-fade-enter-active,
.banner-fade-leave-active {
  transition: all 0.3s ease;
}

.banner-fade-enter-from,
.banner-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.today-badge {
  background-color: #7c3aed;
  color: white !important;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ping-green,
.ping-purple {
  position: absolute;
  inset: 0;
  border-radius: 4px;
  pointer-events: none;
}

.ping-green {
  animation: pingGreen 1.5s ease-in-out infinite;
}

.ping-purple {
  animation: pingPurple 1.5s ease-in-out infinite;
}

@keyframes pingGreen {
  0%, 100% { box-shadow: inset 0 0 0 0 rgba(34, 197, 94, 0.6); }
  50%       { box-shadow: inset 0 0 0 3px rgba(34, 197, 94, 0); }
}

@keyframes pingPurple {
  0%, 100% { box-shadow: inset 0 0 0 0 rgba(124, 58, 237, 0.6); }
  50%       { box-shadow: inset 0 0 0 3px rgba(124, 58, 237, 0); }
}
</style>