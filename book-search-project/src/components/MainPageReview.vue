<template>
  <div class="main-page-section">
    <h2 class="section-title">📙 책짱 회원들의 리뷰에요 📙</h2>
    <ul class="review-item">
      <li v-for="review in sortedReviews" :key="review.id">
        <router-link class="review" :to="{ name: 'reviewDetail', params: { bookId:review.book ,reviewId: review.id } }">
          <div class="img"><img :src="review.cover_image" alt="cover" @error="e => e.target.src = noImage" class="cover-image" /></div>
          <div class="hover-content">
            <div class="like-count">{{ getBookTitle(review.book) }}</div>
            <div class="title-wrap">
              <div class="book-title">{{ review.title }}</div>
              <p>⭐ {{ review.rating ?? '0.0' }}</p>
            </div>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import noImage from '@/assets/img/no_image.jpg'
import { onMounted, computed } from 'vue'
import { useReviewStore } from '@/stores/reviews'
import { useBookListStore } from '@/stores/booksList'

const reviewStore = useReviewStore()
const bookStore = useBookListStore()

onMounted(() => {
  reviewStore.reviewsList()
  bookStore.FetchBookList()
})

// 최신순으로 정렬
const sortedReviews = computed(() => {
  return [...reviewStore.reviews].sort((a, b) => {
    return b.id - a.id
  })
})

// 책 제목을 반환하는 함수
const getBookTitle = (bookId) => {
  const book = bookStore.books.find(b => b.id === bookId)
  return book ? book.title : '(제목 없음)'
}
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

.hover-content .title-wrap{
  display: flex;justify-content: space-between;align-items: center;
}

/* 호버 콘텐츠 기본 상태 */
.hover-content {
  position: absolute;
  bottom: -100%;
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.7); /* 반투명 검정 배경 */
  color: #fff;
  padding: 15px 8px 10px;
  transition: bottom 0.3s ease;
  display: flex;
  flex-direction: column;
}

/* 호버 시 위로 올라옴 */
.review:hover .hover-content {
  bottom: 0;
}

.book-title {
  font-weight: bold;
  font-size: 16px;
}

.like-count {
  font-size: 13px;
  opacity: 0.85;
}

.review .img {
  height: 190px;
}

.review img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
</style>