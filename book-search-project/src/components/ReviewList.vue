<template>
  <ul class="reviews-wrap">
    <li v-for="review in filteredReviews" :key="review.pk">
      <div class="content-wrap">
        <div class="user-date">
          {{ review.fields.user }} | {{ review.fields.created_at }}
        </div>
        <router-link :to="{ name: 'reviewDetail', params: { reviewId: review.pk } }">
          <div class="img"><img :src="review.fields.cover_image" alt="" /></div>
          <div class="content">{{ review.fields.title }}</div>
        </router-link>
        <div class="likes-comment-wrap">
          <div class="like-wrap">
            <span class="ico_like"></span>0
          </div>
          <div class="comment-btn" @click="toggleComments(review.pk)">
            <span class="ico_reply"></span>
            답글 {{ getCommentsByReview(review.pk).length }}
          </div>
        </div>
      </div>

      <!-- 댓글 목록 및 작성 -->
      <ul class="comment-wrap" v-if="visibleComments.includes(review.pk)">
        <div class="byte_check_wrap">
          <textarea v-model="commentInputs[review.pk]" class="form_textarea" title="답글 입력"
            placeholder="1000자 이내로 입력해주세요." maxlength="1000"></textarea>
          <div class="btn_wrap">
            <button class="comment-cancle" @click="cancelComment(review.pk)">취소</button>
            <button class="comment-submit" @click="submitComment(review.pk)">등록</button>
          </div>
        </div>

        <li class="comment" v-for="comment in getCommentsByReview(review.pk) || []" :key="comment.pk">
          <div class="user-date">{{ comment.user }} | {{ comment.fields.created_at }}</div>
          <div class="content">{{ comment.fields.content }}</div>
        </li>
      </ul>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useReviewStore } from '@/stores/reviews'
import { useCommentStore } from '@/stores/comments'

const props = defineProps({
  bookPk: {
    type: Number,
    required: true,
  },
})

const reviewStore = useReviewStore()
const commentStore = useCommentStore()
const visibleComments = ref([])
const commentInputs = ref({})

// 해당 책에 존재하는 리뷰 필터링
const filteredReviews = computed(() => {
  return reviewStore.reviews.filter(review => review.fields.book === props.bookPk)
})

// 댓글 관련련
// 해당 리뷰에 존재하는 댓글 필터링
const getCommentsByReview = (reviewId) => {
  return commentStore.comments.filter(comment => comment.fields.thread === reviewId)
}
// 댓글 창 토글
const toggleComments = (reviewId) => {
  if (visibleComments.value.includes(reviewId)) {
    visibleComments.value = visibleComments.value.filter((id) => id !== reviewId)
  } else {
    visibleComments.value.push(reviewId)
  }
}
// 댓글 작성
const submitComment = (reviewId) => {
  const content = commentInputs.value[reviewId]
  if (!content) return alert('내용을 입력해주세요.')

  commentStore.createComment(props.bookPk, reviewId, { content }).then(() => {
    commentInputs.value[reviewId] = ''
    commentStore.fetchComments(props.bookPk, reviewId) // 최신 댓글 반영용
  })
}


const cancelComment = (reviewId) => {
  commentInputs.value[reviewId] = ''
}

onMounted(() => {
  reviewStore.fetchReviews(props.bookPk)
})

watch(() => props.bookPk, (newPk) => {
  reviewStore.fetchReviews(newPk)
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
