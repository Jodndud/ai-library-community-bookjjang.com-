import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useReviewStore } from '@/stores/reviews'

export const useBookListStore = defineStore('books', () => {
  const accountStore = useAccountStore()
  
  const API_URL = 'http://127.0.0.1:8000'
  const books = ref([])

  // 전체 책 리스트 조회
  const FetchBookList = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/`,
    })
      .then((res) => {
        // console.log(res.data)
        books.value = res.data
      })
      .catch((err) => {
        console.error(err.message)
      })
  }

  // 상세 책 리스트 조회
  const DetailBookList = function (bookId) {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/${bookId}/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        books.value = res.data
      })
      .catch((err) => {
        console.log(err.data)
      })
  }

  // 리뷰 조회 함수 추가
  const FetchBookReviews = function (bookId) {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/books/${bookId}/threads/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        // reviewStore에 직접 저장하거나 return
        const reviewStore = useReviewStore()
        reviewStore.reviews = res.data
      })
      .catch((err) => {
        console.error('리뷰 불러오기 실패:', err.message)
      })
  }

  return {
    books,
    FetchBookList, DetailBookList, FetchBookReviews
  }
})
