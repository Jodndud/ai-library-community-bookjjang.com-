<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <form class="modal" @submit.prevent="reviewCreate">
      <h2>리뷰 작성</h2>
      <!-- 평점을 매겨주세요 -->
      <div class="rating-input">
        <input type="number" v-model.number="rating" min="0" max="5" step="0.5" @input="emitRating" />
        <span>{{ rating.toFixed(1) }}</span>
      </div>
      <input v-model="title" class="modal-input" placeholder="제목을 입력하세요" />
      <textarea v-model="content" class="modal-textarea" placeholder="내용을 입력하세요"></textarea>
      <div class="modal-actions">
        <button class="cancel-btn" @click="$emit('close')">취소</button>
        <button class="submit-btn" type="submit">등록</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useReviewStore } from '@/stores/reviews'

const emit = defineEmits(['close'])
const reviewStore = useReviewStore()
const props = defineProps({
  show: Boolean,
  bookPk: Number
})

const title = ref('')
const content = ref('')
const rating = ref(0.0)

const reviewCreate = function () {
  const reviewInfo = {
    title: title.value,
    content: content.value,
    // rating: rating.value
    book: props.bookPk // 만약 서버에서 book을 요구하면 주석 해제
  }
  reviewStore.createReview(props.bookPk, reviewInfo)
  emit('close')
}

</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  background: white;
  padding: 24px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.modal h2 {
  margin-bottom: 12px;
  font-size: 20px;
}

.modal-input,
.modal-textarea {
  width: 100%;
  margin-bottom: 12px;
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.modal-textarea {
  height: 100px;
  outline: 0;
  overflow-y: auto;
  resize: none;
  letter-spacing: -0.01em;
  font-family: "Noto Sans KR", sans-serif;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.cancel-btn,
.submit-btn {
  padding: 6px 12px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #aaa;
  color: white;
}

.submit-btn {
  background-color: #2d7c4a;
  color: white;
}
</style>