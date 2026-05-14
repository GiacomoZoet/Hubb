<template>
  <div class="shrink-0 flex flex-col bg-teal-light dark:bg-gray-800 border-r border-teal-border dark:border-gray-700 h-screen overflow-hidden">
    <div class="px-3 py-3.5 border-b border-teal-border dark:border-gray-700 shrink-0 flex items-center justify-between gap-2">
      <div
        class="font-bold text-sm text-teal-text dark:text-gray-100 truncate cursor-pointer hover:opacity-75"
        @click="showMembersModal = true"
      >{{ workspaceName || 'Workspace' }}</div>
      <div class="flex items-center gap-2 shrink-0">
        <button
          @click="handleToggleDark"
          class="md:hidden text-teal-text/60 dark:text-gray-500 hover:text-teal-text dark:hover:text-gray-300 text-sm"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        >{{ isDark ? '☀' : '🌙' }}</button>
        <div class="relative md:hidden">
          <button
            @click="showInvites = !showInvites"
            class="relative text-teal-text/60 dark:text-gray-500 hover:text-teal-text dark:hover:text-gray-300 text-sm"
            title="Invitations"
          >
            🔔
            <span v-if="invitations.length" class="absolute -top-0.5 -right-0.5 w-2 h-2 bg-red-500 rounded-full block"></span>
          </button>
          <div v-if="showInvites" class="fixed inset-0 z-40" @click="showInvites = false"></div>
          <div v-if="showInvites" class="absolute top-full mt-1 right-0 w-64 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-teal-border dark:border-gray-700 p-3 flex flex-col gap-2 z-50">
            <div class="text-xs font-bold text-gray-700 dark:text-gray-300 mb-1">Invitations</div>
            <div v-if="invitations.length === 0" class="text-xs text-gray-400 dark:text-gray-500">No pending invitations</div>
            <div v-for="inv in invitations" :key="inv.id" class="flex items-center justify-between gap-2 text-xs">
              <span class="text-gray-700 dark:text-gray-300 truncate">{{ inv.workspace_name }}</span>
              <div class="flex gap-1 shrink-0">
                <button @click.stop="handleAccept(inv)" class="px-2 py-1 rounded-md bg-teal-primary text-white text-[10px] hover:bg-teal-dark transition-colors">Accept</button>
                <button @click.stop="handleDecline(inv)" class="px-2 py-1 rounded-md bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-[10px] hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">Decline</button>
              </div>
            </div>
          </div>
        </div>
        <div class="relative md:hidden">
          <div
            @click="showProfile = !showProfile"
            class="w-8 h-8 rounded-full bg-teal-primary text-white border-2 border-teal-dark flex items-center justify-center font-bold text-xs cursor-pointer hover:opacity-80 transition-all"
            :title="authStore.user?.username"
          >{{ authStore.user?.username?.charAt(0).toUpperCase() }}</div>
          <div v-if="showProfile" class="fixed inset-0 z-40" @click="showProfile = false"></div>
          <div v-if="showProfile" class="absolute top-full mt-1 right-0 w-56 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-teal-border dark:border-gray-700 p-3 flex flex-col gap-2 z-50">
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
            <button @click.stop="logout" class="text-left text-sm text-red-500 hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 transition-colors">Logout</button>
          </div>
        </div>
        <button
          @click="showInviteModal = true"
          class="hidden md:block text-xs text-teal-primary hover:text-teal-dark transition-colors"
          title="Invite member"
        >+ Member</button>
      </div>
    </div>

    <div class="md:hidden flex gap-2 px-3 py-2 overflow-x-auto border-b border-teal-border dark:border-gray-700 shrink-0">
      <div
        v-for="ws in workspaces"
        :key="ws.id"
        class="w-9 h-9 rounded-xl flex items-center justify-center font-bold text-sm cursor-pointer transition-all shrink-0"
        :class="activeWorkspace?.id === ws.id
          ? 'bg-teal-primary text-white'
          : 'bg-teal-border/50 dark:bg-gray-700 text-teal-text dark:text-gray-400 hover:bg-teal-border dark:hover:bg-gray-600'"
        :title="ws.name"
        @click="$emit('selectWorkspace', ws)"
      >
        {{ ws.name.charAt(0).toUpperCase() }}
      </div>
      <div
        class="w-9 h-9 rounded-xl flex items-center justify-center text-lg cursor-pointer transition-all shrink-0 bg-teal-border/50 dark:bg-gray-700 text-teal-primary dark:text-gray-400 hover:bg-teal-border dark:hover:bg-gray-600"
        title="Create huub"
        @click="showCreateWsModal = true"
      >+</div>
    </div>

    <div class="flex-1 overflow-y-auto py-2">
      <div class="px-3 py-2 text-[10px] font-bold text-teal-primary uppercase tracking-widest">Channels</div>
      <div
        v-for="ch in channels"
        :key="ch.id"
        class="flex items-center gap-1.5 px-2.5 py-1.5 mx-1.5 rounded-md text-xs cursor-pointer"
        :class="activeChannel?.id === ch.id
          ? 'bg-teal-primary text-white font-semibold'
          : 'text-teal-text dark:text-gray-400 hover:bg-teal-border/50 dark:hover:bg-gray-700'"
        @click="$emit('selectChannel', ch)"
      >
        <span class="opacity-60 text-[11px]">{{ ch.is_private ? '🔒' : '#' }}</span>
        {{ ch.name }}
      </div>
      <button
        class="flex items-center gap-1 px-4 py-1.5 mx-1.5 mt-1 text-xs text-teal-primary hover:text-teal-dark transition-colors"
        @click="showModal = true"
      >
        + Add Channel
      </button>
    </div>

    <button
      class="md:hidden px-4 py-2.5 text-xs text-teal-primary hover:text-teal-dark border-t border-teal-border dark:border-gray-700 text-left transition-colors shrink-0"
      @click="$emit('showDM')"
    >
      💬 Direct Messages
    </button>

    <!-- New Channel modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="showModal = false">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-80 border border-teal-border dark:border-gray-700 flex flex-col gap-4 shadow-lg">
        <h3 class="font-bold text-gray-900 dark:text-gray-100">New Channel</h3>
        <input
          v-model="newChannelName"
          placeholder="channel-name"
          class="w-full px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-primary"
        />
        <label class="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
          <input type="checkbox" v-model="isPrivate" class="accent-teal-primary" />
          Private channel
        </label>
        <div class="flex gap-2 justify-end">
          <button @click="showModal = false" class="px-4 py-2 rounded-lg text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">Cancel</button>
          <button @click="createNewChannel" class="px-4 py-2 rounded-lg text-sm bg-teal-primary text-white font-semibold hover:bg-teal-dark transition-colors">Create</button>
        </div>
      </div>
    </div>

    <!-- Invite Member modal -->
    <div v-if="showInviteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="closeInviteModal">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-80 border border-teal-border dark:border-gray-700 flex flex-col gap-4 shadow-lg">
        <h3 class="font-bold text-gray-900 dark:text-gray-100">Invite to huub</h3>
        <input
          v-model="inviteEmail"
          placeholder="email@example.com"
          type="email"
          class="w-full px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-primary"
        />
        <p v-if="inviteError" class="text-xs text-red-500">{{ inviteError }}</p>
        <div class="flex gap-2 justify-end">
          <button @click="closeInviteModal" class="px-4 py-2 rounded-lg text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">Cancel</button>
          <button @click="sendInvite" class="px-4 py-2 rounded-lg text-sm bg-teal-primary text-white font-semibold hover:bg-teal-dark transition-colors">Invite</button>
        </div>
      </div>
    </div>

    <!-- Create Workspace modal (mobile) -->
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

    <!-- Workspace Members modal -->
    <WorkspaceMembersModal
      v-if="showMembersModal"
      :workspaceId="workspaceId"
      :workspaceName="workspaceName"
      @close="showMembersModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createChannel, inviteMember, getInvitations, acceptInvitation, declineInvitation, createWorkspace } from '@/api/workspaces'
