<template>
  <div class="container">
    <div class="title-wrap">
      <p class="rating-wrap"><span class="rating">{{ review.rating }}</span>/5</p>
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
      <!-- 댓글 목록 및 작성 -->
      <ul class="comment-wrap">
        <div class="byte_check_wrap">
          <textarea
            v-model="commentInputs[review.id]"
            class="form_textarea" title="답글 입력"
            placeholder="1000자 이내로 입력해주세요."
            maxlength="1000"></textarea>
          <div class="btn_wrap">
            <button class="comment-cancle" @click="cancelComment(review.id)">취소</button>
            <button class="comment-submit" @click="submitComment(review.id)">등록</button>
          </div>
        </div>

        <li class="comment" v-for="comment in review.comments" :key="comment.id">
          <div class="user-date">{{ comment.user }} | {{ comment.created_at }}</div>
          <div class="content">{{ comment.content }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviews'

const commentInputs = ref({})
const route = useRoute()
const reviewStore = useReviewStore()

const bookId = Number(route.params.bookId)
const reviewId = Number(route.params.reviewId)

const review = computed(() => reviewStore.reviewDetail)

onMounted(() => {
  reviewStore.detailReview(bookId, reviewId)
})

// 댓글 입력 초기화 (reviewId 별로 비워주기)
function cancelComment(reviewId) {
  commentInputs.value[reviewId] = ''
}

// 댓글 등록 함수 (서버에 전송 후 입력란 비우고 댓글 다시 불러오기)
function submitComment(reviewId) {
  const content = commentInputs.value[reviewId]
  if (!content?.trim()) return

  reviewStore.createComment(bookId, reviewId, { thread: reviewId, content })
    .then((newComment) => {
      commentInputs.value[reviewId] = ''  // 입력창 비우기
      reviewStore.detailReview(bookId, reviewId)  // 댓글 목록 다시 불러오기 ✅
    })
    .catch(err => {
      console.error('댓글 작성 실패:', err.response?.data || err.message)
    })
}
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