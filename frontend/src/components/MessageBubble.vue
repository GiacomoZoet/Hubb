<template>
  <div class="flex gap-3 px-2 py-1.5 rounded-lg hover:bg-teal-lighter/60 dark:hover:bg-gray-800/60 group">
    <div class="w-9 h-9 rounded-full bg-teal-primary shrink-0 flex items-center justify-center font-bold text-sm text-white">
      {{ message.username?.charAt(0).toUpperCase() || '?' }}
    </div>
    <div class="flex flex-col gap-0.5 min-w-0">
      <div class="flex items-baseline gap-2">
        <span class="text-xs font-semibold text-teal-primary dark:text-teal-primary">{{ message.username }}</span>
        <span class="text-[10px] text-gray-400 dark:text-gray-500">{{ formatTime(message.created_at) }}</span>
        <span v-if="message.is_edited" class="text-[10px] text-gray-400 dark:text-gray-500">(edited)</span>
      </div>
      <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed break-words">{{ message.content }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps(['message'])

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
