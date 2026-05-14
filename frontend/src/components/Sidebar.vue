<template>
  <div class="w-[60px] shrink-0 flex flex-col items-center py-3 gap-2 bg-teal-primary dark:bg-gray-950 h-screen">
    <div class="font-bold text-sm text-white dark:text-teal-primary mb-2 tracking-tight">iMU</div>
    <div class="flex flex-col gap-2 flex-1 w-full items-center">
      <div
        v-for="ws in workspaces"
        :key="ws.id"
        class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-sm cursor-pointer transition-all"
        :class="activeWorkspace?.id === ws.id
          ? 'bg-white text-teal-primary dark:bg-teal-primary dark:text-white'
          : 'bg-white/25 text-white dark:bg-gray-800 dark:text-gray-400 hover:bg-white/40 dark:hover:bg-gray-700'"
        :title="ws.name"
        @click="$emit('selectWorkspace', ws)"
      >
        {{ ws.name.charAt(0).toUpperCase() }}
      </div>
    </div>

    <button
      @click="handleToggleDark"
      class="text-white/60 dark:text-gray-500 hover:text-white dark:hover:text-gray-300 text-base mb-1"
      :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    >{{ isDark ? '☀' : '🌙' }}</button>

    <div class="relative mb-1">
      <button
        @click="showInvites = !showInvites"
        class="text-white/60 dark:text-gray-500 hover:text-white dark:hover:text-gray-300 text-base relative"
        title="Invitations"
      >
        🔔
        <span v-if="invitations.length" class="absolute -top-0.5 -right-0.5 w-2 h-2 bg-red-500 rounded-full block"></span>
      </button>

      <div v-if="showInvites" class="fixed inset-0 z-40" @click="showInvites = false"></div>
      <div
        v-if="showInvites"
        class="absolute bottom-8 left-12 w-64 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-teal-border dark:border-gray-700 p-3 flex flex-col gap-2 z-50"
      >
        <div class="text-xs font-bold text-gray-700 dark:text-gray-300 mb-1">Invitations</div>
        <div v-if="invitations.length === 0" class="text-xs text-gray-400 dark:text-gray-500">No pending invitations</div>
        <div
          v-for="inv in invitations"
          :key="inv.id"
          class="flex items-center justify-between gap-2 text-xs"
        >
          <span class="text-gray-700 dark:text-gray-300 truncate">{{ inv.workspace_name }}</span>
          <div class="flex gap-1 shrink-0">
            <button
              @click.stop="handleAccept(inv)"
              class="px-2 py-1 rounded-md bg-teal-primary text-white text-[10px] hover:bg-teal-dark transition-colors"
            >Accept</button>
            <button
              @click.stop="handleDecline(inv)"
              class="px-2 py-1 rounded-md bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-[10px] hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            >Decline</button>
          </div>
        </div>
      </div>
    </div>

    <UserAvatar :user="authStore.user" @click="logout" title="Click to logout" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import UserAvatar from './UserAvatar.vue'
import { toggleDarkMode } from '@/utils/darkMode'
import { getInvitations, acceptInvitation, declineInvitation } from '@/api/workspaces'

const isDark = ref(false)

onMounted(async () => {
  isDark.value = document.documentElement.classList.contains('dark')
  const res = await getInvitations()
  invitations.value = res.data
})

function handleToggleDark() {
  toggleDarkMode()
  isDark.value = document.documentElement.classList.contains('dark')
}

defineProps(['workspaces', 'activeWorkspace'])
defineEmits(['selectWorkspace'])

const authStore = useAuthStore()
const router = useRouter()

async function logout() {
  await authStore.logout()
  router.push('/login')
}

const invitations = ref([])
const showInvites = ref(false)

async function handleAccept(inv) {
  await acceptInvitation(inv.id)
  invitations.value = invitations.value.filter(i => i.id !== inv.id)
  showInvites.value = false
  router.push(`/workspace/${inv.workspace_slug}`)
}

async function handleDecline(inv) {
  await declineInvitation(inv.id)
  invitations.value = invitations.value.filter(i => i.id !== inv.id)
}
</script>
