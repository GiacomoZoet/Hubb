import { defineStore } from 'pinia'
import { getMe } from '@/api/auth'
import * as authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null
    }),
    actions: {
        async fetchUser() {
            const res = await getMe()
            this.user = res.data
        },
        async login(credentials) {
            const res = await authApi.login(credentials)
            localStorage.setItem('access_token', res.data.access_token)
            localStorage.setItem('refresh_token', res.data.refresh_token)
            this.user = res.data.user
        },
        async logout() {
            const refreshToken = localStorage.getItem('refresh_token')
            await authApi.logout({ refresh_token: refreshToken }).catch(() => {})
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            this.user = null
        }
    }
})
