<template>
  <div class="flex flex-col h-dvh bg-teal-lighter dark:bg-gray-900">
    <div class="flex flex-1 overflow-hidden">
      <Sidebar
        class="hidden md:flex"
        :workspaces="workspaces"
        :activeWorkspace="activeWorkspace"
        @selectWorkspace="handleSelectWorkspace"
      />
      <ChannelList
        :channels="channels"
        :activeChannel="activeChannel"
        :workspaceId="activeWorkspace?.id"
        :workspaceName="activeWorkspace?.name"
        :workspaces="workspaces"
        :activeWorkspace="activeWorkspace"
        :class="activeMobilePanel === 'channels' ? 'w-full md:w-[220px]' : 'hidden md:flex md:w-[220px]'"
        @selectChannel="handleSelectChannel"
        @channelCreated="reloadChannels"
        @selectWorkspace="handleSelectWorkspace"
      />
      <ChatArea
        v-if="activeChannel"
        :channel="activeChannel"
        :class="activeMobilePanel === 'chat' ? 'flex-1 min-w-0' : 'hidden md:flex flex-1 min-w-0'"
        @back="activeMobilePanel = 'channels'"
      />
      <div
        v-else
        :class="activeMobilePanel === 'chat' ? 'flex flex-1 items-center justify-center text-sm text-gray-400 dark:text-gray-500' : 'hidden md:flex flex-1 items-center justify-center text-sm text-gray-400 dark:text-gray-500'"
      >
        Select a channel to start chatting
      </div>
      <DirectMessagePanel
        :class="activeMobilePanel === 'dm' ? 'w-full md:w-[240px]' : 'hidden md:flex md:w-[240px]'"
        @back="activeMobilePanel = 'channels'"
      />
    </div>
    <BottomTabBar
      class="md:hidden"
      :activePanel="activeMobilePanel"
      :chatUnread="chatUnread"
      :dmUnread="dmUnread"
      @update:activePanel="activeMobilePanel = $event"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import ChannelList from '@/components/ChannelList.vue'
import ChatArea from '@/components/ChatArea.vue'
import { listWorkspaces, getWorkspace, listChannels } from '@/api/workspaces'
import DirectMessagePanel from '@/components/DirectMessagePanel.vue'
import BottomTabBar from '@/components/BottomTabBar.vue'
import { useChatStore } from '@/stores/chat'
import { useDMStore } from '@/stores/dm'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()
const dmStore = useDMStore()

const chatUnread = ref(false)
const dmUnread = computed(() => dmStore.inbox.reduce((sum, c) => sum + (c.unread_count || 0), 0))

const workspaces = ref([])
const activeWorkspace = ref(null)
const channels = ref([])
const activeChannel = ref(null)
const activeMobilePanel = ref('channels')

async function loadWorkspace(slug) {
  const res = await getWorkspace(slug)
  activeWorkspace.value = res.data
  chatStore.connectSocket()
  if (chatStore.socket?.connected) {
    chatStore.joinWorkspace(res.data.id)
  } else {
    chatStore.socket?.once('connect', () => chatStore.joinWorkspace(res.data.id))
  }
  const chRes = await listChannels(res.data.id)
  channels.value = chRes.data
  if (chRes.data.length > 0) activeChannel.value = chRes.data[0]
}

function handleSelectWorkspace(workspace) {
  router.push(`/workspace/${workspace.slug}`)
}

function handleSelectChannel(channel) {
  activeChannel.value = channel
  activeMobilePanel.value = 'chat'
}

async function reloadChannels() {
  const chRes = await listChannels(activeWorkspace.value.id)
  channels.value = chRes.data
}

async function goToNextWorkspace(deletedId) {
  const res = await listWorkspaces()
  const remaining = res.data.filter(w => w.id !== deletedId)
  if (remaining.length > 0) {
    router.push(`/workspace/${remaining[0].slug}`)
  } else {
    router.push('/create-workspace')
  }
}

watch(() => chatStore.deletedWorkspaceId, (id) => {
  if (id && activeWorkspace.value?.id === id) {
    chatStore.deletedWorkspaceId = null
    goToNextWorkspace(id)
  }
})

watch(() => chatStore.messages.length, (newLen, oldLen) => {
  if (newLen > oldLen && activeMobilePanel.value !== 'chat') chatUnread.value = true
})

watch(activeMobilePanel, (panel) => {
  if (panel === 'chat') chatUnread.value = false
})

onMounted(async () => {
  const wsRes = await listWorkspaces()
  workspaces.value = wsRes.data
  await loadWorkspace(route.params.slug)
})

watch(() => route.params.slug, async (slug) => {
  if (slug) {
    const wsRes = await listWorkspaces()
    workspaces.value = wsRes.data
    await loadWorkspace(slug)
  }
})
</script>
