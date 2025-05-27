<template>
    <div class="container">
      <div class="profile-wrap">

        <div class="profile-title-wrap">
          <div class="profile-img">
            <img :src="accountStore.userInfo.profile_image || '/no-profile-img.png'" />
          </div>
          <h2 class="nickname">{{ accountStore.userInfo.nickname }}님</h2>
        </div>

        <div class="right-wrap">
          <div class="user-info">
            <h3>내가 쓴 리뷰 : {{ userReviews.length }} 건</h3>
          </div>

          <div class="user-info">
            <h3>연간 독서량 : {{ accountStore.userInfo.yearly_reading_amount }} 권</h3>
          </div>

          <div class="user-info">
            <h3>관심 장르 :</h3>
            <ul class="favorite-genre">
              <li
                v-for="genre in accountStore.userInfo.favorite_genres"
                :key="genre"
                >
                {{ genre }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="my-page-section recommend-wrap">
        <div class="text-wrap">
          <h3 class="title">추천도서</h3>
          <p class="desc">{{ accountStore.userInfo.nickname }}님의 관심장르를 기반으로 한 추천도서에요!</p>
        </div>
        <!-- 추천도서 카테고리별 분류 -->
        <!-- <div class="categories-wrap">
          <RouterLink v-for="category in categoryStore.categories" :key="category.pk"
            :to="category.pk === 0 ? { name: 'books' } : { name: 'books', params: { categoryId: category.pk } }"
            :class="{ active: isActive(category.pk) }">
            {{ category.fields.name }}
          </RouterLink>
        </div> -->
        <swiper
          v-if="recommendedBooks.length > 0"
          :slidesPerView="4"
          :spaceBetween="30"
          :modules="modules"
          :loop="true"
          class="recommend-books"
        >
          <swiper-slide v-for="book in recommendedBooks" :key="book.id">
            <div class="book">
              <RouterLink :to="{ name:'bookDetail', params:{pk:book.id}}">
                <div class="img"><img :src="book.cover" alt=""></div>
              </RouterLink>
              <div class="text-wrap">
                <RouterLink :to="{ name:'bookDetail', params:{pk:book.id}}">
                  <h3>{{ book.title }}</h3>
                </RouterLink>
                <p class="author">{{ book.author }}</p>
              </div>
            </div>
          </swiper-slide>
        </swiper>
      </div>

      <div class="my-page-section">
        <div class="text-wrap">
          <h3>나의 리뷰 [{{ userReviews.length }}]</h3>
        </div>
        <ul class="review-wrap" v-if="userReviews && userReviews.length">
          <li
          v-for="review in userReviews"
          :key="review.id"
          >
            <RouterLink :to="{ name:'reviewDetail', params:{ bookId:review.book, reviewId:review.id }}">
              <div class="img"><img :src="review.cover_image" alt=""></div>
            </RouterLink>
          </li>
        </ul>
        
        <div class="no-review" v-else>
          <p>작성된 리뷰가 없습니다.</p>
        </div>
      </div>
    </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'

import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'

import { useAccountStore } from '@/stores/accounts'
import { useReviewStore } from '@/stores/reviews'
import { useBookListStore } from '@/stores/booksList'
import { useCategoryStore } from '@/stores/category'

import 'swiper/css'
import 'swiper/css/navigation'

const modules = [Navigation]

const accountStore = useAccountStore()
const reviewStore = useReviewStore()
const bookStore = useBookListStore()
const categoryStore = useCategoryStore()

onMounted(async () => {
  await accountStore.myPage()
  await reviewStore.reviewsList()
  await bookStore.FetchBookList()
})

// 사용자 본인의 리뷰만 필터링
const userReviews = computed(() =>
  reviewStore.reviews.filter(
    (review) => review.user === accountStore.userInfo.username
  )
)

// 관심 장르와 일치하는 책 필터링
const recommendedBooks = computed(() => {
  const favoriteGenres = accountStore.userInfo.favorite_genres || []

  // pk → name 매핑: { 1: '소설/시/희곡', ... }
  const categoryMap = new Map(
    (categoryStore.categories || []).map(cat => [cat.pk, cat.fields.name])
  )

  // 필터링된 책 리스트
  return bookStore.books.filter(book => {
    const categoryName = categoryMap.get(book.category)
    return favoriteGenres.includes(categoryName)
  })
})

</script>

<style scoped>
.right-wrap{
  display: flex;flex-direction: column;gap:8px;
  padding: 15px 0;
}
.user-info{
  display: flex;flex-direction: column;gap: 5px;
  
}
.user-info h3{
  letter-spacing: -0.5px;
  margin-bottom: 5px;
  font-size: 16px;font-weight: 400;
}

.my-page-section{
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #dedede;
}
.my-page-section h3{
  font-size: 20px;margin-bottom: 5px;
}

.profile-section .container{
    height: 100%;padding: 0;
    display: flex;align-items: center;gap: 80px;
}

.profile-title-wrap{
  padding: 40px;
  border-radius: 12px;
  display: flex;flex-direction: column;align-items: center;
}
.profile-wrap{
  margin-top: 40px;
  display: flex;gap: 25px;
}

.profile-wrap .profile-img{
    width: 120px;height: 120px;
    background: #fff;
    border-radius: 60px;
    overflow: hidden;
}
.profile-wrap .profile-img img{width: 100%;}
.profile-wrap .nickname{
    margin: 7px 0 12px;
    font-size: 20px;
}

/* 나의 리뷰 */
.review-wrap{
  display: grid;grid-template-columns: repeat(4, 1fr);gap: 10px;
  margin-top: 15px;
}
.review-wrap .img{width: 100%;}
.review-wrap .img img{max-width: 200px;}


/* genre */
.favorite-genre{
  width: 100%;color: #292929;
  display: flex;justify-content: center;gap: 12px;
}
.favorite-genre li{
  font-size: 14px;
  background: #e9f1e7;
  padding: 5px 16px;
  border-radius: 5px;
}


/* swiper */
.recommend-wrap{
    display: flex;flex-direction: column;gap: 20px;
}
.recommend-books{
    width: 100%;
}
.recommend-books .book{
  
}
.recommend-books .book .img {
  height: 220px;
  border: 1px solid #dedede;
  overflow: hidden;
  border-radius: 4px 12px 12px 4px;
}
.recommend-books .book .img img{width: 100%;height: 100%;object-fit: cover;}
.recommend-books .book h3{font-size: 14px;margin: 8px 0 0;}
</style>