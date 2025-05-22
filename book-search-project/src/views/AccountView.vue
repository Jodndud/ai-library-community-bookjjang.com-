<template>
    <div class="container">
        <div class="account-wrap">
            <LoginLogo />
            <RouterView />
        </div>
    </div>
</template>

<script setup>
import LoginLogo from '@/components/LoginLogo.vue'
import { RouterView } from 'vue-router'

</script>

<style scoped>
.account-wrap {
    width: 400px;
    margin: 200px auto 0;
}
</style>