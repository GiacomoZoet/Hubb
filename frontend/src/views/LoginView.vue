<template>
  <div class="min-h-screen flex items-center justify-center bg-teal-lighter dark:bg-gray-900">
    <div class="bg-white dark:bg-gray-800 rounded-2xl px-10 py-10 w-[400px] shadow-sm border border-teal-border dark:border-gray-700">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">iMessageU</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-8">Sign in to your workspace</p>
      <form @submit.prevent="handleLogin">
        <div class="mb-5">
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">Email</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="you@example.com"
            required
            class="w-full px-4 py-2.5 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary"
          />
        </div>
        <div class="mb-5">
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">Password</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="••••••••"
            required
            class="w-full px-4 py-2.5 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary"
          />
        </div>
        <p v-if="error" class="text-red-500 text-xs mb-3">{{ error }}</p>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 bg-teal-primary text-white rounded-lg font-semibold text-sm hover:bg-teal-dark transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <p class="text-center mt-6 text-gray-400 dark:text-gray-500 text-sm">
        Don't have an account?
        <RouterLink to="/register" class="text-teal-primary hover:underline">Register</RouterLink>
      </p>
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

