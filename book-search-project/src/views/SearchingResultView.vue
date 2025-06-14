<template>
  <div class="container">
    <div class="booklistview">
      <ul class="context-wrap">
        <li v-if="filterBooks.length === 0" class="no-result">
          '{{ keyword }}'의 검색 결과가 없습니다.
        </li>
        <li v-for="book in filterBooks" :key="book.pk">
          <router-link :to="{ name: 'bookDetail', params: { pk: book.id } }">
            <div class="img">
              <img style="width:100%;height:100%;object-fit: cover;" :src="book.cover" :alt="book.title">
            </div>
          </router-link>
          <div class="text-wrap">
            <router-link :to="{ name: 'bookDetail', params: { pk: book.id } }">
              <h3>{{ book.title }}</h3>
            </router-link>
            <p>{{ book.author }} | {{ book.publisher }} | {{ book.pub_date }}</p>
            <p class="text-sub-title">{{ book.subTitle }}</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBookListStore } from '@/stores/booksList'
import { useCategoryStore } from '@/stores/category'

const bookStore = useBookListStore()
const categoryStore = useCategoryStore()
const route = useRoute()

const keyword = ref(route.params.value || '')     // 검색어
const type = ref(route.query.type || 'TOT')       // 검색 타입

onMounted(() => {
  bookStore.FetchBookList()
  // categoryStore.fetchCategories()
})

// URL에서 categoryId 가져오기
const categoryId = computed(() => route.params.categoryId)

// 필터링된 책 목록 계산
const filterBooks = computed(() => {
  const parsedId = parseInt(categoryId.value)

  return bookStore.books.filter(book => {
    const matchesCategory = isNaN(parsedId) || book.category === parsedId
    const lowerKeyword = keyword.value.toLowerCase()

    const matchesKeyword = (() => {
      if (!lowerKeyword) return true
      const { title, author } = book
      if (type.value === 'TITLE') return title.toLowerCase().includes(lowerKeyword)
      if (type.value === 'AUTHOR') return author.toLowerCase().includes(lowerKeyword)
      // TOT(전체)인 경우
      return title.toLowerCase().includes(lowerKeyword) || author.toLowerCase().includes(lowerKeyword)
    })()

    return matchesCategory && matchesKeyword
  })
})

watch(
  () => route.fullPath,
  () => {
    keyword.value = route.params.value || ''
    type.value = route.query.type || 'TOT'
    bookStore.FetchBookList()
  }
)
</script>


<style scoped>
.container {
  padding-top: 40px;
}

.category-nav .categories-wrap>a.active {
  color: rgb(143, 187, 114);
  font-weight: bold;
}

.category-nav input {
  border: 1px solid #666;
  height: 40px;
  width: 100%;
  border-radius: 4px;
  padding-left: 8px;
  margin-bottom: 12px;
}

.booklistview {
  display: flex;
  gap: 40px;
}

.category-nav {
  width: 150px;
}

.category-nav .categories-wrap {
  display: flex;
  flex-direction: column;
}

.category-nav .categories-wrap>a {
  font-size: 14px;
  padding: 6px 20px 6px 0;
}

.context-wrap {
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex: 1;
  border-top: 1px solid #dedede;
}

.context-wrap>li {
  display: flex;
  gap: 16px;
  padding: 24px 0;
  border-bottom: 1px solid #dedede;
}

.context-wrap>li .img {
  width: 120px;
  border: 1px solid #ddd;
  overflow: hidden;
}

.context-wrap>li .text-wrap {}
</style>