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
                <input type="text" v-model="keyword" placeholder="검색어를 입력하세요...">
            </div>
            <ul class="context-wrap">
                <li v-for="book in filterBooks" :key="book.id">
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

// URL params에서 categoryId 가져오기 (반응형)
const categoryId = computed(() => parseInt(route.params.categoryId))

// 필터링된 책 목록 계산 (카테고리 + 키워드)
const filterBooks = computed(() => {
    const parsedCategoryId = categoryId.value

    return bookStore.books.filter(book => {
        // 카테고리 필터링
        const categoryMatch = isNaN(parsedCategoryId) || book.category === parsedCategoryId

        // 키워드 필터링 (제목, 저자)
        const keywordMatch = !keyword.value ||
            book.title.toLowerCase().includes(keyword.value.toLowerCase()) ||
            book.author.toLowerCase().includes(keyword.value.toLowerCase())

        return categoryMatch && keywordMatch
    })
})

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
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin: 30px 0 30px;
    border-bottom: 1px solid #dedede;
}

.category-nav input {
    border: 1px solid #ddd;
    height: 40px;
    width: 300px;
    padding-left: 20px;
    border-bottom: unset;
    outline: none;
}

.category-nav .categories-wrap {
    display: flex;
}

.category-nav .categories-wrap>a:first-child {
    border-left: 1px solid #dedede;
}

.category-nav .categories-wrap>a {
    font-size: 14px;
    padding: 8px 12px;
    background: #f6f6f6;
    border: 1px solid #dedede;
    border-left: unset;
    border-bottom: unset;
}

.category-nav .categories-wrap>a.active {
    background: #ff9a66;
    color: #fff;
}

.context-wrap {
    display: flex;
    flex-wrap: wrap;
    /* grid-template-columns: repeat(6, 1fr); */
    gap: 40px 24px;
}

.context-wrap>li {
    width: 15%;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.context-wrap>li .img {
    border: 1px solid #eee;
    height: 260px;
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

.context-wrap>li {
    width: 15%;
    display: flex;
    flex-direction: column;
    gap: 8px;
    transition: all 0.3s ease;
    cursor: pointer;
    border-radius: 12px;
    padding: 8px;
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