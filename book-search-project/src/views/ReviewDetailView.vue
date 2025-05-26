<template>
  <div class="container">
    <div class="title-wrap">
      <h2>{{ review.title }}</h2>
      <p class="user">{{ review.user }}</p>
    </div>
    <p class="text">{{ review.content }}</p>
    <div class="review-detail-wrap">
      <div class="img">
        <img :src="reviewStore.BASE_URL + review.cover_image" width="100%" alt="">
      </div>
      <div class="comment-wrap">
      </div>
    </div>
    <div>
      <p><strong>작성일:</strong> {{ review.created_at }}</p>

      <h3>댓글</h3>
      <ul>
        <li v-for="comment in review.comments" :key="comment.id">
          {{ comment.user }}: {{ comment.content }} ({{ comment.created_at }})
        </li>
      </ul>
    </div>
  </div>
</template>


<script setup>
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviews'

const route = useRoute()
const reviewStore = useReviewStore()

const bookId = Number(route.params.bookId)
const reviewId = Number(route.params.reviewId)

const review = computed(() => reviewStore.reviewDetail)

onMounted(() => {
  reviewStore.detailReview(bookId, reviewId)
})
</script>



<style scoped>
.title-wrap{
  display: flex;justify-content: space-between;align-items: center;
  background-color: #eee;
  padding: 12px 20px;margin-top: 40px;
}
.title-wrap h2{font-size: 22px;font-weight: 500;}
.title-wrap .user{font-size: 14px;color: #80888A;font-weight: 300;}
.img{
  padding: 20px;
}
</style>