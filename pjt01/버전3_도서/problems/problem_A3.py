import os                       # 운영 체제와 상호작용하기 위한 라이브러리
import requests                 # HTTP 요청을 보내기 위한 라이브러리
from gtts import gTTS           # 텍스트를 음성으로 변환하기 위한 라이브러리
from dotenv import load_dotenv  # 환경 변수 로드를 위한 라이브러리


load_dotenv()

MY_TTBKEY = os.getenv('MY_API_KEY')
ALADIN_SEARCH_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'

# 3. 도서 제목 가져오는 함수 정의
def fetch_book_title(keyword):
    url = ALADIN_SEARCH_URL
    params = {
        "TTBKey": MY_TTBKEY,    # API 키
        "Query": keyword,       # 검색 키워드
        "output": "js",         # 응답 형식
        "Version": "20131101",  # API 버전
    }

    data = requests.get(url, params=params).json()

    # 3.3 [ 첫 번째 도서 제목 추출하여 title 변수에 저장하기 ]
    title = data['item'][0]['title']

    return title


# 4. TTS 파일 생성 함수 정의
def create_tts_file(keyword, output_file):
    # 4.1 [ 첫 번째 도서 제목 가져오기 ]
    title = fetch_book_title(keyword)  # fetch_book_title 함수 호출로 도서 제목 가져오기
    
    if title:
        # 4.2 [ gTTS를 사용해 title의 내용으로 음성 파일 생성하기 ]
        tts = gTTS(text=title, lang='ko', slow=False) 
        tts.save(output_file)  # 음성 파일 저장
        print(f"음성 파일이 {output_file}로 저장되었습니다.")
    else:
        print("도서 제목을 가져오는데 실패했습니다.")


# 함수 실행 (output 폴더가 없으면 생성 필요)
if __name__ == '__main__':
    create_tts_file("자격증", "output/book_title.mp3")
