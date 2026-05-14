<template>
  <div class="w-[220px] shrink-0 flex flex-col bg-teal-light dark:bg-gray-800 border-r border-teal-border dark:border-gray-700 h-screen overflow-hidden">
    <div class="px-3 py-3.5 border-b border-teal-border dark:border-gray-700 shrink-0">
      <div class="font-bold text-sm text-teal-text dark:text-gray-100 truncate">{{ workspaceName || 'Workspace' }}</div>
    </div>

    <div class="flex-1 overflow-y-auto py-2">
      <div class="px-3 py-2 text-[10px] font-bold text-teal-primary uppercase tracking-widest">Channels</div>
      <div
        v-for="ch in channels"
        :key="ch.id"
        class="flex items-center gap-1.5 px-2.5 py-1.5 mx-1.5 rounded-md text-xs cursor-pointer"
        :class="activeChannel?.id === ch.id
          ? 'bg-teal-primary text-white font-semibold'
          : 'text-teal-text dark:text-gray-400 hover:bg-teal-border/50 dark:hover:bg-gray-700'"
        @click="$emit('selectChannel', ch)"
      >
        <span class="opacity-60 text-[11px]">{{ ch.is_private ? '🔒' : '#' }}</span>
        {{ ch.name }}
      </div>
      <button
        class="flex items-center gap-1 px-4 py-1.5 mx-1.5 mt-1 text-xs text-teal-primary hover:text-teal-dark transition-colors"
        @click="showModal = true"
      >
        + Add Channel
      </button>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showModal = false">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-80 border border-teal-border dark:border-gray-700 flex flex-col gap-4 shadow-lg">
        <h3 class="font-bold text-gray-900 dark:text-gray-100">New Channel</h3>
        <input
          v-model="newChannelName"
          placeholder="channel-name"
          class="w-full px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-primary"
        />
        <label class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
          <input type="checkbox" v-model="isPrivate" class="accent-teal-primary" />
          Private channel
        </label>
        <div class="flex gap-2 justify-end">
          <button @click="showModal = false" class="px-4 py-2 rounded-lg text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">Cancel</button>
          <button @click="createNewChannel" class="px-4 py-2 rounded-lg text-sm bg-teal-primary text-white font-semibold hover:bg-teal-dark transition-colors">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createChannel } from '@/api/workspaces'

const props = defineProps(['channels', 'activeChannel', 'workspaceId', 'workspaceName'])
defineEmits(['selectChannel'])

const showModal = ref(false)
const newChannelName = ref('')
const isPrivate = ref(false)

async function createNewChannel() {
  if (!newChannelName.value.trim()) return
  await createChannel(props.workspaceId, {
    name: newChannelName.value.trim(),
    is_private: isPrivate.value
  })
  showModal.value = false
  newChannelName.value = ''
  // Reload channels — parent will handle via emit if needed
  window.location.reload()
}
</script>
