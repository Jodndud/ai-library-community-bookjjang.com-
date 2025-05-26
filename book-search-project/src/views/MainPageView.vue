<template>
  <div class="container">
    <div class="main-title">
      <h1>AI기반 추천도서 커뮤니티</h1>
      <p>회원 평점을 기반으로 한 상위 책 리스트입니다.</p>
    </div>

    <div class="main-wrap">
      <!-- 책짱 추천 도서 -->
      <KeepAlive>
         <MainPageRecommend />
      </KeepAlive>
            
      <!-- 리뷰 미리보기 -->
      <MainPageReview />

      <!-- 책짱 오늘의 추천 명대사 -->
      <Paragraph />
    </div>
  </div>
</template>

<script setup>
import MainPageReview from '@/components/MainPageReview.vue'
import MainPageRecommend from '@/components/MainPageRecommend.vue'
import Paragraph from '@/components/Paragraph.vue'

</script>

<style scoped>
.main-title {
  display: flex;
  flex-direction: column;
  gap: 12px;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.main-wrap {
  border: 1px solid #dedede;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

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