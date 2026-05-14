<template>
  <div class="min-h-screen flex items-center justify-center bg-teal-lighter dark:bg-gray-900">
    <div class="bg-white dark:bg-gray-800 rounded-2xl px-6 py-8 md:px-10 md:py-10 w-full max-w-[400px] mx-4 md:mx-auto shadow-sm border border-teal-border dark:border-gray-700 text-center">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">hubb</h1>
      <p v-if="loading" class="text-sm text-gray-500 dark:text-gray-400">Confirming your email...</p>
      <div v-else-if="success">
        <p class="text-sm text-teal-primary font-semibold mb-2">Email confirmed!</p>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">Your account is ready. You can now sign in.</p>
        <RouterLink to="/login" class="px-6 py-2.5 bg-teal-primary text-white rounded-lg text-sm font-semibold hover:bg-teal-dark transition-colors">Sign In</RouterLink>
      </div>
      <div v-else>
        <p class="text-sm text-red-500 mb-4">{{ error }}</p>
        <RouterLink to="/login" class="text-sm text-teal-primary hover:underline">Back to sign in</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const loading = ref(true)
const success = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    await api.get(`/auth/confirm/${route.params.token}`)
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong'
  } finally {
    loading.value = false
  }
})
</script>
