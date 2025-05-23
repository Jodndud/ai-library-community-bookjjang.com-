<template>
  <div class="book-detail container" v-if="book">
    <div class="detail-inner" style="width:768px">

      <h1 class="section-title">책 정보</h1>
      <section class="detail-section book-info-wrap">
        <div class="cover">
          <img :src="book.fields.cover" :alt="book.fields.title" />
        </div>
        <div class="info">
          <h1 class="title">{{ book.fields.title }}</h1>
          <p class="meta">{{ book.fields.author }} 지음 | {{ book.fields.publisher }}</p>
          <p class="meta">{{ book.fields.pub_date }}</p>
          <p class="rating">⭐ {{ book.fields.rating ?? '5.0' }} <span class="reviews">(리뷰 1건)</span></p>
        </div>
      </section>
      
      <h1 class="section-title">상세 정보</h1>
      <section class="detail-section book-description">
        <p>{{ book.fields.description }}</p>
      </section>
      
      <h1 class="section-title">도서리뷰 (1)</h1>
      <section class="detail-section review">
        <div class="review-title-wrap">
          <p>이 책을 읽고 느낀 감정을 작성해보세요. 책짱봇이 그림을 그려줍니다!</p>
          <button class="review-create-btn">리뷰쓰기</button>
        </div>
        <ul class="reviews-wrap">
          <li>
            <div class="content-wrap">
              <div class="user-date">
                user | 2025.04.09
              </div>
              <div class="content">이런 시기에 좋은 산문 한편 읽을 수 있게 해주셔서 고마워요</div>
              <div class="likes-comment-wrap">
                <div class="like-wrap">0</div>
                <div class="comment-btn" @click="showComments = !showComments">
                  답글 0
                </div>
              </div>
            </div>
            <ul class="comment-wrap" v-if="showComments">
              <div class="byte_check_wrap">
                <textarea class="form_textarea" title="답글 입력" placeholder="1000자 이내로 입력해주세요." maxlength="1000"></textarea>
                <div class="btn_wrap">
                  <button class="comment-cancle" type="button">취소</button>
                  <button class="comment-submit" type="button">등록</button>
                </div>
              </div>
              <li
                v-for="i in 2"
                class="comment"
              >
              <div class="user-date">user | 2025.04.09</div>
              <div class="content">너무 좋아요</div>
              </li>
            </ul>
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useBookListStore } from '@/stores/booksList'

const route = useRoute()
const bookStore = useBookListStore()
const book = ref(null)

const showComments = ref(false)

onMounted(async () => {
  if (bookStore.books.length === 0) {
    await bookStore.fetchBooks()
  }

  const pk = parseInt(route.params.pk)
  book.value = bookStore.books.find(b => b.pk === pk)
})
</script>

<style scoped>
.container {
  margin-top: 40px;
}

.section-title{
  background: #f6f6f6;
  border: 1px solid #dedede;
  border-bottom: unset;
  padding: 8px 20px;
  width: fit-content;
  font-size: 18px;font-weight: 500;
  color: #333;
}
.detail-section{
  border-top: 1px solid #dedede;
  padding: 40px 0;
}
.detail-section p{
  font-size: 16px;line-height: 1.6;
  color: #595959;
}

/* 리뷰 */
.review-title-wrap{
  display: flex;justify-content: space-between;align-items: flex-end;
  border-bottom: 1px solid #dedede;
}
.review .section-title{
  margin: 0;
}
.review-create-btn{
  background: #f6f6f6;
  border: 1px solid #dedede;
  padding: 10px 20px;
  font-size: 14px;
}
.likes-comment-wrap{
  display: flex;justify-content: flex-end;gap: 20px;
}
.content-wrap{
  margin-top: 20px;
  padding-bottom: 20px;
  border-bottom:1px solid #dedede
}
.comment-btn{
  font-size: 14px;color: #767676;
  cursor: pointer;
}

/* 댓글 */
.comment-wrap{
  padding-top: 12px;
}
.byte_check_wrap{
  display: flex;flex-direction: column;
}
.comment{
  display: block;
  position: relative;
  padding: 20px 20px 21px 37px;
  box-sizing: border-box;
  background-color: #f7f7f7;
  border-radius: 10px;
  margin-top: 8px;
}
.comment::before{
  content: '';display: inline-block;
  position: absolute;top: 24px;   left: 20px;
  width: 8px;height: 9px;
  background: url(../assets/img/arw_reply@2x.png) 0% 0% no-repeat;
  background-size: 8px 9px;
}
.comment .content{
  font-size: 14px;
}
.user-date{
  margin-bottom: 9px;
  font-size: 12px;color: #767676;
}
.form_textarea{
  width: 100%;height: 70px;
  padding: 11px 14px 0;
  font-size: 14px;color: #000;
  border: 1px solid #d5d5d5;border-radius: 6px 6px 0 0;
  border-bottom: unset;
  outline: 0;
  overflow-y: auto;
  resize: none;
  letter-spacing: -0.01em;
  font-family: "Noto Sans KR", sans-serif;
}
.btn_wrap{
  border: 1px solid #d5d5d5;border-radius: 0 0 6px 6px;
  border-top: unset;
  padding: 10px 10px 10px 14px;
  display: flex;justify-content: flex-end;gap: 4px;
}
.btn_wrap button{
  cursor: pointer;
  font-size: 12px;
  padding: 6px 9px;
  border-radius: 4px;
  border: unset;
  color: #fff;
}
.btn_wrap .comment-cancle{
  background: #767676;
}
.btn_wrap .comment-submit{
  background: #2d7c4a;
}



.book-info-wrap {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.cover img {
  width: 220px;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  object-fit: cover;
}

.info {
  flex: 1;
}

.tags {
  margin-bottom: 8px;
  display: flex;
  gap: 8px;
}

.tag {
  display: inline-block;
  padding: 4px 8px;
  font-size: 13px;
  border-radius: 12px;
  background-color: #d1f0df;
  color: #2d7c4a;
  font-weight: 600;
}

.tag.gray {
  background-color: #f0f0f0;
  color: #666;
}

.title {
  font-size: 24px;
  margin: 8px 0;
  font-weight: bold;
}

.meta {
  color: #555;
  font-size: 14px;
  margin-top: 4px;
}

.rating {
  margin-top: 12px;
  font-size: 16px;
  color: #2a7;
}

.reviews {
  font-size: 13px;
  color: #999;
}
</style>
