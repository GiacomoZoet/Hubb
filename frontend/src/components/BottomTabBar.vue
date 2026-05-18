<template>
  <div class="flex items-center justify-around border-t border-teal-border dark:border-gray-700 bg-white dark:bg-gray-900 shrink-0 pb-safe">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      class="flex flex-col items-center justify-center flex-1 py-2 gap-0.5 text-xs font-medium transition-colors"
      :class="activePanel === tab.id ? 'text-teal-primary' : 'text-gray-400 dark:text-gray-500'"
      @click="$emit('update:activePanel', tab.id)"
    >
      <div class="relative">
        <span class="text-base leading-none">{{ tab.icon }}</span>
        <span
          v-if="(tab.id === 'chat' && chatUnread) || (tab.id === 'dm' && dmUnread > 0)"
          class="absolute -top-0.5 -right-1.5 w-2 h-2 bg-red-500 rounded-full block"
        ></span>
      </div>
      <span>{{ tab.label }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps(['activePanel', 'chatUnread', 'dmUnread'])
defineEmits(['update:activePanel'])

const tabs = [
  { id: 'channels', icon: '#', label: 'Channels' },
  { id: 'chat', icon: '💬', label: 'Chat' },
  { id: 'dm', icon: '✉', label: 'DMs' },
]
</script>
