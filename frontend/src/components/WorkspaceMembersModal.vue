<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" @click.self="$emit('close')">
    <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-80 border border-teal-border dark:border-gray-700 flex flex-col gap-4 shadow-lg">
      <h3 class="font-bold text-gray-900 dark:text-gray-100">{{ workspaceName }}</h3>

      <div class="flex flex-col gap-1 max-h-48 overflow-y-auto">
        <div
          v-for="m in members"
          :key="m.id"
          class="flex items-center justify-between px-2 py-1.5 rounded-lg text-sm text-gray-700 dark:text-gray-300"
        >
          <span>{{ m.username }}</span>
          <span class="text-xs text-gray-400 dark:text-gray-500 capitalize">{{ m.role }}</span>
        </div>
      </div>

      <div v-if="myRole === 'owner'" class="flex flex-col gap-2 pt-2 border-t border-teal-border dark:border-gray-700">
        <div v-if="!showInvite">
          <button
            @click="showInvite = true"
            class="px-4 py-2 rounded-lg text-sm text-teal-primary hover:bg-teal-lighter dark:hover:bg-gray-700 transition-colors text-left w-full"
          >+ Invite member</button>
        </div>
        <div v-else class="flex flex-col gap-2">
          <input
            v-model="inviteEmail"
            placeholder="email@example.com"
            type="email"
            class="w-full px-3 py-2 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-primary"
          />
          <p v-if="inviteError" class="text-xs text-red-500">{{ inviteError }}</p>
          <div class="flex gap-2 justify-end">
            <button @click="showInvite = false; inviteEmail = ''; inviteError = ''" class="px-3 py-1.5 rounded-lg text-sm text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">Cancel</button>
            <button @click="sendInvite" class="px-3 py-1.5 rounded-lg text-sm bg-teal-primary text-white font-semibold hover:bg-teal-dark transition-colors">Send</button>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-2 pt-2 border-t border-teal-border dark:border-gray-700">
        <button
          v-if="myRole && myRole !== 'owner'"
          @click="handleLeave"
          class="px-4 py-2 rounded-lg text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-left"
        >Leave huub</button>
        <button
          v-if="myRole === 'owner'"
          @click="handleDelete"
          class="px-4 py-2 rounded-lg text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-left"
        >Delete huub</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { listMembers, leaveWorkspace, deleteWorkspace, listWorkspaces, inviteMember } from '@/api/workspaces'

const props = defineProps(['workspaceId', 'workspaceName'])
const emit = defineEmits(['close'])

const router = useRouter()
const authStore = useAuthStore()
const members = ref([])

onMounted(async () => {
  const res = await listMembers(props.workspaceId)
  members.value = res.data
})

const showInvite = ref(false)
const inviteEmail = ref('')
const inviteError = ref('')

async function sendInvite() {
  if (!inviteEmail.value.trim()) return
  inviteError.value = ''
  try {
    await inviteMember(props.workspaceId, { email: inviteEmail.value.trim() })
    showInvite.value = false
    inviteEmail.value = ''
  } catch (err) {
    inviteError.value = err.response?.data?.error || 'Something went wrong'
  }
}

const myRole = computed(() => {
  const me = members.value.find(m => m.id === authStore.user?.id)
  return me?.role
})

async function goToNextWorkspace() {
  const res = await listWorkspaces()
  const remaining = res.data.filter(w => w.id !== props.workspaceId)
  if (remaining.length > 0) {
    router.push(`/workspace/${remaining[0].slug}`)
  } else {
    router.push('/create-workspace')
  }
}

async function handleLeave() {
  if (!confirm('Leave this huub?')) return
  try {
    await leaveWorkspace(props.workspaceId)
    goToNextWorkspace()
  } catch (err) {
    alert(err.response?.data?.error || 'Could not leave huub')
  }
}

async function handleDelete() {
  if (!confirm('Delete this huub? This cannot be undone.')) return
  try {
    await deleteWorkspace(props.workspaceId)
    goToNextWorkspace()
  } catch (err) {
    alert(err.response?.data?.error || 'Could not delete huub')
  }
}
</script>
