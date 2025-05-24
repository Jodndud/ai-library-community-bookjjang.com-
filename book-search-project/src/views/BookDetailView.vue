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
          <button class="review-create-btn" @click="showReviewModal = true">리뷰쓰기</button>

          <!-- 리뷰작성 컴포넌트 -->
          <ReviewCreate
            :show="showReviewModal"
            @close="showReviewModal=false"
            @submit="handleReviewSubmit"
          />
        </div>
        <!-- <ul class="reviews-wrap">
          <li>
            <div class="content-wrap">
              <div class="user-date">
                user | 2025.04.09
              </div>
              <div class="content">이런 시기에 좋은 산문 한편 읽을 수 있게 해주셔서 고마워요</div>
              <div class="likes-comment-wrap">
                <div class="like-wrap">0</div>
                <div class="comment-btn" @click="showComments = !showComments">
                  답글 2
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
        </ul> -->
        <!-- 리뷰 리스트 -->
        <ReviewList />
      </section>

      <h1 class="section-title">작가 정보</h1>
      <section class="detail-section book-description">
        <p>{{ book.fields.description }}</p>
      </section>
    </div>
  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useBookListStore } from '@/stores/booksList'
  import ReviewCreate from '@/components/ReviewCreate.vue'
  import ReviewList from '@/components/ReviewList.vue'

  const showReviewModal = ref(false)

  const handleReviewSubmit = (review) => {
    console.log('리뷰 제출됨:', review)
    // 여기에 API 호출 또는 상태 저장 로직을 추가하면 됩니다.
  }
  const route = useRoute()
  const bookStore = useBookListStore()
  const book = ref(null)

  const showComments = ref(false)

  onMounted(async () => {
    // if (bookStore.books.length === 0) {
    //   await bookStore.fetchBooks()
    // }
    await bookStore.fetchBooks()

    const pk = parseInt(route.params.pk)
    book.value = bookStore.books.find(b => b.pk === pk)
    console.log(book.fields.cover)
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

  /* 책 설명 */
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

  .info {flex: 1;}

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

  .tag.gray {background-color: #f0f0f0;color: #666;}

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
