<template>
  <ul class="reviews-wrap">
    <li v-for="review in sortedReviews" :key="review.id">
      <div class="content-wrap">
        <div class="user-date">
          {{ review.user }} | {{ review.created_at }}
        </div>
        <router-link :to="{ name: 'reviewDetail', params: { bookId: bookId, reviewId: review.id } }">
          <div class="img"><img :src="review.cover_image" @error="e => e.target.src = noImage" alt="" /></div>
          <div class="content">{{ review.title }}</div>
        </router-link>
        <div class="likes-comment-wrap">
          <div class="like-wrap" @click="reviewLike(review.id)">
            <!-- likes 배열에 현재 사용자가 포함되어 있는지 확인 -->
            <span class="ico_like" :class="{
              liked: review.likes && review.likes.includes(currentUsername)
            }"></span>
            {{ review.like_count || 0 }}
          </div>
          <div class="comment-btn" @click="toggleComments(review.id)">
            <span class="ico_reply"></span>
            답글 {{ review.comments?.length || 0 }}
          </div>
        </div>
      </div>

      <!-- 댓글 목록 및 작성 -->
      <ul class="comment-wrap" v-if="visibleComments.includes(review.id)">
        <div class="byte_check_wrap">
          <textarea v-model="commentInputs[review.id]" class="form_textarea" title="답글 입력"
            placeholder="1000자 이내로 입력해주세요." maxlength="1000"></textarea>
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
    </li>
  </ul>
</template>

<script setup>
import noImage from '@/assets/img/no_image.jpg'
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useReviewStore } from '@/stores/reviews'
import { useAccountStore } from '@/stores/accounts'

const authStore = useAccountStore()
const reviewStore = useReviewStore()
const route = useRoute()
const bookId = Number(route.params.pk)

const visibleComments = ref([])
const commentInputs = ref({})

const currentUsername = computed(() => authStore.username)

// token 변할 때마다 내 정보 갱신
watch(
  () => authStore.token,
  (newToken) => {
    if (newToken) {
      authStore.myPage()
    } else {
      authStore.userInfo = null
    }
  },
  { immediate: true }
)

onMounted(() => {
  reviewStore.fetchReviews(bookId)
})

// 댓글 토글 함수
function toggleComments(reviewId) {
  if (visibleComments.value.includes(reviewId)) {
    visibleComments.value = visibleComments.value.filter((id) => id !== reviewId)
  } else {
    visibleComments.value.push(reviewId)
  }
}

// 댓글 입력 초기화
function cancelComment(reviewId) {
  commentInputs.value[reviewId] = ''
}

// 댓글 등록 함수
function submitComment(reviewId) {
  const content = commentInputs.value[reviewId]
  if (!content?.trim()) return

  reviewStore
    .createComment(bookId, reviewId, { thread: reviewId, content })
    .then(() => {
      commentInputs.value[reviewId] = ''
    })
    .catch((err) => {
      console.error('댓글 작성 실패:', err.response?.data || err.message)
    })
}

// 좋아요 기능 수정
const reviewLike = async (reviewId) => {
  if (!authStore.token) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    // 서버에 좋아요 요청을 먼저 보냄
    await reviewStore.reviewLike(bookId, reviewId)

    // 성공하면 리뷰 목록을 다시 가져와서 최신 상태로 업데이트
    await reviewStore.fetchReviews(bookId)

  } catch (error) {
    console.error('좋아요 처리 실패:', error)
    alert('좋아요 처리 중 오류가 발생했습니다.')
  }
}

// 최신순 정렬된 리뷰 목록
const sortedReviews = computed(() => {
  return [...reviewStore.reviews]
    .filter((r) => {
      const reviewBookId = typeof r.book === 'object' ? r.book.id : r.book
      return reviewBookId === bookId
    })
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})
</script>

<style>
.review-title-wrap {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #f0f0f0;
  padding: 30px 0;
  gap: 20px;
  margin: 0 20px 40px;
}

.review .section-title {
  margin: 0;
}

.review-create-btn {
  background: #f6f6f6;
  border: 1px solid #dedede;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all .1s;
}

.review-create-btn:hover {
  background: #2d7c4a;
  color: #fff;
}

.reviews-wrap {
  border-top: 1px solid #dedede;
}

.likes-comment-wrap {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.content-wrap {
  margin-top: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #dedede;
}

.content-wrap a {
  display: flex;
  gap: 10px;
}

.content-wrap .img {
  width: 100px;
  height: 100px;
  overflow: hidden;
}

.content-wrap .img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.content-wrap .content {
  font-size: 18px;
  font-weight: 500;
}

.comment-btn {
  font-size: 14px;
  color: #767676;
  cursor: pointer;
  display: flex;
}

.like-wrap {
  cursor: pointer;
  display: flex;
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

.comment-wrap {
  padding: 12px 0;
  border-bottom: 1px solid #dedede;
}

.byte_check_wrap {
  display: flex;
  flex-direction: column;
}

.comment {
  display: block;
  position: relative;
  padding: 20px 20px 21px 37px;
  box-sizing: border-box;
  background-color: #f7f7f7;
  border-radius: 10px;
  margin-top: 8px;
}

.comment::before {
  content: '';
  display: inline-block;
  position: absolute;
  top: 24px;
  left: 20px;
  width: 8px;
  height: 9px;
  background: url(../assets/img/arw_reply@2x.png) 0% 0% no-repeat;
  background-size: 8px 9px;
}

.comment .content {
  font-size: 14px;
}

.user-date {
  margin-bottom: 9px;
  font-size: 12px;
  color: #767676;
}

.form_textarea {
  width: 100%;
  height: 70px;
  padding: 11px 14px 0;
  font-size: 14px;
  color: #000;
  border: 1px solid #d5d5d5;
  border-radius: 6px 6px 0 0;
  border-bottom: unset;
  outline: 0;
  overflow-y: auto;
  resize: none;
  letter-spacing: -0.01em;
  font-family: "Noto Sans KR", sans-serif;
}

.btn_wrap {
  border: 1px solid #d5d5d5;
  border-radius: 0 0 6px 6px;
  border-top: unset;
  padding: 10px 10px 10px 14px;
  display: flex;
  justify-content: flex-end;
  gap: 4px;
}

.btn_wrap button {
  cursor: pointer;
  font-size: 12px;
  padding: 6px 9px;
  border-radius: 4px;
  border: unset;
  color: #fff;
}

.btn_wrap .comment-cancle {
  background: #767676;
}

.btn_wrap .comment-submit {
  background: #2d7c4a;
}
</style>
