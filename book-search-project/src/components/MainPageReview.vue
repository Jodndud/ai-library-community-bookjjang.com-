<template>
  <div class="main-page-section">
    <h2 class="section-title">📙 책짱 회원들의 리뷰에요 📙</h2>
    <ul class="review-item">
      <li v-for="review in reviews" :key="review.id">
        <router-link class="review" :to="{ name: 'reviewDetail', params: { bookId:review.book ,reviewId: review.id } }">
          <div class="img"><img :src="reviewStore.BASE_URL+review.cover_image" alt="cover" class="cover-image" /></div>
          <div class="hover-content">
            <div class="book-title">{{ review.title }}</div>
            <div class="like-count">0</div>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useReviewStore } from '@/stores/reviews'
import { useBookListStore } from '@/stores/booksList'
import { storeToRefs } from 'pinia'
import axios from 'axios'

const reviewStore = useReviewStore()
const bookStore = useBookListStore()

const { reviews } = storeToRefs(reviewStore)
const { books } = storeToRefs(bookStore)

const getBookTitle = (bookId) => {
  const book = books.value.find(book => book.pk === bookId)
  return book ? book.fields.title : '제목 없음'
}

onMounted(() => {
  bookStore.DetailBookList(1)      // 책 정보 가져오기
  bookStore.FetchBookReviews(1)    // 리뷰 가져오기 (방법 2인 경우)
})
</script>

<style scoped>
.review-item {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.review {
  position: relative;
  overflow: hidden;
  display: block;
}

.review .hover-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 12px;
  background-color: rgba(0, 0, 0, 0.6);
  /* 반투명 배경 추가 */
  opacity: 0;
  transition: all 0.2s ease-in-out;
}

.review:hover .hover-content {
  opacity: 1;
}

.review .hover-content .book-title {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.review .img {
  height: 270px;
}

.review img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
</style>