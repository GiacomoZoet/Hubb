<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-teal-lighter dark:bg-gray-900 gap-6">
    <div class="bg-white dark:bg-gray-800 rounded-2xl px-6 py-8 md:px-10 md:py-10 w-full max-w-[400px] mx-4 md:mx-auto shadow-sm border border-teal-border dark:border-gray-700">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">hubb</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-8">Reset your password</p>
      <div v-if="sent">
        <p class="text-sm text-teal-primary font-semibold mb-2">Check your email</p>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">If that email is registered, you'll receive a reset link shortly.</p>
        <RouterLink to="/login" class="text-sm text-teal-primary hover:underline">Back to sign in</RouterLink>
      </div>
      <form v-else @submit.prevent="handleSubmit">
        <div class="mb-5">
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
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
          {{ loading ? 'Sending...' : 'Send reset link' }}
        </button>
      </form>
      <p v-if="!sent" class="text-center mt-6 text-gray-400 dark:text-gray-500 text-sm">
        <RouterLink to="/login" class="text-teal-primary hover:underline">Back to sign in</RouterLink>
      </p>
    </div>
    <p class="text-xs text-gray-400 dark:text-gray-600">Giacomo Zoet</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api/axios'

const email = ref('')
const loading = ref(false)
const error = ref('')
const sent = ref(false)

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    await api.post('/auth/forgot-password', { email: email.value })
    sent.value = true
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>
