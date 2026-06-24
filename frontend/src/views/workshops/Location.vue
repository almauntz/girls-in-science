<template>
  <a
    v-if="location"
    :href="mapsUrl"
    target="_blank"
    rel="noopener noreferrer"
    :class="[
      'inline-flex items-center transition-colors hover:underline',
      gapClass,
      textSizeClass,
      textColorClass,
      hoverColorClass
    ]"
    :title="`Otvori '${location}' na Google Maps`"
    @click.stop
  >
    <svg
      v-if="showIcon"
      :class="iconSizeClass"
      class="flex-shrink-0"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      viewBox="0 0 24 24"
    >
      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
      <circle cx="12" cy="10" r="3" />
    </svg>
    <span>{{ location }}</span>
  </a>

  <span v-else :class="[textSizeClass, 'text-gray-300 italic']">
    Lokacija nije navedena
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  location: {
    type: String,
    default: ''
  },
  showIcon: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'sm',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  },
  textColor: {
    type: String,
    default: 'text-gray-400'
  },
  hoverColor: {
    type: String,
    default: 'hover:text-purple-600'
  }
})

const mapsUrl = computed(() => {
  if (!props.location) return '#'
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(props.location)}`
})

const sizeMap = {
  sm: { icon: 'w-3.5 h-3.5', text: 'text-xs', gap: 'gap-1' },
  md: { icon: 'w-4 h-4', text: 'text-sm', gap: 'gap-1.5' },
  lg: { icon: 'w-5 h-5', text: 'text-base', gap: 'gap-2' }
}

const iconSizeClass = computed(() => sizeMap[props.size].icon)
const textSizeClass = computed(() => sizeMap[props.size].text)
const gapClass = computed(() => sizeMap[props.size].gap)
const textColorClass = computed(() => props.textColor)
const hoverColorClass = computed(() => props.hoverColor)
</script>