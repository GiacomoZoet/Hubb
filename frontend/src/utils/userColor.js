const COLORS = [
  'bg-violet-500',
  'bg-blue-500',
  'bg-emerald-600',
  'bg-orange-500',
  'bg-pink-500',
  'bg-indigo-500',
  'bg-rose-500',
  'bg-amber-600',
]

function hash(str) {
  let h = 0
  for (let i = 0; i < str.length; i++) {
    h = (h * 31 + str.charCodeAt(i)) & 0xffffffff
  }
  return Math.abs(h)
}

export function userColor(username) {
  if (!username) return COLORS[0]
  return COLORS[hash(username) % COLORS.length]
}
