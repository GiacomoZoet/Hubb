<template>
  <div class="message-input">
    <input
        v-model="content"
        :placeholder="`Message #${channelId}`"
        @keydown.enter="sendMessage"
        @input="handleTyping"
    />
    <button @click="sendMessage" :disabled="!content.trim()">Send</button>
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

<style scoped>
.message-input {
  padding: 1rem 1.5rem; display: flex; gap: 0.75rem;
  border-top: 1px solid #222;
}
input {
  flex: 1; padding: 0.75rem 1rem; border-radius: 8px;
  border: 1px solid #333; background: #0f3460; color: white;
  font-size: 0.95rem; outline: none;
}
input:focus { border-color: #e94560; }
button {
  padding: 0.75rem 1.25rem; background: #e94560; color: white;
  border: none; border-radius: 8px; cursor: pointer; font-size: 0.95rem;
}
button:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
