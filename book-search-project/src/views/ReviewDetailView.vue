<template>
  <section class="sub-section">
    <img :src="review.fields.cover_image" width="100%" alt="">
  </section>
  <div class="container">
    <div>
      <h2>{{ review.title }}</h2>
      <p><strong>작성자:</strong> {{ review.fields.user }}</p>
      <p><strong>내용:</strong> {{ review.fields.content }}</p>
      <p><strong>작성일:</strong> {{ review.fields.created_at }}</p>

      <h3>댓글</h3>
      <ul>
        <li v-for="comment in filteredComments" :key="comment.pk">
          {{ comment.fields.user }}: {{ comment.fields.content }} ({{ comment.fields.created_at }})
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviews'
import { useCommentStore } from '@/stores/comments'
import { computed, onMounted } from 'vue'

const route = useRoute()
const reviewStore = useReviewStore()
const commentStore = useCommentStore()

const reviewId = parseInt(route.params.reviewId)

// 선택된 리뷰
const review = computed(() => {
  return reviewStore.reviews.find(r => r.pk === reviewId)
})

// 해당 리뷰와 연결된 댓글만 필터링
const filteredComments = computed(() => {
  return commentStore.comments.filter(comment => comment.fields.thread === reviewId)
})

// 댓글 가져오기 (onMounted에서 반드시 호출!)
onMounted(() => {
  commentStore.fetchComments()
})
</script>



<style scoped>
.sub-section {
  overflow: hidden;
}
</style>