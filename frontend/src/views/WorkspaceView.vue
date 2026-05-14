<template>
  <div class="flex h-screen overflow-hidden bg-teal-lighter dark:bg-gray-900">
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
      @showDM="activeMobilePanel = 'dm'"
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
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import ChannelList from '@/components/ChannelList.vue'
import ChatArea from '@/components/ChatArea.vue'
import { listWorkspaces, getWorkspace, listChannels } from '@/api/workspaces'
import DirectMessagePanel from '@/components/DirectMessagePanel.vue'


const route = useRoute()
const router = useRouter()

const workspaces = ref([])
const activeWorkspace = ref(null)
const channels = ref([])
const activeChannel = ref(null)
const activeMobilePanel = ref('channels')

async function loadWorkspace(slug) {
  const res = await getWorkspace(slug)
  activeWorkspace.value = res.data
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

onMounted(async () => {
  const wsRes = await listWorkspaces()
  workspaces.value = wsRes.data
  await loadWorkspace(route.params.slug)
})

watch(() => route.params.slug, (slug) => {
  if (slug) loadWorkspace(slug)
})
</script>
