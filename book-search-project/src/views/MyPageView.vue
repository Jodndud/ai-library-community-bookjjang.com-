<template>
    <div class="container">
      <div class="profile-wrap">
        <div class="profile-img">
          <img :src="accountStore.userInfo.profile_image || '/no-profile-img.png'" />
        </div>
        <h2 class="nickname">{{ accountStore.userInfo.nickname }}님</h2>
      </div>

      <div class="recommend-wrap">
        <div class="text-wrap">
          <p class="title">추천도서</p>
          <p class="desc">{{ accountStore.userInfo.nickname }}님의 관심장르를 기반으로 한 추천도서에요!</p>
        </div>
        <swiper
          :slidesPerView="4"
          :spaceBetween="30"
          :modules="modules"
          :navigation="true"
          :loop="true"
          class="recommend-books"
        >
          <swiper-slide v-for="i in 5" :key="i">
            <div class="book">{{ i }}</div>
          </swiper-slide>
        </swiper>
      </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/navigation'

const modules = [Navigation]

const accountStore = useAccountStore()

onMounted(() => {
  accountStore.myPage()
})
</script>

<style scoped>
.profile-section .container{
    height: 100%;padding: 0;
    display: flex;align-items: center;gap: 80px;
}

.profile-wrap{
    width: 250px;
}
.profile-wrap .profile-img{
    width: 100px;height: 100px;
    background: #fff;
    border-radius: 50px;
    overflow: hidden;
}
.profile-wrap .profile-img img{width: 100%;}
.profile-wrap .nickname{
    margin: 7px 0 12px;
    font-size: 20px;
}

/* swiper */
.recommend-wrap{
    margin-top: 140px;
    display: flex;flex-direction: column;gap: 20px;
}
.recommend-books{
    width: 900px;
}
.recommend-books .book{
    background: #555;
    height: 250px;
}
</style>