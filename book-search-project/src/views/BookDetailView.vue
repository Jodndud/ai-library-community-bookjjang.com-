<template>
  <div class="book-detail container" v-if="book">
    <div class="detail-inner" style="width:768px">

      <h1 class="section-title">책 정보</h1>
      <section class="detail-section book-info-wrap">
        <div class="cover">
          <img :src="book.cover" :alt="book.title" />
        </div>
        <div class="info">
          <h1 class="title">{{ book.title }}</h1>
          <p class="meta">{{ book.author }} 지음 | {{ book.publisher }}</p>
          <p class="meta">{{ book.pub_date }}</p>
          <p class="rating">⭐ {{ book.rating ?? '5.0' }} <span class="reviews">(리뷰 {{ reviewCount }}건)</span></p>
        </div>
      </section>

      <h1 class="section-title">상세 정보</h1>
      <section class="detail-section book-description">
        <p>{{ book.description }}</p>
      </section>

      <h1 class="section-title">도서리뷰 ({{ reviewCount }})</h1>
      <section class="detail-section review">
        <div class="review-title-wrap">
          <p>이 책을 읽고 느낀 감정을 작성해보세요. 책짱봇이 그림을 그려줍니다!</p>
          <button class="review-create-btn" @click="showReviewModal = true">리뷰쓰기</button>

          <!-- 리뷰작성 컴포넌트 -->
          <ReviewCreate :show="showReviewModal" :bookPk="book?.id" @close="showReviewModal = false" />
        </div>
        <!-- 리뷰 리스트 -->
        <ReviewList :bookPk="book?.id" />
      </section>

      <h1 class="section-title">작가 정보</h1>
      <section class="detail-section book-description">
        <p>{{ book.description }}</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useBookListStore } from '@/stores/booksList'
import { useReviewStore } from '@/stores/reviews'
import ReviewCreate from '@/components/ReviewCreate.vue'
import ReviewList from '@/components/ReviewList.vue'

const showReviewModal = ref(false)

const route = useRoute()
const bookStore = useBookListStore()
const reviewStore = useReviewStore()

const showComments = ref(false)

const bookId = computed(() => parseInt(route.params.pk, 10))

onMounted(() => {
  bookStore.FetchBookList()
  reviewStore.fetchReviews(bookId.value)
})


// 상세 도서 뽑아오기
const book = computed(() => {
  return bookStore.books.find(book => book.id === bookId.value)
})

const reviewCount = computed(() => {
  return reviewStore.reviews.filter(r => {
    const reviewBookId = typeof r.book === 'object' ? r.book.id : r.book
    return reviewBookId === book.value?.id  // ⬅️ .value 추가!
  }).length
})
</script>

<style scoped>
.container {
  margin-top: 40px;
}

.section-title {
  background: #f6f6f6;
  border: 1px solid #dedede;
  border-bottom: unset;
  padding: 8px 20px;
  width: fit-content;
  font-size: 18px;
  font-weight: 500;
  color: #333;
}

.detail-section {
  border-top: 1px solid #dedede;
  padding: 40px 0;
}

.detail-section p {
  font-size: 16px;
  line-height: 1.6;
  color: #595959;
}

/* 책 설명 */
.book-info-wrap {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.cover img {
  width: 220px;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  object-fit: cover;
}

.info {
  flex: 1;
}

.tags {
  margin-bottom: 8px;
  display: flex;
  gap: 8px;
}

.tag {
  display: inline-block;
  padding: 4px 8px;
  font-size: 13px;
  border-radius: 12px;
  background-color: #d1f0df;
  color: #2d7c4a;
  font-weight: 600;
}

.tag.gray {
  background-color: #f0f0f0;
  color: #666;
}

.title {
  font-size: 24px;
  margin: 8px 0;
  font-weight: bold;
}

.meta {
  color: #555;
  font-size: 14px;
  margin-top: 4px;
}

.rating {
  margin-top: 12px;
  font-size: 16px;
  color: #2a7;
}

.reviews {
  font-size: 13px;
  color: #999;
}
</style>
