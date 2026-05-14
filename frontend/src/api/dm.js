import api from './axios'

export const sendDM        = (receiverId, data) => api.post(`/dm/${receiverId}`, data)
export const getConversation = (userId)         => api.get(`/dm/${userId}`)
export const getInbox      = ()                 => api.get('/dm/')
