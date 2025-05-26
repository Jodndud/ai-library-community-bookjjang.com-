<template>
    <section class="sub-section">
        <img :src="review.cover_image" width="100%" alt="">
    </section>
  <div class="container">
    <div>
      <h2>{{ review.title }}</h2>
      <p><strong>작성자:</strong> {{ review.user }}</p>
      <p><strong>내용:</strong> {{ review.content }}</p>
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
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviews'
import { computed } from 'vue'

const route = useRoute()
const reviewStore = useReviewStore()

const reviewId = parseInt(route.params.reviewId)

const review = computed(() => {
  return reviewStore.reviews.find(r => r.id === reviewId)
})
</script>


<style scoped>
.sub-section{
    overflow: hidden;
}
</style>