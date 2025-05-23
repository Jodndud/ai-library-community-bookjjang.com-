<template>
  <div class="book-detail container" v-if="book">
    <div class="book-info-wrap">
      <div class="cover">
        <img :src="book.fields.cover" :alt="book.fields.title" />
      </div>
      <div class="info">
        <h1 class="title">{{ book.fields.title }}</h1>
        <p class="meta">{{ book.fields.author }} 지음 | {{ book.fields.publisher }}</p>
        <p class="meta">{{ book.fields.pub_date }}</p>
        <p class="rating">⭐ {{ book.fields.rating ?? '5.0' }} <span class="reviews">(리뷰 1건)</span></p>
      </div>
    </div>

    <div class="book-description">
        <h1>상세 정보</h1>
        <p>{{ book.fields.description }}</p>
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
