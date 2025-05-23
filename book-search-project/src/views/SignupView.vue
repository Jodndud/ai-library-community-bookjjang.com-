<template>
  <div class="signup-form">
    <form @submit.prevent="signUp">
      <div>
        <label for="username">아이디: </label>
        <input type="text" required id="username" v-model="username" />
      </div>
      <div>
        <label for="password1">비밀번호: </label>
        <input type="password" required id="password1" v-model="password1" />
      </div>
      <div>
        <label for="password2">비밀번호 확인: </label>
        <input type="password" required id="password2" v-model="password2" />
      </div>
      <div>
        <label for="nickname">닉네임: </label>
        <input type="text" required id="nickname" v-model="nickname" />
      </div>
      <div>
        <label for="age">나이: </label>
        <input type="number" id="age" v-model.number="age" />
      </div>
      <div>
        <label for="yearlyReadingAmount">연간 독서량: </label>
        <input type="number" id="yearlyReadingAmount" v-model.number="yearlyReadingAmount" />
      </div>
      <div>
        <label for="profileImage">프로필 이미지: </label>
        <input type="file" id="profileImage" @change="onFileChange" />
      </div>
      <div>
        <label>좋아하는 장르: </label>
        <div v-for="genre in genreOptions" :key="genre">
            <input
            type="checkbox"
            :id="genre"
            :value="genre"
            v-model="selectedGenres"
            />
            <label :for="genre">{{ genre }}</label>
        </div>
      </div>

      <input class="signup-btn" type="submit" value="회원가입" />
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const nickname = ref('')
const age = ref(null)
const yearlyReadingAmount = ref(null)
const favoriteGenres = ref('')
const profileImage = ref(null)
const genreOptions = ['소설', '에세이', 'SF', '역사', '자기계발', '시', '추리', '만화']
const selectedGenres = ref([])

const accountStore = useAccountStore()

function onFileChange(event) {
  const file = event.target.files[0]
  profileImage.value = file
}

const signUp = () => {
  const formData = new FormData()
  formData.append('username', username.value)
  formData.append('password1', password1.value)
  formData.append('password2', password2.value)
  formData.append('nickname', nickname.value)
  if (age.value !== null) formData.append('age', age.value)
  if (yearlyReadingAmount.value !== null) formData.append('yearly_reading_amount', yearlyReadingAmount.value)
  if (profileImage.value) formData.append('profile_image', profileImage.value)
  formData.append('favorite_genres', selectedGenres.value.join(','))  // 변경된 부분

  accountStore.signUp(formData)
}
</script>