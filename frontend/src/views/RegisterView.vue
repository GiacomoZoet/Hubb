<template>
  <div class="min-h-screen flex items-center justify-center bg-teal-lighter dark:bg-gray-900">
    <div class="bg-white dark:bg-gray-800 rounded-2xl px-6 py-8 md:px-10 md:py-10 w-full max-w-[400px] mx-4 md:mx-auto shadow-sm border border-teal-border dark:border-gray-700">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">hubb</h1>

      <div v-if="registered">
        <p class="text-sm text-teal-primary font-semibold mt-4 mb-2">Check your email</p>
        <p class="text-sm text-gray-500 dark:text-gray-400">We sent a confirmation link to <strong>{{ registeredEmail }}</strong>. Click it to activate your account.</p>
        <p class="text-center mt-6 text-gray-400 dark:text-gray-500 text-sm">
          <RouterLink to="/login" class="text-teal-primary hover:underline">Back to sign in</RouterLink>
        </p>
      </div>

      <div v-else>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-8">Create a hubb account</p>
        <form @submit.prevent="handleRegister">
          <div class="mb-5">
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">Username</label>
            <input
              v-model="form.username"
              type="text"
              placeholder="giacomo"
              required
              class="w-full px-4 py-2.5 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary"
            />
          </div>

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
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">Confirm Email</label>
            <input
              v-model="form.emailConfirm"
              type="email"
              placeholder="you@example.com"
              required
              class="w-full px-4 py-2.5 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary"
            />
            <p v-if="form.emailConfirm && form.email !== form.emailConfirm" class="text-red-500 text-xs mt-1">Emails do not match</p>
          </div>

          <div class="mb-5">
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">Password</label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                required
                class="w-full px-4 py-2.5 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary pr-10"
              />
              <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xs">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <div v-if="form.password" class="mt-2 space-y-1">
              <p :class="pwChecks.length ? 'text-teal-primary' : 'text-gray-400'" class="text-xs flex items-center gap-1">
                <span>{{ pwChecks.length ? '✓' : '○' }}</span> At least 6 characters
              </p>
              <p :class="pwChecks.upper ? 'text-teal-primary' : 'text-gray-400'" class="text-xs flex items-center gap-1">
                <span>{{ pwChecks.upper ? '✓' : '○' }}</span> At least 1 uppercase letter
              </p>
              <p :class="pwChecks.special ? 'text-teal-primary' : 'text-gray-400'" class="text-xs flex items-center gap-1">
                <span>{{ pwChecks.special ? '✓' : '○' }}</span> At least 1 special character
              </p>
            </div>
          </div>

          <div class="mb-5">
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-300 mb-1.5">Confirm Password</label>
            <div class="relative">
              <input
                v-model="form.passwordConfirm"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                required
                class="w-full px-4 py-2.5 rounded-lg border border-teal-border dark:border-gray-600 bg-teal-lighter dark:bg-gray-900 text-gray-900 dark:text-gray-100 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-teal-primary pr-10"
              />
            </div>
            <p v-if="form.passwordConfirm && form.password !== form.passwordConfirm" class="text-red-500 text-xs mt-1">Passwords do not match</p>
          </div>

          <p v-if="error" class="text-red-500 text-xs mb-3">{{ error }}</p>
          <button
            type="submit"
            :disabled="loading || !canSubmit"
            class="w-full py-3 bg-teal-primary text-white rounded-lg font-semibold text-sm hover:bg-teal-dark transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {{ loading ? 'Creating account...' : 'Register' }}
          </button>
        </form>
        <p class="text-center mt-6 text-gray-400 dark:text-gray-500 text-sm">
          Already have an account?
          <RouterLink to="/login" class="text-teal-primary hover:underline">Sign in</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { register } from '@/api/auth'

const form = ref({ username: '', email: '', emailConfirm: '', password: '', passwordConfirm: '' })
const error = ref('')
const loading = ref(false)
const registered = ref(false)
const registeredEmail = ref('')
const showPassword = ref(false)

const pwChecks = computed(() => ({
  length: form.value.password.length >= 6,
  upper: /[A-Z]/.test(form.value.password),
  special: /[^A-Za-z0-9]/.test(form.value.password)
}))

const canSubmit = computed(() =>
  pwChecks.value.length &&
  pwChecks.value.upper &&
  pwChecks.value.special &&
  form.value.email === form.value.emailConfirm &&
  form.value.password === form.value.passwordConfirm
)

async function handleRegister() {
  if (form.value.email !== form.value.emailConfirm) {
    error.value = 'Emails do not match'
    return
  }
  if (form.value.password !== form.value.passwordConfirm) {
    error.value = 'Passwords do not match'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await register({ username: form.value.username, email: form.value.email, password: form.value.password })
    registeredEmail.value = form.value.email
    registered.value = true
  } catch (e) {
    error.value = e.response?.data?.error || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
