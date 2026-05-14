<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1>iMessageU</h1>
      <h2>Create your workspace</h2>
      <form @submit.prevent="handleCreate">
        <div class="field">
          <label>Workspace Name</label>
          <input v-model="name" type="text" placeholder="My Team" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create Workspace' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createWorkspace } from '@/api/workspaces'

const router = useRouter()
const name = ref('')
const error = ref('')
const loading = ref(false)

async function handleCreate() {
  loading.value = true
  error.value = ''
  try {
    const res = await createWorkspace({ name: name.value })
    router.push(`/workspace/${res.data.workspace.slug}`)
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to create workspace'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex; justify-content: center; align-items: center;
  height: 100vh; background: #1a1a2e;
}
.auth-box {
  background: #16213e; padding: 2.5rem; border-radius: 12px;
  width: 400px; color: white;
}
h1 { font-size: 1.8rem; margin-bottom: 0.25rem; }
h2 { font-size: 1rem; font-weight: 400; color: #aaa; margin-bottom: 2rem; }
.field { margin-bottom: 1.2rem; }
label { display: block; font-size: 0.85rem; margin-bottom: 0.4rem; color: #ccc; }
input {
  width: 100%; padding: 0.7rem 1rem; border-radius: 8px;
  border: 1px solid #333; background: #0f3460; color: white;
  font-size: 0.95rem; box-sizing: border-box;
}
button {
  width: 100%; padding: 0.75rem; background: #e94560; color: white;
  border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 0.5rem;
}
button:disabled { opacity: 0.6; cursor: not-allowed; }
.error { color: #e94560; font-size: 0.85rem; margin-bottom: 0.5rem; }
</style>
