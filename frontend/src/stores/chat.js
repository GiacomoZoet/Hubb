import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'
import { io } from 'socket.io-client'
import { getMessages } from '@/api/messages'
import { useDMStore } from '@/stores/dm'

export const useChatStore = defineStore('chat', () => {
    const messages = ref([])
    const typingUsers = ref([])
    const socket = shallowRef(null)
    const deletedWorkspaceId = ref(null)
    const newInvitation = ref(null)

    function connectSocket() {
        if (socket.value) return

        socket.value = io(import.meta.env.VITE_API_URL || '/', {
            withCredentials: true,
            transports: ['websocket'],
        })

        socket.value.on('connect', () => {
            const token = localStorage.getItem('access_token')
            if (token) socket.value.emit('join_user_room', { token })
        })

        socket.value.on('new_message', (msg) => {
            messages.value = [...messages.value, msg]
        })

        socket.value.on('new_dm', (dm) => {
            const dmStore = useDMStore()
            if (dmStore.activeUser?.id === dm.sender_id) {
                dmStore.activeConversation.push(dm)
            } else {
                const contact = dmStore.inbox.find(c => c.id === dm.sender_id)
                if (contact) {
                    contact.unread_count = (contact.unread_count || 0) + 1
                } else {
                    dmStore.inbox.push({ id: dm.sender_id, username: dm.sender_username, unread_count: 1 })
                }
            }
        })

        socket.value.on('workspace_deleted', (data) => {
            deletedWorkspaceId.value = data.workspace_id
        })

        socket.value.on('new_invitation', (data) => {
            newInvitation.value = data
        })

        socket.value.on('user_typing', (data) => {
            if (!typingUsers.value.includes(data.username)) {
                typingUsers.value.push(data.username)
                setTimeout(() => {
                    typingUsers.value = typingUsers.value.filter(u => u !== data.username)
                }, 2000)
            }
        })
    }


    function joinWorkspace(workspaceId) {
        socket.value?.emit('join_workspace_room', { workspace_id: workspaceId })
    }

    function joinChannel(channelId) {
        socket.value?.emit('join_room', { channel_id: channelId })
    }

    function leaveChannel(channelId) {
        socket.value?.emit('leave_room', { channel_id: channelId })
    }

    function sendTyping(channelId) {
        socket.value?.emit('typing', { channel_id: channelId })
    }

    async function loadMessages(channelId) {
        const res = await getMessages(channelId)
        messages.value = [...res.data.messages].reverse()
    }



    return { messages, typingUsers, socket, deletedWorkspaceId, newInvitation, connectSocket, joinWorkspace, joinChannel, leaveChannel, sendTyping, loadMessages }
})
