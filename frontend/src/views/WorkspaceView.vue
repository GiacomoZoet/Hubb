<template>
  <div class="workspace-layout">
    <Sidebar :workspaces="workspaces" :activeWorkspace="activeWorkspace" @selectWorkspace="handleSelectWorkspace" />
    <ChannelList :channels="channels" :activeChannel="activeChannel" :workspaceId="activeWorkspace?.id" @selectChannel="handleSelectChannel" />
    <ChatArea v-if="activeChannel" :channel="activeChannel" />
    <div v-else class="no-channel">
      <p>Select a channel to start chatting</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import ChannelList from '@/components/ChannelList.vue'
import ChatArea from '@/components/ChatArea.vue'
import { listWorkspaces, getWorkspace, listChannels } from '@/api/workspaces'

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

<style scoped>
.workspace-layout {
  display: flex;
  height: 100vh;
  background: #1a1a2e;
  color: white;
}
.no-channel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 1.1rem;
}
</style>
