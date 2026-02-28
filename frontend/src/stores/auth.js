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
            await authApi.login(credentials)
            await this.fetchUser()
        },
        async logout() {
            await authApi.logout()
            this.user = null
        }
    }
})
