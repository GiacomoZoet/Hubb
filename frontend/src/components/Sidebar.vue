<template>
  <div class="sidebar">
    <div class="logo">iMU</div>
    <div class="workspace-list">
      <div
          v-for="ws in workspaces"
          :key="ws.id"
          class="workspace-icon"
          :class="{ active: activeWorkspace?.id === ws.id }"
          @click="$emit('selectWorkspace', ws)"
          :title="ws.name"
      >
        {{ ws.name.charAt(0).toUpperCase() }}
      </div>
    </div>
    <div class="sidebar-bottom">
      <UserAvatar :user="authStore.user" @click="logout" title="Click to logout" />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import UserAvatar from './UserAvatar.vue'

defineProps(['workspaces', 'activeWorkspace'])
defineEmits(['selectWorkspace'])

const authStore = useAuthStore()
const router = useRouter()

async function logout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 68px;
  background: #0f0f23;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
  gap: 0.75rem;
}
.logo {
  font-weight: bold;
  font-size: 1rem;
  color: #e94560;
  margin-bottom: 1rem;
}
.workspace-list { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
.workspace-icon {
  width: 44px; height: 44px;
  background: #16213e;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; font-weight: bold; font-size: 1.1rem;
  transition: border-radius 0.2s, background 0.2s;
}
.workspace-icon:hover, .workspace-icon.active {
  background: #e94560; border-radius: 16px;
}
.sidebar-bottom { margin-top: auto; }
</style>
