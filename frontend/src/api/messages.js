import api from './axios'

export const getMessages   = (channelId, page = 1) => api.get(`/messages/${channelId}?page=${page}`)
export const sendMessage   = (channelId, data)     => api.post(`/messages/${channelId}`, data)
export const editMessage   = (channelId, msgId, data) => api.patch(`/messages/${channelId}/${msgId}`, data)
export const deleteMessage = (channelId, msgId)    => api.delete(`/messages/${channelId}/${msgId}`)
export const addReaction   = (channelId, msgId, data) => api.post(`/messages/${channelId}/${msgId}/reactions`, data)
export const searchMessages = (q, channelId)       => api.get(`/messages/search?q=${q}${channelId ? `&channel_id=${channelId}` : ''}`)
