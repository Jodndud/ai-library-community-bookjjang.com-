<template>
    <div class="container">
        <h1>리뷰</h1>
        <ul class="review-item">
            <li v-for="review in reviews" :key="review.id">
                <router-link class="review" :to="{ name: 'reviewDetail', params: { reviewId: review.id } }">
                    <div class="img"><img :src="review.cover_image" alt="cover" class="cover-image" /></div>
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
    margin-top: 40px;
    padding-top: 10px;
    border-top: 1px solid #dedede;
}

.review-item li {
    padding: 10px 0;
    border-bottom: 1px solid #dedede;
}
</style>