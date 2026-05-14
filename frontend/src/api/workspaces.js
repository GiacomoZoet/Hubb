import api from './axios'

export const createWorkspace  = (data)                  => api.post('/workspaces/', data)
export const listWorkspaces   = ()                       => api.get('/workspaces/')
export const getWorkspace     = (slug)                   => api.get(`/workspaces/${slug}`)
export const inviteMember     = (workspaceId, data)      => api.post(`/workspaces/${workspaceId}/members`, data)
export const listMembers      = (workspaceId)            => api.get(`/workspaces/${workspaceId}/members`)
export const listChannels  = (workspaceId)       => api.get(`/channels/${workspaceId}/channels`)
export const createChannel = (workspaceId, data)  => api.post(`/channels/${workspaceId}/channels`, data)
export const addChannelMember = (channelId, data)        => api.post(`/channels/channel/${channelId}/members`, data)
