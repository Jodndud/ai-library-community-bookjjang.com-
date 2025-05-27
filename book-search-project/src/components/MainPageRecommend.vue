<template>
  <div class="main-page-section">
    <h2 class="section-title">📒 도서 리스트 평점 TOP 10 📒</h2>
    <!-- 리뷰 평점이 높은 순으로 5개 -->
    <div class="recommend-books-wrap">
      <swiper
        v-if="topRatedBooks.length > 0"
        :slidesPerView="4"
        :spaceBetween="30"
        :modules="modules"
        :autoplay="{
          delay: 2000,
          disableOnInteraction: false,
        }"
        :loop="topRatedBooks.length > 5"
        class="recommend-books"
      >
        <swiper-slide v-for="book, index in topRatedBooks" :key="book.id">
          <router-link :to="{ name: 'bookDetail', params: { pk: book.id } }">
            <span class="rank-tag" :class="{ gray: index + 1 >= 4 }">
              {{ index + 1 }}
            </span>
            <div class="book">
              <div class="img"><img :src="book.cover" alt=""></div>
              <div class="text-wrap">
                <p>⭐ {{ (parseFloat(book.average_rating) || 0).toFixed(1) }}</p>
                <h3>{{ book.title }}</h3>
                <p>{{ book.author }}</p>
              </div>
            </div>
          </router-link>
        </swiper-slide>
      </swiper>
    </div>
  </div>

</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useBookListStore } from '@/stores/booksList';
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Autoplay } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/navigation'

// Swiper에서 사용할 모듈 정의
const modules = [Navigation, Autoplay]

const bookStore = useBookListStore()

// average_rating 기준으로 정렬
const topRatedBooks = computed(() => {
  const booksArray = Array.isArray(bookStore.books) ? bookStore.books : []
  return booksArray
    .slice()
    .sort((a, b) => (b.average_rating || 0) - (a.average_rating || 0))
    .slice(0, 10)
})

onMounted(() => {
  bookStore.FetchBookList()
})
</script>

<style>
/* swiper */
.recommend-books {
  padding: 0 25px;
  position: relative;
}

.swiper-button-prev:after,
.swiper-button-next:after {
  position: absolute;
  font-size: 20px;
  border: 1px solid #dedede;
  background: #eee;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #3d3c3f;
}

.swiper-button-prev:after {
  left: 5px;
}

.swiper-button-next:after {
  right: 5px;
}

.rank-tag {
  position: absolute;
  top: 0;
  left: 0;
  background-color: #f1c40f;
  /* 노란색 배경 */
  color: #fff;
  font-weight: bold;
  padding: 6px 12px;
  font-size: 18px;
  border-top-left-radius: 6px;
  border-bottom-right-radius: 6px;
  z-index: 10;
  clip-path: polygon(0 0, 100% 0, 100% 70%, 50% 100%, 0 70%);
}

.rank-tag.gray {
  background-color: #a3a39c; /* 회색 */
}

.recommend-books-wrap {
  width: 100%;
}

.recommend-books-wrap .book {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommend-books-wrap .img {
  background: #eee;
  border: 1px solid #dedede;
  height: 210px;
  overflow: hidden;
  border-radius: 5px 12px 12px 5px;
}

.recommend-books-wrap .img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.text-wrap h3 {
  font-size: 16px;
  color: #3d3c3f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.text-wrap p {
  font-size: 14px;
  color: #80888a;
}
</style>