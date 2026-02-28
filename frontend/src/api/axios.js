import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:5001/api',
    withCredentials: true  // sends cookies with every request
})

// Auto-refresh token on 401
api.interceptors.response.use(
    response => response,
    async error => {
        if (error.response?.status === 401 && !error.config._retry) {
            error.config._retry = true
            try {
                await axios.post('http://localhost:5001/api/auth/refresh', {}, { withCredentials: true })
                return api(error.config)
            } catch {
                window.location.href = '/login'
            }
        }
        return Promise.reject(error)
    }
)

export default api
