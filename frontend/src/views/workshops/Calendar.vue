<template>
  <div class="bg-white rounded-2xl shadow-xl border border-purple-100 overflow-hidden">
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
      
      <div class="flex justify-between items-center mt-4">
        <button @click="updateMonth(-1)" class="text-2xl hover:scale-125 transition-transform">←</button>
        
        <Presence exit-before-enter>
          <Motion 
            :key="currentMonth + '-' + currentYear"
            :initial="{ opacity: 0, y: -10 }"
            :animate="{ opacity: 1, y: 0 }"
            :transition="{ duration: 0.2 }"
            class="text-3xl font-extrabold capitalize"
          >
            {{ currentMonthName }}
          </Motion>
        </Presence>

        <button @click="updateMonth(1)" class="text-2xl hover:scale-125 transition-transform">→</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-px bg-purple-50 border-b border-purple-100">
      <div class="p-3 text-center">
        <p class="text-[10px] text-purple-500 uppercase font-bold tracking-tighter">Ukupno radionica</p>
        <p class="text-xl font-black text-purple-800">{{ stats.totalInMonth }}</p>
      </div>
      <div class="p-3 text-center border-x border-purple-100">
        <p class="text-[10px] text-purple-500 uppercase font-bold tracking-tighter">Slobodnih mjesta</p>
        <p class="text-xl font-black text-green-600">{{ stats.freeSpotsInMonth }}</p>
      </div>
      <div class="p-3 text-center">
        <p class="text-[10px] text-purple-500 uppercase font-bold tracking-tighter">Moje prijave</p>
        <p class="text-xl font-black text-purple-600">{{ stats.registeredCount }}</p>
      </div>
    </div>

    <div class="flex flex-wrap gap-4 p-3 bg-gray-50 border-b text-[9px] uppercase font-bold text-gray-500 justify-center">
      <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-green-500 rounded-full"></span> Slobodno</div>
      <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 bg-red-500 rounded-full"></span> Popunjeno</div>
      <div class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full border-2 border-[#5b21b6]" style="background-color: #7c3aed"></span> Prijava</div>
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
        <div v-for="day in ['Pon', 'Uto', 'Sre', 'Čet', 'Pet', 'Sub', 'Ned']" :key="day" 
             class="py-2 text-center text-[10px] font-bold uppercase text-purple-700 bg-purple-50">
          {{ day }}
        </div>
      </div>

      <Presence :initial="false">
        <Motion
          :key="currentMonth + '-' + currentYear"
          :initial="{ opacity: 0, x: direction * 40 }"
          :animate="{ opacity: 1, x: 0 }"
          :exit="{ opacity: 0, x: direction * -40 }"
          :transition="{ duration: 0.3 }"
          class="grid grid-cols-7 gap-px"
        >
          <div v-for="empty in firstDayOffset" :key="'empty-' + empty" class="bg-gray-50/30 min-h-[120px]"></div>

          <div v-for="n in daysInMonth" :key="n" class="bg-white min-h-[120px] p-2 border-t border-l border-purple-50">
            <span class="text-sm font-semibold mb-1 block transition-all" 
                  :style="isToday(n) ? 'background-color: #7c3aed; color: white; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; border-radius: 50%; shadow: 0 4px 6px rgba(0,0,0,0.1);' : 'color: #9ca3af;'">
              {{ n }}
            </span>
            
            <div class="mt-1 space-y-1">
              <Motion 
                v-for="workshop in filteredWorkshopsForDay(n)" 
                :key="workshop.ID_workshop"
                :initial="{ scale: 0.9, opacity: 0 }"
                :animate="{ scale: 1, opacity: 1 }"
                @click="$router.push(`/workshops/${workshop.ID_workshop}`)"
                :style="getFinalStyle(workshop, n)"
                class="p-2 text-[10px] leading-tight rounded shadow-sm cursor-pointer border-l-[5px] border-solid transition-all relative overflow-hidden"
                :hover="{ scale: 1.04, x: 2 }"
              >
                <div class="flex justify-between items-start">
                  <div class="flex items-center gap-1 min-w-0">
                    <span v-if="isToday(n)" class="relative flex h-1.5 w-1.5 flex-shrink-0">
                      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-current opacity-75"></span>
                      <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-current"></span>
                    </span>
                    <p class="font-bold truncate" :style="{ color: checkIsRegistered(workshop.ID_workshop) ? 'white' : '#1f2937' }">
                      {{ workshop.title }}
                    </p>
                  </div>
                </div>
                <p class="truncate opacity-80 mt-0.5" :style="{ color: checkIsRegistered(workshop.ID_workshop) ? '#e9d5ff' : '#6b7280' }">
                  📍 {{ workshop.location }}
                </p>
              </Motion>
            </div>
          </div>
        </Motion>
      </Presence>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Motion, Presence } from "@motionone/vue"

const props = defineProps({
  workshops: { type: Array, default: () => [] },
  registrations: { type: Object, default: () => ({}) }
})

const searchQuery = ref('')
const displayedDate = ref(new Date())
const direction = ref(1)

const monthNames = ["Januar", "Februar", "Mart", "April", "Maj", "Jun", "Jul", "Avgust", "Septembar", "Oktobar", "Novembar", "Decembar"]

const currentMonth = computed(() => displayedDate.value.getMonth())
const currentYear = computed(() => displayedDate.value.getFullYear())
const currentMonthName = computed(() => monthNames[currentMonth.value])
const daysInMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0).getDate())

const firstDayOffset = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
  return firstDay === 0 ? 6 : firstDay - 1
})

// --- LOGIKA ZA MINI DASHBOARD ---
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

// --- LOGIKA ZA SEARCH FILTRIRANJE ---
const filteredWorkshopsForDay = (n) => {
  return props.workshops.filter(w => {
    const d = new Date(w.date)
    const matchesDay = d.getDate() === n && d.getMonth() === currentMonth.value && d.getFullYear() === currentYear.value
    const matchesSearch = w.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          w.location.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    return matchesDay && matchesSearch
  })
}

const updateMonth = (v) => {
  direction.value = v
  const tempDate = new Date(displayedDate.value)
  tempDate.setMonth(tempDate.getMonth() + v)
  displayedDate.value = tempDate
}

const updateYear = (v) => {
  direction.value = v
  const tempDate = new Date(displayedDate.value)
  tempDate.setFullYear(tempDate.getFullYear() + v)
  displayedDate.value = tempDate
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
  let style = { borderLeftWidth: '5px' }

  if (isPrijavljena) {
    style.backgroundColor = '#7c3aed'; style.borderColor = '#5b21b6'; style.color = 'white'
  } else if (free <= 0) {
    style.backgroundColor = '#fee2e2'; style.borderColor = '#ef4444'; style.color = '#b91c1c'
  } else {
    style.backgroundColor = '#dcfce7'; style.borderColor = '#22c55e'; style.color = '#15803d'
  }

  if (isToday(n)) {
    style.boxShadow = '0 0 10px rgba(124, 58, 237, 0.3)'
  }
  return style
}
</script>