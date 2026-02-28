<template>
  <div class="message-list" ref="listEl">
    <MessageBubble v-for="msg in chatStore.messages" :key="msg.id" :message="msg" />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import MessageBubble from './MessageBubble.vue'

const chatStore = useChatStore()
const listEl = ref(null)

// Auto-scroll when new messages arrive
watch(() => chatStore.messages.length, async () => {
  await nextTick()
  if (listEl.value) listEl.value.scrollTop = listEl.value.scrollHeight
})
</script>


<style scoped>
.message-list {
  flex: 1; overflow-y: auto; padding: 1rem 1.5rem;
  display: flex; flex-direction: column; gap: 0.2rem;
}
</style>
