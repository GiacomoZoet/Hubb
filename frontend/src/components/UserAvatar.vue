<template>
  <div
    class="w-8 h-8 rounded-full bg-white/20 dark:bg-gray-700 flex items-center justify-center font-bold text-xs text-white dark:text-gray-300 cursor-pointer overflow-hidden hover:ring-2 hover:ring-white/50 transition-all"
    :title="user?.username"
  >
    <img v-if="user?.avatar_url" :src="user.avatar_url" :alt="user.username" class="w-full h-full object-cover" />
    <span v-else>{{ user?.username?.charAt(0).toUpperCase() }}</span>
  </div>
</template>

<script setup>
defineProps(['user'])
</script>
