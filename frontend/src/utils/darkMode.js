export function initDarkMode() {
  const saved = localStorage.getItem('theme')
  document.documentElement.classList.toggle('dark', saved === 'dark')
}

export function toggleDarkMode() {
  const isDark = document.documentElement.classList.toggle('dark')
  localStorage.setItem('theme', isDark ? 'dark' : 'light')
}
