<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-teal-lighter dark:bg-gray-900 gap-6">
    <div class="bg-white dark:bg-gray-800 rounded-2xl px-6 py-8 md:px-10 md:py-10 w-full max-w-[400px] mx-4 md:mx-auto shadow-sm border border-teal-border dark:border-gray-700">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">hubb</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-8">Choose a new password</p>
      <form @submit.prevent="handleSubmit">
        <div class="mb-5">
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">New password</label>
          <div class="relative">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
              required
              class="w-full px-4 py-2.5 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary pr-10"
            />
            <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xs">
              {{ showPassword ? 'Hide' : 'Show' }}
            </button>
          </div>
        </div>
        <p v-if="error" class="text-red-500 text-xs mb-3">{{ error }}</p>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3 bg-teal-primary text-white rounded-lg font-semibold text-sm hover:bg-teal-dark transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Updating...' : 'Update password' }}
        </button>
      </form>
    </div>
    <p class="text-xs text-gray-400 dark:text-gray-600">Giacomo Zoet</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    await api.post(`/auth/reset-password/${route.params.token}`, { password: password.value })
    router.push('/login')
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>
