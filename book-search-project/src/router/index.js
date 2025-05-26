import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'
import SearchingResultView from '@/views/SearchingResultView.vue'
import AccountView from '@/views/AccountView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import MyPageView from '@/views/MyPageView.vue'
import BookList from '@/views/BookList.vue'
import ReviewView from '@/views/ReviewView.vue'
import BookDetailView from '@/views/BookDetailView.vue'
import ReviewDetailView from '@/views/ReviewDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainPageView
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
    },
    {
      path: '/books',
      name: 'books',
      component: BookList
    },
    {
      path: '/books/detail/:pk',
      name: 'bookDetail',
      component: BookDetailView
    },
    {
      path: '/books/:categoryId?',
      name: 'books',
      component: BookList,
    },
    {
      path: '/books/search/:value',
      name: 'booksResult',
      component: SearchingResultView
    },
    {
      path: '/mypage',
      component: MyPageView,
      children: [
        { path: '', name: 'mypage', component: MyPageView },
      ]
    },
    {
      path: '/review',
      name: 'review',
      component: ReviewView,
    },
    {
      path: '/review/:reviewId',
      name: 'reviewDetail',
      component: ReviewDetailView
    },
  ],
})

export default router
