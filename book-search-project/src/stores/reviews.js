// stores/reviews.js

import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useReviewStore = defineStore('review', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const reviews = ref([
    {
        "id": 1,
        "book": 3,
        "cover_image": 'https://picsum.photos/250/250',
        "user": "user1",
        "title": "좋은 책이에요",
        "content": "감동 받았습니다.",
        "created_at": "2025-05-19",
        "comments": [
            {
                "id": 1,
                "user": "user2",
                "content": "저도 감동이었어요!",
                "created_at": "2025-05-19"
            },
            {
                "id": 2,
                "user": "doriconi",
                "content": "저도요!",
                "created_at": "2025-05-24"
            },
        ]
    },
    {
        "id": 2,
        "book": 1,
        "cover_image": 'https://picsum.photos/250/250',
        "user": "asdf",
        "title": "눈물 실화냐 ㅠㅠ",
        "content": "감동 받았습니다.",
        "created_at": "2025-05-19",
        "comments": []
    },
  ])

  // 특정 책의 리뷰 목록 불러오기
  const fetchReviews = function(bookId) {
    axios({
      method: 'get',
      url: `${API_URL}/threads/${bookId}/reviews/`,
    })
    .then((res) => {
      reviews.value = res.data
    })
    .catch((err) => {
      console.error('리뷰 불러오기 실패:', err.response?.data || err.message)
    })
  }

  // 특정 책에 대한 리뷰 작성
  const createReview = function(bookId, reviewData) {
    axios({
      method: 'post',
      url: `${API_URL}/books/${bookId}/reviews/`,
      data: reviewData,
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then((res) => {
      reviews.value.push(res.data)
      alert('리뷰가 등록되었습니다.')
    })
    .catch((err) => {
      console.error('리뷰 등록 실패:', err.response?.data || err.message)
      alert('리뷰 등록 중 오류가 발생했습니다.')
    })
  }

  return {
    reviews,
    fetchReviews,
    createReview,
  }
})
