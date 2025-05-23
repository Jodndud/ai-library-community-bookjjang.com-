<template>
    <!-- <section class="sub-section books">
        <div class="container">

            <div class="text-wrap">
                <h1>전체 도서</h1>
                <P>원하는 도서를 찾아보세요</P>
            </div>
        </div>
    </section> -->
    <div class="booklistview">
        <div class="container">

            <div class="category-nav">
                <div class="categories-wrap">
                    <RouterLink
                        v-for="category in categoryStore.categories"
                        :key="category.pk"
                        :to="category.pk === 0 ? { name: 'books' } : { name: 'books', params: { categoryId: category.pk } }"
                        :class="{ active: isActive(category.pk) }"
                    >
                        {{ category.fields.name }}
                    </RouterLink>
                </div>
                <input type="text" v-model="keyword" placeholder="검색어를 입력하세요...">
            </div>
            <ul class="context-wrap">
                <li v-for="book in filterBooks" :key="book.pk">
                    <div class="img"><img style="width:100%;height:100%;object-fit: cover;" :src="book.fields.cover" :alt="book.fields.title"></div>
                    <div class="text-wrap">
                        <h3>{{ book.fields.title }}</h3>
                        <p>{{ book.fields.author }} | {{ book.fields.publisher }} | {{ book.fields.pub_date }}</p>
                        <p class="text-sub-title">{{ book.fields.subTitle }}</p>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useBookListStore } from '@/stores/booksList'
import { useCategoryStore } from '@/stores/category'

const bookStore = useBookListStore()
const categoryStore = useCategoryStore()
const route = useRoute()

const keyword = ref('')

onMounted(() => {
  bookStore.fetchBooks()
  categoryStore.fetchCategories()
})


const isActive = (pk) => {
  // 현재 URL에 categoryId가 없으면 pk가 0일 때 active
  if (!route.params.categoryId && pk === 0) return true
  return parseInt(route.params.categoryId) === pk
}

// URL params에서 categoryId 가져오기 (반응형)
const categoryId = computed(() => route.params.categoryId)

// 필터링된 책 목록 계산
const filterBooks = computed(() => {
  const parsedId = parseInt(categoryId.value)

  return bookStore.books.filter(book => {
    const matchesCategory = isNaN(parsedId) || book.fields.category === parsedId
    const matchesKeyword = book.fields.title.includes(keyword.value)
    return matchesCategory && matchesKeyword
  })
})
</script>

<style scoped>
.booklistview{
    display: flex;flex-direction: column;
}
.booklistview h1{
    font-size: 28px;
}

.category-nav{
    display: flex;justify-content: space-between;align-items: flex-end;
    margin: 30px 0 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid #eee;
}
.categories-wrap > a.active {
  color: #ff9a66;
  font-weight: bold;
}
.category-nav input{
  border: 1px solid #666;
  height: 40px;width: 300px;border-radius: 20px;
  padding-left: 20px;
  outline: none;
}
.category-nav .categories-wrap{
  display: flex;gap: 20px;
}
.category-nav .categories-wrap > a{
  font-size: 16px;
}

.context-wrap{
    display: grid;grid-template-columns: repeat(6, 1fr);
    gap: 16px 32px;
}
.context-wrap > li{
  display: flex;flex-direction: column;
  gap: 16px; 
}
.context-wrap > li .img{
  border: 1px solid #ddd;
  height: 240px;
  overflow: hidden;
}
</style>