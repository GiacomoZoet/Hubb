<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { initDarkMode } from '@/utils/darkMode'

onMounted(initDarkMode)
</script>

<template>
  <RouterView />
</template>
