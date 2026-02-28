<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1>iMessageU</h1>
      <h2>Sign in to your workspace</h2>
      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="you@example.com" required />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <p class="switch">Don't have an account? <RouterLink to="/register">Register</RouterLink></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { listWorkspaces } from '@/api/workspaces'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({ email: '', password: '' })
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(form.value)
    const res = await listWorkspaces()
    if (res.data.length > 0) {
      router.push(`/workspace/${res.data[0].slug}`)
    } else {
      router.push('/create-workspace')
    }
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #1a1a2e;
}
.auth-box {
  background: #16213e;
  padding: 2.5rem;
  border-radius: 12px;
  width: 400px;
  color: white;
}
h1 { font-size: 1.8rem; margin-bottom: 0.25rem; }
h2 { font-size: 1rem; font-weight: 400; color: #aaa; margin-bottom: 2rem; }
.field { margin-bottom: 1.2rem; }
label { display: block; font-size: 0.85rem; margin-bottom: 0.4rem; color: #ccc; }
input {
  width: 100%;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  border: 1px solid #333;
  background: #0f3460;
  color: white;
  font-size: 0.95rem;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 0.75rem;
  background: #e94560;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 0.5rem;
}
button:disabled { opacity: 0.6; cursor: not-allowed; }
.error { color: #e94560; font-size: 0.85rem; margin-bottom: 0.5rem; }
.switch { text-align: center; margin-top: 1.5rem; color: #aaa; font-size: 0.9rem; }
.switch a { color: #e94560; }
</style>
