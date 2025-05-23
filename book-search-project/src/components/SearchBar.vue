<template>
  <div class="select-wrap" :class="{ active: showSelect || isInputFocused }" ref="dropdownRef">
    <div>
      <div>
        <button class="select-btn" @click="toggleSelect">
          {{ selectedOption }}
          <img style="width:8px;margin-top: 2px;" src="../assets/img/select-down.svg" alt=""
            :class="{ rotated: showSelect }">
        </button>
        <select class="hidden" id="searchSelect">
          <option value="TOT">통합검색</option>
          <option value="TITLE">제목</option>
          <option value="AUTHOR">저자</option>
        </select>
      </div>
      <ul class="select" v-if="showSelect">
        <li @click="selectItem('통합검색', 'TOT')">통합검색</li>
        <li @click="selectItem('제목', 'TITLE')">제목</li>
        <li @click="selectItem('저자', 'AUTHOR')">저자</li>
      </ul>
    </div>

    <form id="searchForm" @submit.prevent="onSubmit">
      <input v-model="searchInput" type="text" placeholder="예: 김영하의 그 책 뭐더라..." @focus="isInputFocused = true"
        @blur="isInputFocused = false">
      <button><img src="../assets/img/search-btn.svg" alt=""></button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

// select option 초기화
const showSelect = ref(false)
const selectedOptionCode = ref('TOT')
const selectedOption = ref('통합검색')

// hidden button toggle
const dropdownRef = ref(null)
const isInputFocused = ref(false)

const router = useRouter()
const searchInput = ref('')

const toggleSelect = () => {
  showSelect.value = !showSelect.value
}

const selectItem = (label, value) => {
  selectedOption.value = label
  selectedOptionCode.value = value
  document.getElementById('searchSelect').value = value
  showSelect.value = false
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showSelect.value = false
    isInputFocused.value = false
  }
}

const onSubmit = () => {
  if (searchInput.value.trim()) {
    router.push({
      name: 'booksResult',
      params: { value: searchInput.value.trim() },
      query: { type: selectedOptionCode.value }  // 예: 'TITLE'
    })
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.select-wrap {
  position: relative;
  display: flex;
  align-items: center;
  border: 1px solid #bbbbbb;
  border-radius: 29px;
  height: 45px;
  margin: 0 auto;
  width: fit-content;
}

.select-wrap.active {
  border: 1px solid #000;
}

/* select-btn */
.select-btn {
  position: relative;
  width: 116px;
  display: flex;
  gap: 16px;
  align-items: center;
  border: unset;
  background: unset;
  cursor: pointer;
  font-size: 14px;
  padding: 13px 0 13px 20px;
}

.select-btn img.rotated {
  transform: rotate(180deg);
}

.select-btn::after {
  content: '';
  position: absolute;
  right: 0;
  display: block;
  width: 1px;
  height: 10px;
  background: #00000015;
}

.hidden {
  display: none;
}

.select {
  position: absolute;
  background: #fff;
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
  bottom: -104px;
  left: 0;
  padding: 12px 18px;
  border: 1px solid #000;
  border-radius: 10px;
}

.select>li {
  font-size: 12px;
  color: #777;
  cursor: pointer;
}

.select>li:hover {
  color: #000;
}

/* form */
#searchForm input {
  height: 100%;
  padding: 13px 100px 13px 20px;
  border: unset;
  background: unset;
  font-size: 14px;
  outline: none;
}

#searchForm button {
  border: unset;
  background: unset;
}

#searchForm button img {
  width: 15px;
  transform: translate(0, 3px);
  margin-right: 20px;
  cursor: pointer;
}
</style>