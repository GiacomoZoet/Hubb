<template>
  <div class="flex items-center justify-around border-t border-teal-border dark:border-gray-700 bg-white dark:bg-gray-900 shrink-0 pb-safe">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      class="flex flex-col items-center justify-center flex-1 py-2 gap-0.5 text-xs font-medium transition-colors"
      :class="activePanel === tab.id ? 'text-teal-primary' : 'text-gray-400 dark:text-gray-500'"
      @click="$emit('update:activePanel', tab.id)"
    >
      <span class="text-base leading-none">{{ tab.icon }}</span>
      <span>{{ tab.label }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps(['activePanel'])
defineEmits(['update:activePanel'])

const tabs = [
  { id: 'channels', icon: '#', label: 'Channels' },
  { id: 'chat', icon: '💬', label: 'Chat' },
  { id: 'dm', icon: '✉', label: 'DMs' },
]
</script>