import WorkspaceMembersModal from './WorkspaceMembersModal.vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { toggleDarkMode } from '@/utils/darkMode'

const props = defineProps(['channels', 'activeChannel', 'workspaceId', 'workspaceName', 'workspaces', 'activeWorkspace'])
const emit = defineEmits(['selectChannel', 'channelCreated', 'showDM', 'selectWorkspace'])

const authStore = useAuthStore()
const router = useRouter()

const isDark = ref(false)
const invitations = ref([])
const showInvites = ref(false)
const showProfile = ref(false)

onMounted(async () => {
  isDark.value = document.documentElement.classList.contains('dark')
  const res = await getInvitations()
  invitations.value = res.data
})

function handleToggleDark() {
  toggleDarkMode()
  isDark.value = document.documentElement.classList.contains('dark')
}

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

async function logout() {
  await authStore.logout()
  router.push('/login')
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

const showModal = ref(false)
const newChannelName = ref('')
const isPrivate = ref(false)

async function createNewChannel() {
  if (!newChannelName.value.trim()) return
  await createChannel(props.workspaceId, {
    name: newChannelName.value.trim(),
    is_private: isPrivate.value
  })
  showModal.value = false
  newChannelName.value = ''
  emit('channelCreated')
}

const showInviteModal = ref(false)
const inviteEmail = ref('')
const inviteError = ref('')

function closeInviteModal() {
  showInviteModal.value = false
  inviteEmail.value = ''
  inviteError.value = ''
}

async function sendInvite() {
  if (!inviteEmail.value.trim()) return
  inviteError.value = ''
  try {
    await inviteMember(props.workspaceId, { email: inviteEmail.value.trim() })
    closeInviteModal()
  } catch (err) {
    inviteError.value = err.response?.data?.error || 'Something went wrong'
  }
}

const showMembersModal = ref(false)
</script>
