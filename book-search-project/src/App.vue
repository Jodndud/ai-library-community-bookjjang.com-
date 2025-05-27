<template>
  <header v-if="showHeader">
    <div class="container">
      <div class="logo-search-bar">
        <div class="logo" @click="goHome">
          <h1>책짱닷컴</h1>
        </div>
        <SearchBar />
      </div>
      <nav class="navbar">
        <RouterLink :to="{ name: 'books' }" :class="{ active: route.name === 'books' }">전체도서</RouterLink>
        <RouterLink :to="{ name: 'review' }" :class="{ active: route.name === 'review' }">책쨩후기</RouterLink>
        <RouterLink :to="{ name: 'mypage' }" :class="{ active: route.name === 'mypage' }">마이페이지</RouterLink>
        <RouterLink v-if="accountStore.isLogin === false" :to="{ name: 'login' }">로그인</RouterLink>
        <form v-if="accountStore.isLogin === true" class="logout-btn" @submit.prevent="logOut">
          <input type="submit" value="로그아웃">
        </form>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<script setup>
import SearchBar from '@/components/SearchBar.vue'
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()

const route = useRoute()
const router = useRouter()

const goHome = function () {
  router.push({ name: 'home' })
}

const noLayoutRoutes = ['login', 'signup'] // 이름 기준 조건 분기

const showHeader = computed(() => {
  return route.name && !noLayoutRoutes.includes(route.name)
})

// 로그아웃
const logOut = function () {
  accountStore.logOut()
}
</script>

<style scoped>
/* 헤더 전체 */
header {
  width: 100%;
  height: 80px;
  background: #f6f6f6;
  border-bottom: 1px solid #eee;
}

header .container {
  height: 100%;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

header .logo-search-bar {
  display: flex;
  align-items: center;
  gap: 32px;
}

/* 로고 */
header .logo {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
}

/* 네이게이션 바 */
.navbar {
  display: flex;
  gap: 16px;
}

.navbar>a:hover {
  color: #2d7c4a;
  font-weight: bold;
}

.navbar>a.active {
  color: #2d7c4a;
  font-weight: bold;
}
</style>
