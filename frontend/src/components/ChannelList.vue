<template>
  <div class="channel-list">
    <div class="workspace-name">{{ activeChannel?.name || 'Channels' }}</div>
    <div class="section-label">CHANNELS</div>
    <div
        v-for="ch in channels"
        :key="ch.id"
        class="channel-item"
        :class="{ active: activeChannel?.id === ch.id }"
        @click="$emit('selectChannel', ch)"
    >
      <span class="hash">{{ ch.is_private ? '🔒' : '#' }}</span>
      {{ ch.name }}
    </div>
    <div class="add-channel" @click="showModal = true">+ Add Channel</div>

    <!-- Add Channel Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h3>New Channel</h3>
        <input v-model="newChannelName" placeholder="channel-name" />
        <label><input type="checkbox" v-model="isPrivate" /> Private</label>
        <div class="modal-actions">
          <button @click="showModal = false">Cancel</button>
          <button class="primary" @click="createNewChannel">Create</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createChannel } from '@/api/workspaces'

const props = defineProps(['channels', 'activeChannel', 'workspaceId'])
defineEmits(['selectChannel'])

const showModal = ref(false)
const newChannelName = ref('')
const isPrivate = ref(false)

async function createNewChannel() {
  if (!newChannelName.value.trim()) return
  await createChannel(props.workspaceId, {
    name: newChannelName.value.trim(),
    is_private: isPrivate.value
  })
  showModal.value = false
  newChannelName.value = ''
  // Reload channels — parent will handle via emit if needed
  window.location.reload()
}
</script>

<style scoped>
.channel-list {
  width: 220px; background: #16213e;
  padding: 1rem 0; display: flex; flex-direction: column;
}
.workspace-name {
  font-weight: bold; padding: 0 1rem 1rem; font-size: 1rem;
  border-bottom: 1px solid #222;
}
.section-label {
  font-size: 0.7rem; color: #888; padding: 1rem 1rem 0.5rem;
  letter-spacing: 0.08em;
}
.channel-item {
  padding: 0.4rem 1rem; cursor: pointer; border-radius: 6px;
  margin: 0 0.5rem; display: flex; align-items: center; gap: 0.4rem;
  font-size: 0.95rem; color: #ccc;
}
.channel-item:hover { background: #1a2a4a; color: white; }
.channel-item.active { background: #0f3460; color: white; }
.hash { color: #888; }
.add-channel {
  padding: 0.4rem 1rem; margin: 0.5rem; color: #888;
  cursor: pointer; font-size: 0.9rem; border-radius: 6px;
}
.add-channel:hover { background: #1a2a4a; color: white; }
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.6);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal {
  background: #16213e; padding: 2rem; border-radius: 12px;
  width: 320px; color: white; display: flex; flex-direction: column; gap: 1rem;
}
.modal input[type="text"], .modal input:not([type="checkbox"]) {
  padding: 0.6rem; border-radius: 8px; border: 1px solid #333;
  background: #0f3460; color: white; font-size: 0.95rem; width: 100%;
  box-sizing: border-box;
}
.modal-actions { display: flex; gap: 0.5rem; justify-content: flex-end; }
.modal-actions button {
  padding: 0.5rem 1rem; border-radius: 8px; border: none; cursor: pointer;
  background: #333; color: white;
}
.modal-actions .primary { background: #e94560; }
</style>
