<template>
    <div class="container">
        <div class="booklistview">
            <div class="category-nav">
                <!-- <input type="text" v-model="keyword" placeholder="검색어를 입력하세요..."> -->
                <div class="categories-wrap">
                    <h1>카테고리</h1>
                    <RouterLink
                        v-for="category in categoryStore.categories"
                        :key="category.pk"
                        :to="category.pk === 0 ? { name: 'books' } : { name: 'books', params: { categoryId: category.pk } }"
                        exact-active-class="active"
                    >
                        {{ category.fields.name }}
                    </RouterLink>
                </div>
                <div class="filter-keyword">
                    <h1>필터</h1>
                    
                </div>
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

console.log('검색어:', keyword)
console.log('검색 유형:', type)
const bookStore = useBookListStore()
const categoryStore = useCategoryStore()
const route = useRoute()

const keyword = route.params.value
const type = route.query.type  // 'TOT', 'TITLE', 'AUTHOR'

onMounted(() => {
  bookStore.fetchBooks()
  categoryStore.fetchCategories()
})

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
.container{
    padding-top: 40px;
}
.category-nav .categories-wrap > a.active {
  color: rgb(143, 187, 114);
  font-weight: bold;
}

.category-nav input{
  border: 1px solid #666;
  height: 40px;width: 100%;border-radius: 4px;
  padding-left: 8px;margin-bottom: 12px;
}

.booklistview{
    display: flex;gap: 40px;
}
.category-nav{
    width: 150px;
}
.category-nav .categories-wrap{
  display: flex;flex-direction: column;
}
.category-nav .categories-wrap > a{
  font-size: 14px;padding: 6px 20px 6px 0;
}

.context-wrap{
    display: flex;flex-direction: column;gap: 16px;flex: 1;
}
.context-wrap > li{
  display: flex;gap: 16px;padding: 24px 0;border-top: 1px solid #ddd;
}
.context-wrap > li .img{
  width: 120px;
  border: 1px solid #ddd;
  overflow: hidden;
}
.context-wrap > li .text-wrap{
}
</style>