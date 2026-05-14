<template>
  <div class="flex h-screen overflow-hidden bg-teal-lighter dark:bg-gray-900">
    <Sidebar :workspaces="workspaces" :activeWorkspace="activeWorkspace" @selectWorkspace="handleSelectWorkspace" />
    <ChannelList
      :channels="channels"
      :activeChannel="activeChannel"
      :workspaceId="activeWorkspace?.id"
      :workspaceName="activeWorkspace?.name"
      @selectChannel="handleSelectChannel"
    />
    <ChatArea v-if="activeChannel" :channel="activeChannel" class="flex-1 min-w-0" />
    <div v-else class="flex-1 flex items-center justify-center text-sm text-gray-400 dark:text-gray-500">
      Select a channel to start chatting
    </div>
    <DirectMessagePanel />
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
