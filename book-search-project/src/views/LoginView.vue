<template>
    <div class="login-form">
        <form @submit.prevent="login">
            <div class="input-wrap">
                <input type="text" placeholder="아이디를 입력해 주세요." v-model="id">
                <input type="password" placeholder="비밀번호를 입력해 주세요." v-model="password">
            </div>

            <input class="login-page-btn" type="submit" value="로그인">
        </form>
    </div>

    <RouterLink class="login-page-btn signup-btn" :to="{ name: 'signup' }">회원가입</RouterLink>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'

const accountStore = useAccountStore()
const id = ref('')
const password = ref('')

const login = () => {
    const payload = {
        username: username.value,
        password: password.value
    }
    accountStore.logIn(payload)
}
</script>

<style scoped>
.login-form>form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
}

.login-form>form input:first-child {
    border-bottom: 1px solid #ccc;
}

.login-form>form input:first-child:focus {
    border-bottom: 1px solid #ccc;
}

.login-form>form input {
    width: 100%;
    padding: 16px 12px;
    border: unset;
    font-size: 16px;
}

.login-form>form input:focus {
    border: none;
    outline: none;
}

.input-wrap {
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
}

.login-page-btn {
    cursor: pointer;
    border-radius: 8px;
    background: #666;
    color: #fff;
    font-size: 16px;
}

.signup-btn {
    display: block;
    width: 100%;
    margin-top: 10px;
    padding: 16px 12px;
    text-align: center;
    border: 1px solid #666;
    background: unset;
    color: #666;
    font-weight: 600;
    transition: all .4s;
}

.signup-btn:hover {
    background: #eee;
}
</style>