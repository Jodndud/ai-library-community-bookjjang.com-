<template>
  <div class="container">
    <!-- 책짱 추천 도서 -->
    <MainPageRecommend />

    <!-- 리뷰 미리보기 -->
    <MainPageReview />

    <!-- 책짱 오늘의 추천 명대사 -->
    <Paragraph />
  </div>
</template>

<script setup>
import MainPageReview from '@/components/MainPageReview.vue'
import MainPageRecommend from '@/components/MainPageRecommend.vue'
import Paragraph from '@/components/Paragraph.vue'

</script>

<style scoped>
.main-section .container {
  height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.title-content {
  text-align: center;
  margin-bottom: 100px;
}

.title-content p {
  margin-bottom: 12px;
  font-size: 16px;
}

.title-content h1 {
  font-size: 38px;
  line-height: 1.4;
  margin: 12px 0 40px;
}
</style>