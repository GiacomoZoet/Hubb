<template>
  <div class="px-4 py-3 border-t border-teal-border dark:border-gray-700 shrink-0">
    <div class="flex items-center gap-2 bg-teal-lighter dark:bg-gray-800 border border-teal-border dark:border-gray-700 rounded-xl px-4 py-2.5 focus-within:ring-2 focus-within:ring-teal-primary transition-shadow">
      <input
        v-model="content"
        :placeholder="`Message #${channelId}`"
        @keydown.enter="sendMessage"
        @input="handleTyping"
        class="flex-1 bg-transparent text-sm text-gray-800 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-500 outline-none"
      />
      <button
        @click="sendMessage"
        :disabled="!content.trim()"
        class="bg-teal-primary text-white text-xs font-semibold px-3 py-1.5 rounded-lg hover:bg-teal-dark transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'
import { sendMessage as apiSendMessage } from '@/api/messages'

const props = defineProps(['channelId'])
const chatStore = useChatStore()
const content = ref('')
let typingTimeout = null

async function sendMessage() {
  if (!content.value.trim()) return
  try {
    await apiSendMessage(props.channelId, { content: content.value })
    content.value = ''
  } catch (e) {
    console.error('Failed to send message', e)
  }
}

function handleTyping() {
  clearTimeout(typingTimeout)
  typingTimeout = setTimeout(() => {
    chatStore.sendTyping(props.channelId)
  }, 300)
}
</script>
