<template>
  <div class="container">
    <div class="categories-wrap">
      <button
        v-for="option in sortOptions"
        :key="option"
        @click="selectedSort = option"
        :class="{ active: selectedSort === option }"
        class="sort-button"
      >
        {{ option }}
      </button>
    </div>

    <ul class="review-item">
      <li v-for="review in sortedReviews" :key="review.id">
        
        <div class="left-content">
          <div class="like">
            <div class="like-img"><img src="../assets/img/ico_like@2x.png" alt=""></div>
            {{ review.like_count }}
          </div>
            <router-link
              class="review"
              :to="{ name: 'reviewDetail', params: { bookId: review.book, reviewId: review.id } }"
            >
            <div class="img">
              <img
              :src="review.cover_image"
              alt="cover"
              class="cover-image"
              @error="e => e.target.src = noImage"
              />
            </div>
            <div class="title-wrap">
              <div class="hover-content">
                <div class="book-title">{{ review.title }}</div>
                <div class="comments-count">[{{ review.comments.length || 0 }}]</div>
              </div>
            </div>
          </router-link>
        </div>
        <div class="right-content">
          <p class="book-title"><span class="title">도서명 : </span>{{ bookTitleById(review.book) }}</p>
          <p class="rating">⭐ {{ review.rating ?? '0.0' }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>


<script setup>
import noImage from '@/assets/img/no_image.jpg'

import { ref, onMounted, computed } from 'vue'
import { useReviewStore } from '@/stores/reviews'
import { useBookListStore } from '@/stores/booksList'

const reviewStore = useReviewStore()
const bookStore = useBookListStore()

onMounted(() => {
  reviewStore.reviewsList()
  bookStore.FetchBookList()  // 책 목록 미리 불러오기
})

const sortOptions = ['최신순', '좋아요순']
const selectedSort = ref('최신순')

// 책 제목 반환 함수
function bookTitleById(bookId) {
  const book = bookStore.books.find((b) => b.id === bookId)
  return book ? book.title : '알 수 없는 책'
}

// 정렬된 리뷰 목록 (computed로 반응형 정렬)
const sortedReviews = computed(() => {
  const reviews = [...reviewStore.reviews]
  if (selectedSort.value === '최신순') {
    return reviews.sort((a, b) => b.id - a.id)  // 최신순: ID 내림차순
  } else if (selectedSort.value === '좋아요순') {
    return reviews.sort((a, b) => b.like_count - a.like_count)  // 좋아요순
  }
  return reviews
})
</script>

<style scoped>
.container{
    width: 768px;
}
.left-content{display: flex;gap: 15px;}
.review-item {
    border-top: 1px solid #dedede;
}

.review-item li {
    padding: 8px 0;
    border-bottom: 1px solid #dedede;
    display: flex;justify-content: space-between;align-items: center;
}

.review{display: flex;gap: 12px;align-items: center;}
.review .img{
    width: 80px;height: 80px;overflow: hidden;
}
.review img{width: 100%;}
.review .hover-content{display: flex;align-items: center;gap: 8px;}
.left-content .like{display: flex;gap: 4px;align-items: center;}
.left-content .like .like-img{width: 20px;display: flex;align-items: center;}
.left-content .like .like-img img{width: 100%;}


.title-wrap{
    display: flex;flex-direction: column;justify-content: center;
}
.title-wrap p{
    font-size: 13px;color: #878787;font-weight: 300;
}

.right-content{
    display: flex;align-content: flex-end;gap: 4px;flex-direction: column;
    font-size: 16px;font-weight: 300;color: #333;text-align: right;
}
.right-content .book-title{
  display: flex;align-items: center;gap: 8px;
  color: #333;font-weight: 700;
}
.right-content .book-title .title{font-size:14px ;color:#878787;font-weight: 300;}
.right-content .rating{
    font-size: 14px;
}

/* 필터 바 */
.categories-wrap{
    display: flex;margin: 40px 0 10px;
    justify-content: flex-end;
}
.categories-wrap .sort-button:first-child {
    border-left: 1px solid #dedede;
}

.categories-wrap .sort-button {
    cursor: pointer;
    font-size: 14px;
    padding: 8px 12px;
    background: #f6f6f6;
    border: 1px solid #dedede;
    border-left: unset;
}

.categories-wrap .sort-button.active {
    background: #2d7c4a;
    color: #fff;
}

/* hover 효과 */
.review-item li {
    padding: 8px 20px;
    border-bottom: 1px solid #dedede;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
    cursor: pointer;
}

.review-item li:hover {
    background-color: rgba(45, 124, 74, 0.05);
}

.review {
    display: flex;
    gap: 12px;
    align-items: center;
    text-decoration: none;
}

.review .title-wrap .book-title {
    transition: all 0.2s ease;
    text-decoration: none;
}

.review:hover .title-wrap .book-title {
    text-decoration: underline;
}
</style>