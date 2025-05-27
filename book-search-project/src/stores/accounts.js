import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const token = ref(null)
  const isLogin = computed(() => !!token.value)
  const router = useRouter()

  const userInfo = ref(null)  // 유저 정보는 객체로 관리하는 게 편함

  // 현재 로그인한 유저 이름 쉽게 가져오기
  const username = computed(() => userInfo.value?.username || '')

  const signUp = function (formData) {
    const username = formData.get('username')
    const password = formData.get('password1')

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then(() => {
        console.log('회원가입 완료')
        logIn({ username, password })  // 회원가입 후 바로 로그인
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
        myPage()  // 로그인 성공하면 내 정보 가져오기 호출
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
        userInfo.value = null
        console.log('로그아웃 되었습니다.')
        alert('로그아웃 되었습니다.')
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const myPage = function () {
    if (!token.value) return

    axios({
      method: 'get',
      url: `${API_URL}/accounts/mypage/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((res) => {
        userInfo.value = res.data
        console.log('내 정보:', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {
    token, isLogin, userInfo, username,
    signUp, logIn, logOut, myPage
  }
}, { persist: true })
