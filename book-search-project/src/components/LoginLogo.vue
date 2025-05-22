<template>
  <div class="home-logo">

    <RouterLink :to="{ name: 'home' }">
      <div class="logo">
        <h1>책쨩닷컴</h1>
      </div>
    </RouterLink>
    <!-- <p>설명설명설명</p> -->
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.home-logo {
  margin: 0 auto 40px;
  text-align: center;
}

.logo h1 {
  width: 100%;
  text-align: center;
}
</style>