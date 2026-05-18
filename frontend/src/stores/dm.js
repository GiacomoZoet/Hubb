import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getInbox, getConversation, sendDM } from '@/api/dm'

export const useDMStore = defineStore('dm', () => {
    const inbox = ref([])
    const activeConversation = ref([])
    const activeUser = ref(null)

    const dmUnread = computed(() => inbox.value.reduce((sum, c) => sum + (c.unread_count || 0), 0))

    async function loadInbox() {
        const res = await getInbox()
        inbox.value = res.data
    }

    async function loadConversation(userId) {
        const res = await getConversation(userId)
        activeConversation.value = [...res.data.messages].reverse()
        const idx = inbox.value.findIndex(c => c.id === userId)
        if (idx !== -1) inbox.value.splice(idx, 1, { ...inbox.value[idx], unread_count: 0 })
    }

    function incrementUnread(senderId, senderUsername) {
        const idx = inbox.value.findIndex(c => c.id === senderId)
        if (idx !== -1) {
            inbox.value.splice(idx, 1, { ...inbox.value[idx], unread_count: (inbox.value[idx].unread_count || 0) + 1 })
        } else {
            inbox.value.push({ id: senderId, username: senderUsername, unread_count: 1 })
        }
    }

    async function send(receiverId, content) {
        const res = await sendDM(receiverId, { content })
        activeConversation.value.push(res.data.data)
    }

    return { inbox, activeConversation, activeUser, dmUnread, loadInbox, loadConversation, incrementUnread, send }
})
