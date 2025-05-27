import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import { useAccountStore } from '@/stores/accounts'

export const useReviewStore = defineStore('review', () => {
  const accountStore = useAccountStore()
  const router = useRouter()

  const API_URL = 'http://127.0.0.1:8000/api/v1/books'
  const BASE_URL = 'http://127.0.0.1:8000'
  const reviews = ref([])
  const reviewDetail = ref([])

  const isLoading = ref(false)

  // 모든 책의 리뷰 목록 불러오기
  const reviewsList = function () {
    axios({
      method: 'get',
      url: `${API_URL}/threads/`,
    })
      .then((res) => {
        // console.log(res.data)
        reviews.value = res.data
      })
      .catch((err) => {
        console.log('리뷰 불러오기 실패:', err.message)
      })
  }


  // 특정 책의 리뷰 목록 불러오기
  const fetchReviews = function (bookId) {
    axios({
      method: 'get',
      url: `${API_URL}/${bookId}/threads/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        // console.log(res.data.filter(review => review.book === bookId))
        reviews.value = res.data.filter(review => review.book === bookId)
      })
      .catch((err) => {
        console.error('리뷰 불러오기 실패:', err.response?.data || err.message)
      })
  }

  // 특정 책에 대한 리뷰 작성
  const createReview = function (bookId, reviewData) {
    console.log('로딩중')
    isLoading.value = true
    // reviewData에 rating, title, content가 모두 포함되어야 함
    axios({
      method: 'post',
      url: `${API_URL}/${bookId}/threads/`,
      data: reviewData,
      headers: {
        'Authorization': `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        const newReview = res.data
        fetchReviews(bookId)
        // 완료 후 이동
        router.push({ name: 'reviewDetail', params: { bookId: bookId, reviewId: newReview.id } })
      })
      .catch((err) => {
        console.log('리뷰 등록 실패:', err)
      })
      .finally(() => {
        isLoading.value = false  // 로딩 종료
      })
  }

  // 리뷰 상세 조회
  const detailReview = function (bookId, reviewId) {
    axios({
      method: 'get',
      url: `${API_URL}/${bookId}/threads/${reviewId}/`,
    })
      .then((res) => {
        // console.log(res.data)
        reviewDetail.value = res.data
      })
      .catch((err) => {
        console.log('리뷰 상세 불러오기 실패:', err)
      })
  }


  const comments = ref([])

  // 댓글 불러오기
  const fetchComments = function (bookId, reviewId) {
    axios({
      method: 'get',
      url: `${API_URL}/${bookId}/threads/${reviewId}/comments/`,
    })
      .then((res) => {
        // console.log(res.data)
        comments.value = res.data
      })
      .catch((err) => {
        console.error('댓글 불러오기 실패:', err.response?.data || err.message)
      })
  }

  const createComment = function (bookId, reviewId, payload) {
    return axios({
      method: 'post',
      url: `${API_URL}/${bookId}/threads/${reviewId}/comments/`,
      headers: {
        'Authorization': `Token ${accountStore.token}`
      },
      data: payload
    })
      .then((res) => {
        const newComment = res.data

        // 댓글을 특정 리뷰에 바로 반영하려면
        const review = reviews.value.find(r => r.id === reviewId)
        if (review) {
          // comments를 새 배열로 할당해 반응성 유지
          review.comments = [...review.comments, newComment]
        }

        return newComment
      })
      .catch((err) => {
        console.error('댓글 작성 실패:', err.response?.data || err.message)
        throw err
      })
  }

  // 작가 정보 조회
  const authorInfo = function (bookId) {
    return axios({
      method: 'get',
      url: `${API_URL}/${bookId}/author/`,
    })
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => {
        console.log(err.message)
      })
  }

  // 좋아요 기능
  const reviewLike = function (bookId, reviewId) {
    return axios({
      method: 'post',
      url: `${API_URL}/${bookId}/threads/${reviewId}/like/`,
    })
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => {
        console.log(err.message)
      })

  }

  return {
    reviews, reviewDetail, BASE_URL, isLoading,
    fetchReviews, createReview, detailReview, reviewsList,
    fetchComments, createComment,
    authorInfo, reviewLike,
  }
})
