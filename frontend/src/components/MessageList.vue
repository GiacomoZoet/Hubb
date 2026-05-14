<template>
  <div ref="listEl" class="flex-1 overflow-y-auto px-5 py-4 flex flex-col gap-0.5">
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
