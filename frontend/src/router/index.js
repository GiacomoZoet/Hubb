import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView             from '@/views/HomeView.vue'
import LoginView           from '@/views/LoginView.vue'
import RegisterView         from '@/views/RegisterView.vue'
import WorkspaceView        from '@/views/WorkspaceView.vue'
import CreateWorkspaceView  from '@/views/CreateWorkspaceView.vue'

const routes = [
  { path: '/',                  component: HomeView },
  { path: '/login',             component: LoginView },
  { path: '/register',          component: RegisterView },
  { path: '/confirm/:token',    component: () => import('@/views/ConfirmView.vue') },
  { path: '/forgot-password',  component: () => import('@/views/ForgotPasswordView.vue') },
  { path: '/reset-password/:token', component: () => import('@/views/ResetPasswordView.vue') },
  { path: '/create-workspace',  component: CreateWorkspaceView, meta: { requiresAuth: true } },
  {
    path: '/workspace/:slug',
    component: WorkspaceView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  if (to.meta.requiresAuth) {
    const authStore = useAuthStore()
    if (!authStore.user) {
      try {
        await authStore.fetchUser()
      } catch {
        return '/login'
      }
    }
  }
})

export default router
