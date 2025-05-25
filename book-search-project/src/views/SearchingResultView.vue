<template>
    <div class="container">
        <div class="booklistview">
            <!-- <div class="category-nav">
                <input type="text" v-model="keyword" placeholder="검색어를 입력하세요...">
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
            </div> -->

            <ul class="context-wrap">
              <li v-if="filterBooks.length === 0" class="no-result">
                '{{ keyword }}'의 검색 결과가 없습니다.
              </li>
              <li v-for="book in filterBooks" :key="book.pk">
                <router-link :to="{name:'bookDetail', params:{pk:book.pk}}">
                  <div class="img">
                    <img style="width:100%;height:100%;object-fit: cover;" :src="book.fields.cover" :alt="book.fields.title">
                  </div>
                </router-link>
                <div class="text-wrap">
                  <router-link :to="{name:'bookDetail', params:{pk:book.pk}}">
                    <h3>{{ book.fields.title }}</h3>
                  </router-link>
                  <p>{{ book.fields.author }} | {{ book.fields.publisher }} | {{ book.fields.pub_date }}</p>
                  <p class="text-sub-title">{{ book.fields.subTitle }}</p>
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
  bookStore.fetchBooks()
  categoryStore.fetchCategories()
})

// URL에서 categoryId 가져오기
const categoryId = computed(() => route.params.categoryId)

// 필터링된 책 목록 계산
const filterBooks = computed(() => {
  const parsedId = parseInt(categoryId.value)
  
  return bookStore.books.filter(book => {
    const matchesCategory = isNaN(parsedId) || book.fields.category === parsedId
    const lowerKeyword = keyword.value.toLowerCase()

    const matchesKeyword = (() => {
      if (!lowerKeyword) return true
      const { title, author } = book.fields
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
  }
)
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
    border-top: 1px solid #dedede;
}
.context-wrap > li{
  display: flex;gap: 16px;padding: 24px 0;
  border-bottom: 1px solid #dedede;
}
.context-wrap > li .img{
  width: 120px;
  border: 1px solid #ddd;
  overflow: hidden;
}
.context-wrap > li .text-wrap{
}
</style>