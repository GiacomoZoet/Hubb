<template>
  <div class="flex-1 flex flex-col bg-white dark:bg-gray-900 min-w-0 h-screen overflow-hidden">
    <div class="flex items-center gap-2 px-5 py-3.5 border-b border-teal-border dark:border-gray-700 shrink-0">
      <span class="text-teal-primary font-bold text-base">{{ channel.is_private ? '🔒' : '#' }}</span>
      <span class="font-bold text-gray-900 dark:text-gray-100 text-sm flex-1">{{ channel.name }}</span>
      <button
        v-if="channel.is_private"
        @click="showAddMemberModal = true"
        class="text-xs text-teal-primary hover:text-teal-dark transition-colors"
      >Add member</button>
    </div>
    <MessageList class="flex-1 min-h-0" />
    <div v-if="chatStore.typingUsers.length" class="px-5 py-1 text-xs text-gray-400 dark:text-gray-500 shrink-0">
      {{ chatStore.typingUsers.join(', ') }} is typing...
    </div>
    <MessageInput :channelId="channel.id" />

    <!-- Add Member modal -->
    <div v-if="showAddMemberModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeAddMemberModal">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-80 border border-teal-border dark:border-gray-700 flex flex-col gap-4 shadow-lg">
        <h3 class="font-bold text-gray-900 dark:text-gray-100">Add to Channel</h3>
        <input
          v-model="addEmail"
          placeholder="email@example.com"
          type="email"
          class="w-full px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-primary"
        />
        <p v-if="addError" class="text-xs text-red-500">{{ addError }}</p>
        <div class="flex gap-2 justify-end">
          <button @click="closeAddMemberModal" class="px-4 py-2 rounded-lg text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">Cancel</button>
          <button @click="submitAddMember" class="px-4 py-2 rounded-lg text-sm bg-teal-primary text-white font-semibold hover:bg-teal-dark transition-colors">Add</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import MessageList from './MessageList.vue'
import MessageInput from './MessageInput.vue'
import { useChatStore } from '@/stores/chat'
import { addChannelMember } from '@/api/workspaces'

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

const showAddMemberModal = ref(false)
const addEmail = ref('')
const addError = ref('')

function closeAddMemberModal() {
  showAddMemberModal.value = false
  addEmail.value = ''
  addError.value = ''
}

async function submitAddMember() {
  if (!addEmail.value.trim()) return
  addError.value = ''
  try {
    await addChannelMember(props.channel.id, { email: addEmail.value.trim() })
    closeAddMemberModal()
  } catch (err) {
    addError.value = err.response?.data?.error || 'Something went wrong'
  }
}
</script>
