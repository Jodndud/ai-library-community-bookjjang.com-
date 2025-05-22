import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'
import SearchingResultView from '@/views/SearchingResultView.vue'
import AccountView from '@/views/AccountView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainPageView
    },
    {
      path: '/searchresult/:value',
      name: 'searchresult',
      component: SearchingResultView
    },
    {
      path: '/login',
      component: AccountView,
      children: [
        {
          path: '',
          name: 'login',
          component: LoginView,
        }
      ]
    },
    {
      path: '/signup',
      component: AccountView,
      children: [
        {
          path: '',
          name: 'signup',
          component: SignupView,
        }
      ]
    }
  ],
})

export default router
