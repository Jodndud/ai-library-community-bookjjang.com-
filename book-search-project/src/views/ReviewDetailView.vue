<template>
  <div class="container">
    <p class="create-date">{{ review?.created_at }}</p>
    <div class="title-wrap">
      <p class="rating-wrap"><span class="rating">{{ review?.rating || 0 }}</span>/5</p>
      <h2>{{ review?.title }}</h2>
      <p class="user">{{ review?.user }}</p>
    </div>

    <div class="review-detail-wrap">
      <div class="img">
        <img :src="reviewStore.BASE_URL + review?.cover_image" width="100%" alt="">
      </div>
      <p class="text">{{ review?.content }}</p>
    </div>

    <div v-if="review">
      <!-- 댓글 목록 및 작성 -->
      <ul class="comment-wrap">
        <div class="like-wrap" @click="reviewLike(review.id)">
          <!-- 안전한 likes 체크 -->
          <span class="ico_like" :class="{
            liked: review.likes?.includes(currentUsername)
          }"></span>
          {{ review.like_count || 0 }}
        </div>

        <div class="byte_check_wrap">
          <textarea v-model="commentInputs[review.id]" class="form_textarea" title="답글 입력"
            placeholder="1000자 이내로 입력해주세요." maxlength="1000"></textarea>
          <div class="btn_wrap">
            <button class="comment-cancel" @click="cancelComment(review.id)">취소</button>
            <button class="comment-submit" @click="submitComment(review.id)">등록</button>
          </div>
        </div>

        <li class="comment" v-for="comment in review.comments" :key="comment.id">
          <div class="user-date">{{ comment.user }} | {{ comment.created_at }}</div>
          <div class="content">{{ comment.content }}</div>
        </li>
      </ul>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="loading">
      리뷰를 불러오는 중...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviews'
import { useAccountStore } from '@/stores/accounts'

const reviewStore = useReviewStore()
const authStore = useAccountStore()
const commentInputs = ref({})
const route = useRoute()

const bookId = Number(route.params.bookId)
const reviewId = Number(route.params.reviewId)
const review = computed(() => reviewStore.reviewDetail)

const currentUsername = computed(() => authStore.username)

// 좋아요 기능 - 낙관적 업데이트 버전
const reviewLike = async (reviewId) => {
  if (!authStore.token) {
    alert('로그인이 필요합니다.')
    return
  }

  // 현재 리뷰 상태 백업
  const currentReview = { ...review.value }
  const isCurrentlyLiked = currentReview.likes?.includes(currentUsername.value)

  try {
    // UI 먼저 업데이트 (낙관적 업데이트)
    if (isCurrentlyLiked) {
      // 좋아요 취소
      currentReview.like_count = (currentReview.like_count || 1) - 1
      currentReview.likes = currentReview.likes?.filter(user => user !== currentUsername.value) || []
    } else {
      // 좋아요 추가
      currentReview.like_count = (currentReview.like_count || 0) + 1
      currentReview.likes = [...(currentReview.likes || []), currentUsername.value]
    }

    // 스토어 업데이트
    reviewStore.reviewDetail = currentReview

    // 서버에 요청
    await reviewStore.reviewLike(bookId, reviewId)

  } catch (error) {
    console.error('좋아요 처리 실패:', error)
    alert('좋아요 처리 중 오류가 발생했습니다.')

    // 실패 시 원래 상태로 복구
    await reviewStore.detailReview(bookId, reviewId)
  }
}

onMounted(() => {
  reviewStore.detailReview(bookId, reviewId)
})

// 댓글 입력 초기화
function cancelComment(reviewId) {
  commentInputs.value[reviewId] = ''
}

// 댓글 등록 함수
function submitComment(reviewId) {
  const content = commentInputs.value[reviewId]
  if (!content?.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  reviewStore.createComment(bookId, reviewId, { thread: reviewId, content })
    .then(() => {
      commentInputs.value[reviewId] = ''  // 입력창 비우기
      reviewStore.detailReview(bookId, reviewId)  // 상세 정보 다시 불러오기
    })
    .catch(err => {
      console.error('댓글 작성 실패:', err.response?.data || err.message)
      alert('댓글 작성에 실패했습니다.')
    })
}
</script>



<style scoped>
.container {
  padding-top: 40px;
}

.create-date {
  font-size: 14px;
  color: #252525;
  font-weight: 300;
  margin: 0 0 5px 5px;
}

.title-wrap {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #eee;
  padding: 12px 20px;
}

.title-wrap h2 {
  font-size: 22px;
  font-weight: 500;
}

.title-wrap .user {
  font-size: 14px;
  color: #80888A;
  font-weight: 300;
}

.img {
  padding: 20px;
}

.review-detail-wrap {
  padding-bottom: 50px;
  border: 1px solid #dedede;
  border-top: unset;
}

.review-detail-wrap .text {
  padding: 0 20px;
}

.like-btn {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  border: unset;
  background: unset;
  margin: 10px auto 20px;
  font-size: 16px;
  font-weight: 500;
}

.like-btn img {
  width: 25px;
  transform: translateY(-3px);
}

.like-wrap {
  cursor: pointer;
  width: fit-content;
  display: flex;
  justify-content: center;
  margin: 10px auto 20px;
  font-size: 14px;
  color: #767676;
}

.ico_like,
.ico_reply {
  width: 20px;
  height: 20px;
  margin-right: 4px;
  background: url(../assets/img/ico_like@2x.png) center no-repeat;
  background-size: 20px 20px;
}

.ico_reply {
  background: url(../assets/img/ico_reply@2x.png) center no-repeat;
  background-size: contain;
}

.ico_like.liked {
  background: url(../assets/img/ico_ullike@2x.png) center no-repeat;
  background-size: contain;
}
</style>