<template>
  <div class="signup-form">
    <form @submit.prevent="signUp">
      <div class="form-group">
        <input 
          type="text" 
          required 
          id="username" 
          v-model="username" 
          class="form-input"
          placeholder=" "
        />
        <label for="username">아이디를 입력해 주세요</label>
      </div>

      <div class="form-group">
        <input 
          type="password" 
          required 
          id="password1" 
          v-model="password1" 
          class="form-input"
          placeholder=" "
        />
        <label for="password1">비밀번호를 입력해 주세요</label>
      </div>

      <div class="form-group">
        <input 
          type="password" 
          required 
          id="password2" 
          v-model="password2" 
          class="form-input"
          placeholder=" "
        />
        <label for="password2">비밀번호 확인을 입력해 주세요</label>
      </div>

      <div class="form-group">
        <input 
          type="text" 
          required 
          id="nickname" 
          v-model="nickname" 
          class="form-input"
          placeholder=" "
        />
        <label for="nickname">닉네임을 입력해 주세요</label>
      </div>

      <div class="form-group">
        <input 
          type="number" 
          id="age" 
          v-model.number="age" 
          class="form-input"
          placeholder=" "
        />
        <label for="age">나이를 입력해 주세요</label>
      </div>

      <div class="form-group">
        <input 
          type="number" 
          id="yearlyReadingAmount" 
          v-model.number="yearlyReadingAmount" 
          class="form-input"
          placeholder=" "
        />
        <label for="yearlyReadingAmount">연간 독서량을 입력해 주세요</label>
      </div>

      <div class="file-input-wrapper">
  <input 
    type="file" 
    id="profileImage" 
    @change="onFileChange" 
    class="file-input"
    accept="image/*"
  />
  <div class="file-input-display">
    <span class="file-upload-text" :class="{ 'file-selected': profileImage }">
      {{ profileImage ? profileImage.name : '프로필 이미지를 선택해 주세요' }}
    </span>
    <span class="file-upload-button">파일 선택</span>
  </div>
</div>

      <div class="genre-container">
        <label>좋아하는 장르:</label>
        <div class="genre-grid">
          <div 
            v-for="genre in genreOptions" 
            :key="genre"
            class="genre-item"
            :class="{ selected: selectedGenres.includes(genre) }"
          >
            <input
              type="checkbox"
              :id="genre"
              :value="genre"
              v-model="selectedGenres"
              class="genre-checkbox"
            />
            <label :for="genre" class="genre-label">{{ genre }}</label>
          </div>
        </div>
      </div>

      <button class="signup-btn" type="submit">회원가입</button>
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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');

.signup-form {
  max-width: 400px;
  background: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 10px;
  position: relative;
}

.form-group label {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #999999;
  font-size: 16px;
  font-weight: 400;
  pointer-events: none;
  transition: all 0.3s ease;
  background: #ffffff;
  padding: 0 4px;
}

.form-input {
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
  transition: all 0.3s ease;
  box-sizing: border-box;
  color: #333333;
  font-family: inherit;
}

.form-input::placeholder {
  color: transparent;
}

.form-input:focus {
  outline: none;
  border-color: #666666;
}

.form-input:focus + label,
.form-input:not(:placeholder-shown) + label {
  top: 0;
  font-size: 14px;
  color: #666666;
  font-weight: 500;
}

.file-input-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-input-display {
  width: 100%;
  padding: 10px 20px;
  font-size: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
  color: #999999;
  cursor: pointer;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.file-input-display:hover {
  border-color: #666666;
}

.genre-container {
  margin-top: 10px;
}

.genre-container label {
  display: block;
  width: 100%;
  color: #666666;
  font-size: 16px;
  font-weight: 500;
  position: static;
  transform: none;
  background: none;
  padding: 0;
}

.genre-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.genre-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #ffffff;
}

.genre-item:hover {
  border-color: #666666;
  background: #f8f8f8;
}

.genre-item.selected {
  border-color: #666666;
  background: #f0f0f0;
}

.genre-checkbox {
  margin-right: 10px;
  width: 16px;
  height: 16px;
  accent-color: #666666;
}

.genre-label {
  font-size: 14px;
  color: #333333;
  cursor: pointer;
  margin: 0;
}

.login-btn {
  width: 100%;
  padding: 20px;
  background: #666666;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 30px;
  font-family: inherit;
}

.login-btn:hover {
  background: #555555;
}

.signup-btn {
  width: 100%;
  padding: 20px;
  background: #666666;
  color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 15px;
  font-family: inherit;
}



/* 첨부파일 */
.file-input-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-input-display {
  width: 100%;
  padding: 10px 20px;
  font-size: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
  color: #999999;
  cursor: pointer;
  transition: all 0.3s ease;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.file-input-display:hover {
  border-color: #666666;
}

.file-upload-icon {
  font-size: 18px;
  color: #999999;
}

.file-upload-text {
  flex: 1;
  text-align: left;
}

.file-upload-button {
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  color: #666666;
  font-weight: 500;
}

.file-selected {
  color: #333333;
}
</style>
