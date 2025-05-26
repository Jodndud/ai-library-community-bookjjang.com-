<template>
    <div class="container">
        <ul class="review-item">
            <li v-for="review in reviewStore.reviews" :key="review.id">
                <router-link class="review" :to="{ name: 'reviewDetail', params: { bookId:review.book, reviewId: review.id } }">
                    <div class="img"><img :src="reviewStore.BASE_URL+review.cover_image" alt="cover" class="cover-image" /></div>
                    <div class="hover-content">
                        <div class="book-title">{{ review.title }}</div>
                        <div class="like-count">[0]</div>
                    </div>
                </router-link>
                <div class="right-content">
                    <p class="book-title">{{ bookTitleById(review.book) }}</p>
                    <p class="username">{{ review.user }}</p>
                </div>
            </li>
        </ul>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useReviewStore } from '@/stores/reviews'
import { useBookListStore } from '@/stores/booksList'

const reviewStore = useReviewStore()
const bookStore = useBookListStore()

// 책 제목을 bookId로 찾아 반환하는 함수
function bookTitleById(bookId) {
  const book = bookStore.books.find((b) => b.id === bookId)
  return book ? book.title : '알 수 없는 책'
}

onMounted(() => {
  reviewStore.reviewsList()
  bookStore.FetchBookList()  // 책 목록 미리 불러오기
})
</script>

<style scoped>
.review-item {
    margin-top: 40px;
    border-top: 1px solid #dedede;
}

.review-item li {
    padding: 8px 0;
    border-bottom: 1px solid #dedede;
    display: flex;justify-content: space-between;align-items: center;
}

.review{display: flex;gap: 12px;}
.review .img{
    width: 80px;height: 80px;overflow: hidden;
}
.review img{width: 100%;}
.review .hover-content{display: flex;align-items: center;gap: 8px;}


.right-content{
    display: flex;align-content: center;gap: 12px;
    font-size: 16px;font-weight: 300;color: #333;
}
.right-content .book-title{color: red;}
</style>