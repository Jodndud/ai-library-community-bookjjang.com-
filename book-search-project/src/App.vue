<template>
  <header v-if="showHeader">
    <div class="container">
      <div class="logo-search-bar">
        <div class="logo" @click="goHome">
          <h1>책쨩닷컴</h1>
        </div>
        <SearchBar v-if="route.path !== '/'" />
      </div>
      <nav class="navbar">
        <form class="logout-btn">
          <input type="submit" value="로그아웃">
        </form>
        <RouterLink :to="{ name: 'login' }">로그인</RouterLink>
        <!-- <RouterLink>전체 도서</RouterLink> -->
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<script setup>
import SearchBar from '@/components/SearchBar.vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const router = useRouter()

const goHome = function () {
  router.push({ name: 'home' })
}

const noLayoutRoutes = ['login', 'signup'] // 이름 기준 조건 분기

const showHeader = computed(() => {
  return route.name && !noLayoutRoutes.includes(route.name)
})
</script>

<style scoped>
/* 헤더 전체 */
header {
  width: 100%;
  height: 80px;
  border-bottom: 1px solid #eee;
}

header .container {
  height: 100%;
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
  gap: 20px;
}

.navbar>a:hover {
  color: #FF5F0E;
}
</style>
