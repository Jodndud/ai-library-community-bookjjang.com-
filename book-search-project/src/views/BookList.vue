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
                    <RouterLink v-for="category in categoryStore.categories" :key="category.pk"
                        :to="category.pk === 0 ? { name: 'books' } : { name: 'books', params: { categoryId: category.pk } }"
                        :class="{ active: isActive(category.pk) }">
                        {{ category.fields.name }}
                    </RouterLink>
                </div>
                <input type="text" v-model="keyword" placeholder="검색어를 입력하세요...">
            </div>
            <ul class="context-wrap">
                <li v-for="book in filterBooks" :key="book.pk">
                    <RouterLink :to="{ name: 'bookDetail', params: { pk: book.pk } }">
                        <div class="img"><img style="width:100%;height:100%;object-fit: cover;" :src="book.fields.cover"
                                :alt="book.fields.title"></div>
                    </RouterLink>
                    <div class="text-wrap">
                        <RouterLink :to="{ name: 'bookDetail', params: { pk: book.pk } }">
                            <h3>{{ book.fields.title }}</h3>
                        </RouterLink>
                        <p>{{ book.fields.author }}</p>
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
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 16px 32px;
}

.context-wrap>li {
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
</style>