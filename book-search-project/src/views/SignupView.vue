<template>
    <div class="signup-form">
        <form @submit.prevent="signUp">
            <div>
                <label for="userId">아이디: </label>
                <input type="text" id="userId">
            </div>
            <div>
                <label for="password1">비밀번호: </label>
                <input type="password" id="password1">
            </div>
            <div>
                <label for="password2">비밀번호 확인: </label>
                <input type="password" id="password2">
            </div>
            <div>
                <label for="password2">닉네임: </label>
                <input type="password" id="password2">
            </div>
            <div>
                <label for="">나이 : </label>
                <input type="" id="">
            </div>
            <div>
                <label for="">연간 독서량 : </label>
                <input type="" id="">
            </div>
            <div>
                <label for="">프로필 이미지: </label>
                <input type="" id="">
            </div>
            <div>
                <label for="">좋아하는 장르: </label>
                <input type="" id="">
            </div>

            <input class="signup-btn" type="submit" value="회원가입">
        </form>
    </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts'
import { ref } from 'vue'

const username = ref('')
const password1 = ref('')
const password2 = ref('')

const accountStore = useAccountStore()
const signUp = function () {
    const payload = {
        username: username.value,
        password1: password1.value,
        password2: password2.value,
    }
    accountStore.signUp(payload)
}
</script>

<style scoped></style>