<template>
    <div class="booklistview">
        <div class="container">
            <div class="category-nav">
                <div class="categories-wrap">
                    <RouterLink v-for="category in categoryStore.categories" :key="category.pk"
                        :to="category.pk === 0 ? { name: 'books' } : { name: 'books', params: { categoryId: category.pk } }"
                        :class="{ active: isActive(category.pk) }">
                        {{ category.fields.name }}
                    </RouterLink>
                </div>
            </div>
            <div class="search-wrap">
                <div class="category-name"><span class="name">'{{ currentCategoryName }}'</span>카테고리</div>
                <input type="text" v-model="keyword" placeholder="검색어를 입력하세요...">
            </div>
            <ul class="context-wrap">
                <li v-for="book in getFilteredBooks()" :key="book.id" :book="book">
                    <RouterLink :to="{ name: 'bookDetail', params: { pk: book.id } }">
                        <div class="img">
                            <img style="width:100%;height:100%;object-fit: cover;" :src="book.cover" :alt="book.title">
                        </div>
                    </RouterLink>
                    <div class="text-wrap">
                        <RouterLink :to="{ name: 'bookDetail', params: { pk: book.id } }">
                            <h3>{{ book.title }}</h3>
                        </RouterLink>
                        <p>{{ book.author }}</p>
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
    bookStore.FetchBookList()
})

// 해당 카테고리의 이름을 찾는 computed 추가
const currentCategoryName = computed(() => {
  const id = categoryId.value
  if (isNaN(id)) return '전체'
  const category = categoryStore.categories.find(cat => cat.pk === id)
  return category ? category.fields.name : '전체'
})

// URL params에서 categoryId 가져오기 (반응형)
const categoryId = computed(() => parseInt(route.params.categoryId))

// 필터링된 책 목록 계산 (카테고리 + 키워드)
const getFilteredBooks = () => {
  const parsedCategoryId = categoryId.value

  if (!Array.isArray(bookStore.books)) return []

  return bookStore.books.filter(book => {
    const categoryMatch = isNaN(parsedCategoryId) || book.category === parsedCategoryId
    const keywordMatch = !keyword.value ||
      book.title.toLowerCase().includes(keyword.value.toLowerCase()) ||
      book.author.toLowerCase().includes(keyword.value.toLowerCase())
    return categoryMatch && keywordMatch
  })
}

const isActive = (pk) => {
    return pk === categoryId.value || (isNaN(categoryId.value) && pk === 0)
}
</script>

<style scoped>
.booklistview {
    display: flex;
    flex-direction: column;
}

.booklistview h1 {
    font-size: 28px;
}

.category-nav {
    display: flex;flex-direction: column-reverse;
    align-items: flex-end;
    margin: 30px 0 0px;gap: 12px;
    border-bottom: 1px solid #dedede;
}

.category-nav .categories-wrap {
    display: flex;width: 100%;
}

.category-nav .categories-wrap>a:first-child {
    border-left: 1px solid #dedede;
}

.category-nav .categories-wrap>a {
    font-size: 14px;
    padding: 8px 20.4px;
    background: #f6f6f6;
    border: 1px solid #dedede;
    border-left: unset;
    border-bottom: unset;
}

.category-nav .categories-wrap>a.active {
    background: #2d7c4a;
    color: #fff;
}

.search-wrap{
    display: flex;justify-content: space-between;align-items: center;
}
.category-name{
    margin: 20px 0;color: #3d3c3f;
}
.category-name .name{font-size:18px;font-weight: 600;margin-right: 4px;}

.search-wrap input {
    border: 1px solid #ddd;
    height: 35px;
    width: 250px;
    padding-left: 15px;
    outline: none;
}

.context-wrap {
    display: flex;
    flex-wrap: wrap;
    /* grid-template-columns: repeat(6, 1fr); */
    gap: 20px 12px;
}

.context-wrap>li {
    width: 23.8%;
    transition: all 0.3s ease;
    padding: 8px;
    display: flex;flex-direction: column;
    gap: 8px;
    cursor: pointer;
}

.context-wrap>li .img {
    border: 1px solid #eee;
    height: 220px;
    overflow: hidden;
    border-radius: 5px 12px 12px 5px;
}

.text-wrap h3 {
    font-size: 16px;
    color: #3d3c3f;
}

.text-wrap p {
    font-size: 14px;
    color: #80888a;
}

/* 호버 이펙트 */
.context-wrap>li:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
}

/* 이미지 호버 이펙트 */
.context-wrap>li .img {
    border: 1px solid #eee;
    height: 260px;
    overflow: hidden;
    border-radius: 5px 12px 12px 5px;
    transition: all 0.3s ease;
    position: relative;
}

.context-wrap>li:hover .img {
    transform: scale(1.02);
}

.context-wrap>li:hover .img img {
    transform: scale(1.05);
    filter: brightness(1.1);
}

.context-wrap>li .img img {
    transition: all 0.4s ease;
}

/* 텍스트 호버 이펙트 */
.text-wrap h3 {
    font-size: 16px;
    color: #3d3c3f;
    transition: all 0.3s ease;
}

.text-wrap p {
    font-size: 14px;
    color: #80888a;
    transition: all 0.3s ease;
}
</style>