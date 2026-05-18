<template>
  <div class="shrink-0 flex flex-col bg-teal-light dark:bg-gray-800 border-l border-teal-border dark:border-gray-700 h-full overflow-hidden">

    <!-- Inbox -->
    <div v-if="!dmStore.activeUser" class="flex flex-col h-full">
      <div class="px-3 pt-3.5 pb-2 border-b border-teal-border dark:border-gray-700 shrink-0 flex items-center gap-2">
        <button
          @click="$emit('back')"
          class="md:hidden text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-sm transition-colors"
        >←</button>
        <div class="text-[10px] font-bold text-teal-primary uppercase tracking-widest">Direct Messages</div>
      </div>
      <div class="flex-1 overflow-y-auto py-2">
        <div
          v-for="contact in dmStore.inbox"
          :key="contact.id"
          class="flex items-center gap-2.5 px-3 py-2 cursor-pointer hover:bg-teal-border/40 dark:hover:bg-gray-700 transition-colors"
          @click="openConversation(contact)"
        >
          <div :class="['w-8 h-8 rounded-full shrink-0 flex items-center justify-center font-bold text-sm text-white', userColor(contact.username)]">
            {{ contact.username.charAt(0).toUpperCase() }}
          </div>
          <span class="text-xs text-teal-text dark:text-gray-300 flex-1 truncate">{{ contact.username }}</span>
          <span v-if="contact.unread_count > 0" class="w-4 h-4 rounded-full bg-teal-primary text-white text-[9px] flex items-center justify-center font-bold">
            {{ contact.unread_count }}
          </span>
        </div>
      </div>
      <button
        class="px-3 py-2.5 text-xs text-teal-primary hover:text-teal-dark border-t border-teal-border dark:border-gray-700 text-left transition-colors shrink-0"
        @click="showSearch = true"
      >
        + New Message
      </button>
      <div v-if="showSearch" class="px-3 pb-3 shrink-0">
        <input
          v-model="searchQuery"
          placeholder="Search users..."
          @input="searchUsers"
          class="w-full px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-white dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary"
        />
        <div
          v-for="user in searchResults"
          :key="user.id"
          class="px-2 py-1.5 mt-1 text-xs text-teal-text dark:text-gray-300 cursor-pointer rounded-md hover:bg-teal-border/40 dark:hover:bg-gray-700"
          @click="openConversation(user)"
        >
          {{ user.username }}
        </div>
      </div>
    </div>

    <!-- Active conversation -->
    <div v-else class="flex flex-col h-full">
      <div class="flex items-center gap-2 px-3 py-3.5 border-b border-teal-border dark:border-gray-700 shrink-0">
        <button @click="dmStore.activeUser = null" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-sm transition-colors">←</button>
        <span class="text-sm font-semibold text-gray-900 dark:text-gray-100">{{ dmStore.activeUser.username }}</span>
      </div>
      <div ref="messagesEl" class="flex-1 overflow-y-auto p-3 flex flex-col gap-2">
        <div
          v-for="msg in dmStore.activeConversation"
          :key="msg.id"
          class="flex flex-col max-w-[85%] gap-0.5"
          :class="msg.sender_id === authStore.user?.id ? 'self-end items-end' : 'self-start items-start'"
        >
          <div
            class="px-3 py-2 rounded-2xl text-xs leading-relaxed"
            :class="msg.sender_id === authStore.user?.id
              ? 'bg-teal-primary text-white rounded-tr-sm'
              : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-tl-sm border border-teal-border dark:border-gray-600'"
          >
            {{ msg.content }}
          </div>
          <span class="text-[10px] text-gray-400 dark:text-gray-500 px-1">{{ formatTime(msg.created_at) }}</span>
        </div>
      </div>
      <div class="px-3 py-2.5 border-t border-teal-border dark:border-gray-700 flex gap-2 shrink-0 pb-safe">
        <input
          v-model="newMessage"
          :placeholder="`Message ${dmStore.activeUser.username}`"
          @keydown.enter="sendMessage"
          class="flex-1 px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-white dark:bg-gray-900 text-xs text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary"
        />
        <button
          @click="sendMessage"
          class="bg-teal-primary text-white text-xs font-semibold px-3 py-2 rounded-lg hover:bg-teal-dark transition-colors"
        >
          Send
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { userColor } from '@/utils/userColor'
import { useDMStore } from '@/stores/dm'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const dmStore = useDMStore()
const authStore = useAuthStore()
defineEmits(['back'])

const newMessage = ref('')
const showSearch = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
const messagesEl = ref(null)

onMounted(() => dmStore.loadInbox())

async function openConversation(user) {
  dmStore.activeUser = user
  showSearch.value = false
  searchQuery.value = ''
  searchResults.value = []
  await dmStore.loadConversation(user.id)
  scrollToBottom()
}

async function sendMessage() {
  if (!newMessage.value.trim()) return
  await dmStore.send(dmStore.activeUser.id, newMessage.value)
  newMessage.value = ''
  scrollToBottom()
}

async function searchUsers() {
  if (searchQuery.value.length < 2) return
  const res = await api.get(`/users/search?q=${searchQuery.value}`)
  searchResults.value = res.data
}

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

watch(() => dmStore.activeConversation.length, scrollToBottom)

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
