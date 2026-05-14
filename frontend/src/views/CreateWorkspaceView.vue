<template>
  <div class="min-h-screen flex items-center justify-center bg-teal-lighter dark:bg-gray-900">
    <div class="bg-white dark:bg-gray-800 rounded-2xl px-6 py-8 md:px-10 md:py-10 w-full max-w-[400px] mx-4 md:mx-auto shadow-sm border border-teal-border dark:border-gray-700">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">hubb</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-8">Create your huub</p>
      <form @submit.prevent="handleCreate">
        <div class="mb-5">
          <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">huub Name</label>
          <input
            v-model="name"
            type="text"
            placeholder="My Team"
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

