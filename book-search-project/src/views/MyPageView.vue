<template>
    <section class="sub-section profile-section">
        <div class="container">
            <div class="profile-wrap">
                <div class="profile-img"><img :src="userInfo.profile_image" style="width:100%" alt=""></div>
                <h2 class="nickname">{{ userInfo.nickname }}님</h2>
                <div class="follow-wrap">
                    <div class="follow">
                        <p class="title">팔로우</p>
                        <p class="num">0</p>
                    </div>
                    <div class="follow-line"></div>
                    <div class="follow follower">
                        <p class="title">팔로워</p>
                        <p class="num">0</p>
                    </div>
                </div>
            </div>

            <div class="recommend-wrap">
                <div class="text-wrap">
                    <p class="title">추천도서</p>
                    <p class="desc">{{ userInfo.nickname }}님의 관심장르를 기반으로 한 추천도서에요!</p>
                </div>
                <swiper
                    :slidesPerView="4"
                    :spaceBetween="30"
                    :modules="modules"
                    :navigation="true"
                    :loop="true"
                    class="recommend-books"
                >
                    <swiper-slide
                        v-for="i in 5"
                    >
                        <div class="book">{{ i }}</div>
                    </swiper-slide>
                </swiper>
            </div>
        </div>
    </section>
</template>

<script setup>
import profileImg from '@/assets/img/test-profile.png'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/navigation'

// Swiper에서 사용할 모듈 정의
const modules = [Navigation]

const userInfo = {
  nickname: 'booklover99',
  age: 27,
  yearly_reading_amount: 52,
  favorite_genres: ['소설', 'SF', '추리'],
  profile_image: profileImg,
}
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
.profile-wrap .nickname{
    margin: 7px 0 12px;
    font-size: 20px;
}
.profile-wrap .follow-wrap{
    display: flex;justify-content: center;align-items: center;
    background: #eee;
    padding: 20px 24px;
    border-radius: 16px;
}
.profile-wrap .follow-wrap{
}
.profile-wrap .follow-wrap .follow-line{
    width: 1px;height: 12px;background: #333;
    margin: 0 24px;
}
.profile-wrap .follow-wrap .follow{
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