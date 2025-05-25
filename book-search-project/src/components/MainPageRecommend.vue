<template>
  <div class="main-page-section">
    <h2 class="section-title">상위 별점 도서 리스트</h2>
    <!-- 리뷰 평점이 높은 순으로 5개 -->
    <!-- book.user_rating -->
    <!-- <ul class="recommend-books-wrap">
      <li
      v-for="book in topRatedBooks"
      :key="book.pk"
      class="book"
      >
      <div class="img"><img :src="book.fields.cover" alt=""></div>
      <div class="text-wrap">
        <h3>{{ book.fields.title }}</h3>
        <p>{{ book.fields.author }}</p>
      </div>
    </li>
  </ul> -->
  <div class="recommend-books-wrap">
    <swiper
        :slidesPerView="5"
        :spaceBetween="30"
        :modules="modules"
        :navigation="true"
        :loop="true"
        class="recommend-books"
    >
        <swiper-slide
          v-for="book, index in topRatedBooks"
          :key="book.pk"
        >
          <router-link :to="{name:'bookDetail', params:{pk:book.pk}}">
            <span v-if="index <= 4" class="rank-tag">
              {{ index + 1 }}
            </span>
            <div class="book">
              <div class="img"><img :src="book.fields.cover" alt=""></div>
              <div class="text-wrap">
                <h3>{{ book.fields.title }}</h3>
                <p>{{ book.fields.author }}</p>
              </div>
            </div>
          </router-link>
        </swiper-slide>
    </swiper>
  </div>
</div>

</template>

<script setup>
import { computed } from 'vue'
import { useBookListStore } from '@/stores/booksList';
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/navigation'

// Swiper에서 사용할 모듈 정의
const modules = [Navigation]

const bookStore = useBookListStore()

// customer_review_rank 기준으로 정렬하고 상위 5개만 추출
const topRatedBooks = computed(() => {
  return [...bookStore.books]
    .sort((a, b) => b.fields.customer_review_rank - a.fields.customer_review_rank)
})
</script>

<style>
/* swiper */
.recommend-books{
  padding: 0 50px;
  position: relative;
}
.swiper-button-prev:after, .swiper-button-next:after{
  position: absolute;
  font-size: 20px;
  border: 1px solid #dedede;
  background: #eee;
  width: 50px;height: 50px;
  display: flex;justify-content: center;align-items: center;
  color: #3d3c3f;
}
.swiper-button-prev:after{left: 5px;}
.swiper-button-next:after{right: 5px;}
.rank-tag {
  position: absolute;
  top: 0;
  left: 0;
  background-color: #f1c40f; /* 노란색 배경 */
  color: #fff;
  font-weight: bold;
  padding: 6px 12px;
  font-size: 18px;
  border-top-left-radius: 6px;
  border-bottom-right-radius: 6px;
  z-index: 10;
  clip-path: polygon(0 0, 100% 0, 100% 70%, 50% 100%, 0 70%);
}



.recommend-books-wrap{
  width: 100%;
}
.recommend-books-wrap .book{
  display: flex;flex-direction: column;gap: 12px;
}
.recommend-books-wrap .img{
  background: #eee;
  border: 1px solid #dedede;
  height: 290px;
  overflow: hidden;
  border-radius: 5px 12px 12px 5px;
}
.recommend-books-wrap .img img{
  width: 100%;height: 100%;object-fit: cover;
}
.text-wrap h3 {
    font-size: 16px;
    color: #3d3c3f;
}
.text-wrap p{
    font-size: 14px;
    color: #80888a;
}
</style>