<template>
  <div class="min-h-screen bg-teal-lighter dark:bg-gray-900 flex flex-col">
    <nav class="sticky top-0 z-10 bg-white dark:bg-gray-800 border-b border-teal-border dark:border-gray-700 px-4 md:px-12 h-[60px] flex items-center justify-between">
      <span class="text-lg font-bold text-teal-text dark:text-gray-100">hubb</span>
      <div class="flex gap-3 items-center">
        <RouterLink
          to="/login"
          class="px-4 py-2 border border-teal-primary text-teal-primary rounded-lg text-sm font-medium hover:bg-teal-light transition-colors"
        >Sign In</RouterLink>
        <RouterLink
          to="/register"
          class="px-4 py-2 bg-teal-primary text-white rounded-lg text-sm font-semibold hover:bg-teal-dark transition-colors"
        >Get Started</RouterLink>
      </div>
    </nav>

    <section class="flex-1 max-w-[1100px] mx-auto w-full px-4 py-10 md:px-12 md:py-20 grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 items-center">
      <div>
        <p class="text-xs font-semibold uppercase tracking-widest text-teal-primary mb-4">Real-time messaging</p>
        <h1 class="text-5xl font-bold leading-tight text-teal-text dark:text-gray-100 mb-5">
          Fast chat.<br><span class="text-teal-primary">Zero bloat.</span>
        </h1>
        <p class="text-base text-teal-muted dark:text-gray-400 leading-relaxed mb-9 max-w-md">
          huubs, channels, and direct messages — everything your team needs, and nothing it doesn't.
        </p>
        <div class="flex gap-4 items-center">
          <RouterLink
            to="/register"
            class="px-7 py-3 bg-teal-primary text-white rounded-xl text-sm font-semibold hover:bg-teal-dark transition-colors"
          >Get Started →</RouterLink>
          <RouterLink to="/login" class="text-sm text-teal-primary font-medium hover:underline">
            Already have an account? Sign in
          </RouterLink>
        </div>
      </div>

      <div class="rounded-2xl border border-teal-border shadow-lg overflow-hidden bg-white dark:bg-gray-800">
        <div class="bg-teal-primary px-4 py-3 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-white/40"></span>
          <span class="w-2 h-2 rounded-full bg-white/40"></span>
          <span class="w-2 h-2 rounded-full bg-white/40"></span>
          <span class="ml-1 text-white text-xs font-semibold">University Squad</span>
        </div>
        <div class="flex h-64">
          <div class="w-40 bg-teal-dark flex-shrink-0 px-3 py-3">
            <p class="text-[10px] font-semibold uppercase tracking-wider text-white/50 mb-2">Channels</p>
            <div class="text-xs text-white/90 bg-white/15 rounded px-2 py-1 mb-1"># general</div>
            <div class="text-xs text-white/60 px-2 py-1 mb-1"># project</div>
            <div class="text-xs text-white/60 px-2 py-1 mb-3"># random</div>
            <p class="text-[10px] font-semibold uppercase tracking-wider text-white/50 mb-2">Direct</p>
            <div class="text-xs text-white/60 px-2 py-1 mb-1">Alex</div>
            <div class="text-xs text-white/60 px-2 py-1">Marco</div>
          </div>
          <div class="flex-1 flex flex-col p-3 gap-3">
            <p class="text-xs font-semibold text-teal-text dark:text-gray-300 border-b border-teal-light dark:border-gray-700 pb-2"># general</p>
            <div class="flex gap-2">
              <div class="w-6 h-6 rounded-full bg-teal-light flex-shrink-0 flex items-center justify-center text-[10px] font-bold text-teal-primary">A</div>
              <div>
                <p class="text-[10px] font-semibold text-teal-text dark:text-gray-300 mb-1">Alex</p>
                <p class="text-[11px] text-gray-600 dark:text-gray-400 bg-teal-lighter dark:bg-gray-700 px-2 py-1 rounded-lg rounded-tl-none inline-block">Hey, anyone up for a study session?</p>
              </div>
            </div>
            <div class="flex gap-2">
              <div class="w-6 h-6 rounded-full bg-teal-light flex-shrink-0 flex items-center justify-center text-[10px] font-bold text-teal-primary">M</div>
              <div>
                <p class="text-[10px] font-semibold text-teal-text dark:text-gray-300 mb-1">Marco</p>
                <p class="text-[11px] text-gray-600 dark:text-gray-400 bg-teal-lighter dark:bg-gray-700 px-2 py-1 rounded-lg rounded-tl-none inline-block">I'm in! Library at 4pm?</p>
              </div>
            </div>
            <div class="flex gap-2 justify-end">
              <p class="text-[11px] text-white bg-teal-primary px-2 py-1 rounded-lg rounded-tr-none inline-block">See you there 👍</p>
            </div>
          </div>
        </div>
        <div class="px-3 py-2 border-t border-teal-border dark:border-gray-700">
          <p class="text-xs text-gray-400 dark:text-gray-500">Type a message…</p>
        </div>
      </div>
    </section>

    <div class="bg-teal-primary text-white text-center text-sm font-medium py-4">
      ⚡ <strong class="font-bold">Lightweight by design</strong> — no unnecessary features, no distractions, just fast messaging.
    </div>

    <section class="bg-white dark:bg-gray-800 border-t border-teal-border dark:border-gray-700 py-8 md:py-12 px-4 md:px-12">
      <div class="max-w-[1100px] mx-auto">
        <h2 class="text-center text-xl font-bold text-teal-text dark:text-gray-100 mb-8">Everything you need. Nothing you don't.</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          <div v-for="f in features" :key="f.name" class="text-center border border-teal-border dark:border-gray-700 rounded-xl p-5 bg-teal-lighter dark:bg-gray-900">
            <div class="text-2xl mb-3">{{ f.icon }}</div>
            <h3 class="text-sm font-semibold text-teal-text dark:text-gray-200 mb-1">{{ f.name }}</h3>
            <p class="text-xs text-teal-muted dark:text-gray-400 leading-relaxed">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { listWorkspaces } from '@/api/workspaces'

const router = useRouter()
const authStore = useAuthStore()

const features = [
  { icon: '🏢', name: 'huubs',           desc: 'Create separate spaces for different teams or projects.' },
  { icon: '#',  name: 'Channels',        desc: 'Topic-based rooms to keep conversations organized.' },
  { icon: '💬', name: 'Direct Messages', desc: 'Private one-on-one chats with anyone in your huub.' },
  { icon: '⚡', name: 'Real-time',       desc: 'Messages delivered instantly via WebSockets, no polling.' },
]

onMounted(async () => {
  try {
    await authStore.fetchUser()
    const res = await listWorkspaces()
    if (res.data.length > 0) {
      router.push(`/workspace/${res.data[0].slug}`)
    } else {
      router.push('/create-workspace')
    }
  } catch {
    // unauthenticated — stay on landing page
  }
})
</script>
