<template>
  <div class="chat-area">
    <div class="chat-header">
      <span class="hash">#</span> {{ channel.name }}
    </div>
    <MessageList />  <!-- ← no prop, reads from store directly -->
    <div class="typing-indicator" v-if="chatStore.typingUsers.length">
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
  chatStore.joinChannel(channel.id)
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

<style scoped>
.chat-area {
  flex: 1; display: flex; flex-direction: column;
  background: #1a1a2e; overflow: hidden;
}
.chat-header {
  padding: 1rem 1.5rem; border-bottom: 1px solid #222;
  font-weight: bold; font-size: 1rem; display: flex; align-items: center; gap: 0.4rem;
}
.hash { color: #888; }
.desc { font-weight: 400; color: #888; font-size: 0.9rem; }
.typing-indicator {
  padding: 0.3rem 1.5rem; font-size: 0.8rem; color: #888; min-height: 1.5rem;
}
</style>
