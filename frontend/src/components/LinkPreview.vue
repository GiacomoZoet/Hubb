<template>
  <a
    v-if="og.title || og.image"
    :href="url"
    target="_blank"
    rel="noopener noreferrer"
    class="mt-1.5 flex gap-3 rounded-lg border border-teal-border dark:border-gray-600 bg-white dark:bg-gray-800 overflow-hidden hover:bg-teal-lighter/60 dark:hover:bg-gray-700 transition-colors no-underline"
  >
    <img
      v-if="og.image"
      :src="og.image"
      class="w-20 h-20 object-cover shrink-0"
      @error="og.image = ''"
    />
    <div class="flex flex-col justify-center gap-0.5 py-2 pr-3 min-w-0" :class="og.image ? '' : 'pl-3'">
      <span class="text-xs font-semibold text-gray-900 dark:text-gray-100 truncate">{{ og.title }}</span>
      <span v-if="og.description" class="text-[11px] text-gray-500 dark:text-gray-400 line-clamp-2 leading-snug">{{ og.description }}</span>
      <span class="text-[10px] text-teal-primary truncate">{{ domain }}</span>
    </div>
  </a>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/api/axios'

const props = defineProps(['url'])
const og = ref({ title: '', description: '', image: '', url: '' })

const domain = computed(() => {
  try { return new URL(props.url).hostname } catch { return props.url }
})

onMounted(async () => {
  try {
    const res = await api.get(`/og?url=${encodeURIComponent(props.url)}`)
    og.value = res.data
  } catch {
    // silently skip
  }
})
</script>
