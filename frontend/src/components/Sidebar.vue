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
    <UserAvatar :user="authStore.user" @click="logout" title="Click to logout" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import UserAvatar from './UserAvatar.vue'
import { toggleDarkMode } from '@/utils/darkMode'

const isDark = ref(false)
onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
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
</script>
