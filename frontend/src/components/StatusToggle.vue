<template>
  <div class="flex items-center space-x-3">
    <span 
      class="text-sm font-medium px-2.5 py-0.5 rounded-full uppercase tracking-wider"
      :class="modelValue ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
    >
      {{ modelValue ? 'Aktivna' : 'Deaktivirana' }}
    </span>

    <button
      type="button"
      @click="toggleStatus"
      :class="modelValue ? 'bg-green-500' : 'bg-gray-300'"
      class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
      role="switch"
      :aria-checked="modelValue"
    >
      <span
        :class="modelValue ? 'translate-x-5' : 'translate-x-0'"
        class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
      />
    </button>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// modelValue omogućava dvosmjernu komunikaciju (v-model) sa roditeljskom komponentom
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const toggleStatus = () => {
  const newValue = !props.modelValue
  emit('update:modelValue', newValue)
  emit('change', newValue)
}
</script>