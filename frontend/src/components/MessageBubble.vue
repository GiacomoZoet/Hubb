<template>
  <div class="message-bubble">
    <div class="avatar-placeholder">{{ message.username?.charAt(0).toUpperCase() || '?' }}</div>
    <div class="content">
      <div class="meta">
        <span class="username">{{ message.username }}</span>
        <span class="time">{{ formatTime(message.created_at) }}</span>
        <span v-if="message.is_edited" class="edited">(edited)</span>
      </div>
      <p class="text">{{ message.content }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps(['message'])

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.message-bubble {
  display: flex; gap: 0.75rem; padding: 0.4rem 0;
}
.message-bubble:hover { background: rgba(255,255,255,0.03); border-radius: 8px; }
.avatar-placeholder {
  width: 36px; height: 36px; border-radius: 50%; background: #e94560;
  display: flex; align-items: center; justify-content: center;
  font-weight: bold; flex-shrink: 0;
}
.content { display: flex; flex-direction: column; }
.meta { display: flex; align-items: baseline; gap: 0.5rem; }
.username { font-weight: bold; font-size: 0.95rem; }
.time { font-size: 0.75rem; color: #888; }
.edited { font-size: 0.75rem; color: #888; }
.text { margin: 0.15rem 0 0; color: #ddd; line-height: 1.5; }
</style>
