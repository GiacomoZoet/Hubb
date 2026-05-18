import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getInbox, getConversation, sendDM } from '@/api/dm'

export const useDMStore = defineStore('dm', () => {
    const inbox = ref([])
    const activeConversation = ref([])
    const activeUser = ref(null)

    async function loadInbox() {
        const res = await getInbox()
        inbox.value = res.data
    }

    async function loadConversation(userId) {
        const res = await getConversation(userId)
        activeConversation.value = [...res.data.messages].reverse()
        const contact = inbox.value.find(c => c.id === userId)
        if (contact) contact.unread_count = 0
    }

    async function send(receiverId, content) {
        const res = await sendDM(receiverId, { content })
        activeConversation.value.push(res.data.data)
    }

    return { inbox, activeConversation, activeUser, loadInbox, loadConversation, send }
})
