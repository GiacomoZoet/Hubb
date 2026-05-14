<template>
  <div class="flex-1 flex flex-col bg-white dark:bg-gray-900 min-w-0 h-screen overflow-hidden">
    <div class="flex items-center gap-2 px-5 py-3.5 border-b border-teal-border dark:border-gray-700 shrink-0">
      <span class="text-teal-primary font-bold text-base">#</span>
      <span class="font-bold text-gray-900 dark:text-gray-100 text-sm">{{ channel.name }}</span>
    </div>
    <MessageList class="flex-1 min-h-0" />
    <div v-if="chatStore.typingUsers.length" class="px-5 py-1 text-xs text-gray-400 dark:text-gray-500 shrink-0">
      {{ chatStore.typingUsers.join(', ') }} is typing...
    </div>
    <MessageInput :channelId="channel.id" />
  </div>
</template>


<script setup>
import { watch, onMounted, onUnmounted } from 'vue'
import MessageList from './MessageList.vue'
import MessageInput from './MessageInput.vue'
import { useChatStore } from '@/stores/chat'

const props = defineProps(['channel'])
const chatStore = useChatStore()

async function loadChannel(channel) {
  if (!channel) return
  chatStore.leaveChannel(channel.id)
  await chatStore.loadMessages(channel.id)
  if (chatStore.socket?.connected) {
    chatStore.joinChannel(channel.id)
  } else {
    chatStore.socket?.once('connect', () => chatStore.joinChannel(channel.id))
  }
}

onMounted(() => {
  chatStore.connectSocket()
  loadChannel(props.channel)
})

onUnmounted(() => {
  chatStore.leaveChannel(props.channel?.id)
})

watch(() => props.channel, loadChannel)
</script>
