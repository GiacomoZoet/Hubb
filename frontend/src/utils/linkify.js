const URL_RE = /https?:\/\/[^\s<>"']+/g

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

export function linkify(text) {
  if (!text) return ''
  const escaped = escapeHtml(text)
  return escaped.replace(URL_RE, url => {
    return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="text-teal-primary underline break-all">${url}</a>`
  })
}

export function extractUrls(text) {
  if (!text) return []
  return [...new Set(text.match(URL_RE) || [])]
}
