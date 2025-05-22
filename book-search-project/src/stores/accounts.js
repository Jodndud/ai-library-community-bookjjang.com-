// store/accounts.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const isLogin = computed(() => {
    return token.value ? true : false
  })
  const router = useRouter()

  // payload를 FormData로 만들어 보내도록 변경
  const signUp = function(formData) {
    const username = formData.get('username')
    const password = formData.get('password1')

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    .then((res) => {
      console.log('회원가입 완료')
      // 가입 후 로그인
      logIn({ username, password })
    })
    .catch((err) => {
      console.error('회원가입 실패:', err.response?.data || err.message)
    })
  }

  const logIn = function ({ username, password }) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: { username, password },
      headers: { 'Content-Type': 'application/json' }
    })
      .then((res) => {
        console.log('로그인 완료')
        token.value = res.data.key
        router.push({ name: 'home' })
      })
      .catch((err) => {
        console.error('로그인 실패:', err.response?.data || err.message)
        alert('아이디 또는 비밀번호가 잘못되었습니다.')
      })
  }


  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`
    })
      .then(() => {
        token.value = null
        alert('로그아웃 되었습니다.')
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.error('로그아웃 실패:', err.response?.data || err.message)
      })
  }

  return {
    token, isLogin,
    signUp, logIn, logOut
  }
}, { persist: true })