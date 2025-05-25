<template>
  <ul class="reviews-wrap">
    <li v-for="review in reviews" :key="review.id">
      <div class="content-wrap">
        <div class="user-date">
          {{ review.user }} | {{ review.created_at }}
        </div>
        <router-link :to="{name:'reviewDetail', params:{reviewId:review.id}}">
          <div class="img"><img :src="review.cover_image" alt=""></div>
          <div class="content">{{ review.title }}</div>
        </router-link>
        <div class="likes-comment-wrap">
          <div class="like-wrap">
            <span class="ico_like"></span>0
          </div>
          <div class="comment-btn" @click="toggleComments(review.id)">
            <span class="ico_reply"></span>
            답글 {{ review.comments.length }}
          </div>
        </div>
      </div>

      <!-- 댓글 목록 및 작성 -->
      <ul class="comment-wrap" v-if="visibleComments.includes(review.id)">
        <div class="byte_check_wrap">
          <textarea
            v-model="commentInputs[review.id]"
            class="form_textarea"
            title="답글 입력"
            placeholder="1000자 이내로 입력해주세요."
            maxlength="1000"
          ></textarea>
          <div class="btn_wrap">
            <button class="comment-cancle" @click="cancelComment(review.id)">취소</button>
            <button class="comment-submit" @click="submitComment(review.id)">등록</button>
          </div>
        </div>

        <li
          class="comment"
          v-for="comment in review.comments"
          :key="comment.id"
        >
          <div class="user-date">{{ comment.user }} | {{ comment.created_at }}</div>
          <div class="content">{{ comment.content }}</div>
        </li>
      </ul>
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useReviewStore } from '@/stores/reviews'
import { useRoute } from 'vue-router'

const reviewStore = useReviewStore()
const reviews = ref([])
const route = useRoute()
const visibleComments = ref([])
const commentInputs = ref({})

const toggleComments = (reviewId) => {
  if (visibleComments.value.includes(reviewId)) {
    visibleComments.value = visibleComments.value.filter(id => id !== reviewId)
  } else {
    visibleComments.value.push(reviewId)
  }
}

const cancelComment = (reviewId) => {
  commentInputs.value[reviewId] = ''
}

const submitComment = (reviewId) => {
  const content = commentInputs.value[reviewId]
  if (!content) return alert('내용을 입력해주세요.')

  reviewStore.createComment(reviewId, { content })
    .then(() => {
      commentInputs.value[reviewId] = ''
      fetchReviews()
    })
}

const fetchReviews = async () => {
  const bookId = route.params.pk
  await reviewStore.fetchReviews(bookId)
  reviews.value = reviewStore.reviews
}

onMounted(fetchReviews)
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
.reviews-wrap{
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
.content-wrap a{display: flex;gap: 10px;}
.content-wrap .img{
  width: 100px;height: 100px;overflow: hidden;
}
.content-wrap .img img{width: 100%;height: 100%;object-fit: cover;}
.content-wrap .content{font-size: 18px;font-weight: 500;}
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
.ico_like, .ico_reply {
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
