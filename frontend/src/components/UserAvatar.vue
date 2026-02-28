<template>
  <div class="avatar" :title="user?.username">
    <img v-if="user?.avatar_url" :src="user.avatar_url" :alt="user.username" />
    <span v-else>{{ user?.username?.charAt(0).toUpperCase() }}</span>
  </div>
</template>

<script setup>
defineProps(['user'])
</script>

<style scoped>
.avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: #e94560; display: flex; align-items: center;
  justify-content: center; font-weight: bold; cursor: pointer;
  overflow: hidden;
}
.avatar img { width: 100%; height: 100%; object-fit: cover; }
</style>
