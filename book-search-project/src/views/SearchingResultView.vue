<template>
    <div>
        <h1>검색 결과페이지</h1>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const keyword = route.params.value
const type = route.query.type  // 'TOT', 'TITLE', 'AUTHOR'

console.log('검색어:', keyword)
console.log('검색 유형:', type)
</script>

<style scoped>

</style>