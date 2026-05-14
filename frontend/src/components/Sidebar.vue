<template>
  <div class="hidden md:flex w-[60px] shrink-0 flex-col items-center py-3 gap-2 bg-teal-primary dark:bg-gray-950 h-screen">
    <div class="font-bold text-sm text-white dark:text-teal-primary mb-2 tracking-tight">hub</div>
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
      <div
        class="w-9 h-9 rounded-xl flex items-center justify-center text-lg cursor-pointer transition-all bg-white/25 text-white dark:bg-gray-800 dark:text-gray-400 hover:bg-white/40 dark:hover:bg-gray-700"
        title="Create huub"
        @click="showCreateWsModal = true"
      >+</div>
    </div>

    <!-- Create Workspace modal -->
    <div v-if="showCreateWsModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showCreateWsModal = false">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-80 border border-teal-border dark:border-gray-700 flex flex-col gap-4 shadow-lg">
        <h3 class="font-bold text-gray-900 dark:text-gray-100">New huub</h3>
        <input
          v-model="newWsName"
          placeholder="My Team"
          class="w-full px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-primary"
        />
        <p v-if="createWsError" class="text-xs text-red-500">{{ createWsError }}</p>
        <div class="flex gap-2 justify-end">
          <button @click="showCreateWsModal = false" class="px-4 py-2 rounded-lg text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">Cancel</button>
          <button @click="handleCreateWs" :disabled="createWsLoading" class="px-4 py-2 rounded-lg text-sm bg-teal-primary text-white font-semibold hover:bg-teal-dark transition-colors disabled:opacity-60">{{ createWsLoading ? 'Creating...' : 'Create' }}</button>
        </div>
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

    <div class="relative mb-1">
      <UserAvatar :user="authStore.user" @click="showProfile = !showProfile" />

      <div v-if="showProfile" class="fixed inset-0 z-40" @click="showProfile = false"></div>
      <div
        v-if="showProfile"
        class="absolute bottom-12 left-12 w-56 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-teal-border dark:border-gray-700 p-3 flex flex-col gap-2 z-50"
      >
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-teal-primary text-white flex items-center justify-center font-bold text-sm shrink-0">
            {{ authStore.user?.username?.charAt(0).toUpperCase() }}
          </div>
          <div class="flex flex-col min-w-0">
            <span class="text-sm font-bold text-gray-800 dark:text-gray-100 truncate">{{ authStore.user?.username }}</span>
            <span class="text-[11px] text-gray-400 dark:text-gray-500 truncate">{{ authStore.user?.email }}</span>
          </div>
        </div>
        <div class="border-t border-gray-100 dark:border-gray-700"></div>
        <button
          @click.stop="logout"
          class="text-left text-sm text-red-500 hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 transition-colors"
        >Logout</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import UserAvatar from './UserAvatar.vue'
import { toggleDarkMode } from '@/utils/darkMode'
import { getInvitations, acceptInvitation, declineInvitation, createWorkspace } from '@/api/workspaces'

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
const showProfile = ref(false)

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

const showCreateWsModal = ref(false)
const newWsName = ref('')
const createWsError = ref('')
const createWsLoading = ref(false)

async function handleCreateWs() {
  if (!newWsName.value.trim()) return
  createWsLoading.value = true
  createWsError.value = ''
  try {
    const res = await createWorkspace({ name: newWsName.value.trim() })
    showCreateWsModal.value = false
    newWsName.value = ''
    router.push(`/workspace/${res.data.workspace.slug}`)
  } catch (e) {
    createWsError.value = e.response?.data?.error || 'Failed to create huub'
  } finally {
    createWsLoading.value = false
  }
}
</script>
