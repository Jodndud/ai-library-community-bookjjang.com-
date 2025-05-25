import json
import requests
import openai
from pathlib import Path
from django.conf import settings
import wikipediaapi
from pydantic import BaseModel
from books.models import Book  # ✅ Book 모델 import 추가
from django.core.files import File 

class AuthorInfo(BaseModel):
    author_info: str
    author_works: str


wiki_wiki = wikipediaapi.Wikipedia(
    language='ko',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
)


# ✅ 인자를 book_author → book_pk로 수정
def get_wikipedia_image(book_pk):
    try:
        book = Book.objects.get(pk=book_pk)
    except Book.DoesNotExist:
        return None

    URL = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": book.author,
        "prop": "pageimages",
        "format": "json",
        "piprop": "original",
    }
    response = requests.get(URL, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for _, page_data in pages.items():
            original = page_data.get("original", {})
            if original:
                return original.get("source")
    return None


def get_wikipedia_content(book_author):
    page = wiki_wiki.page(book_author)
    if not page.exists():
        return None
    return {
        "summary": page.summary,
        "url": page.fullurl,
    }


def process_wikipedia_info(book):
    wiki_data = get_wikipedia_content(book.author)
    if wiki_data:
        wiki_summary = wiki_data.get("summary", "")
        img_url = get_wikipedia_image(book.pk)

        if not book.pk:
            book.save()

        if img_url:
            response_img = requests.get(img_url)
            if response_img.status_code == 200:
                output_dir = Path(settings.MEDIA_ROOT) / "author_profiles"
                output_dir.mkdir(parents=True, exist_ok=True)

                original_filename = Path(img_url).name
                file_name = f"author_{book.pk}_{original_filename}"
                file_path = output_dir / file_name

                file_path.write_bytes(response_img.content)

                # 📌 상대 경로 (문자열)도 따로 저장하고
                image_path = str(Path("author_profiles") / file_name)

                # ✅ Author 객체에는 파일 객체로 저장
                with open(file_path, "rb") as f:
                    django_file = File(f)
                    book.author_profile_img = image_path  # Book에는 문자열 저장
                    book.save()

                    return wiki_summary, django_file  # photo에는 File 객체 넘김
    else:
        wiki_summary = "위키피디아에서 정보를 찾을 수 없습니다."
    return wiki_summary, None


def generate_author_gpt_info(book, wiki_summary):
    prompt = f"""
        <도서 정보>
            책 제목: {book.title}
            작가: {book.author}
            위키피디아 요약: {wiki_summary}
        </도서 정보>
        """
    try:
        client = openai.OpenAI()
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """ 프롬프트 작성하기
                                    답변 예시 : 
                                    {{ 
                                        "author_info": "작가 소개 예시입니다.",
                                        "author_works": "작품1, 작품2, 작품3"
                                    }}
                            .""",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=AuthorInfo,
            max_tokens=2040,
            temperature=0.5,
        )

        json_response = response.choices[0].message.content
        print(json_response)
        data = json.loads(json_response)
        author_info = data.get(
            "author_info", "작가 정보를 가져오지 못했습니다."
        )
        author_works = data.get(
            "author_works", "작품 목록을 가져오지 못했습니다."
        )
    except Exception as e:
        print("GPT 작가 정보 생성 에러:", e)
        author_info = "작가 정보를 가져오지 못했습니다."
        author_works = "작품 목록을 가져오지 못했습니다."
    return author_info, author_works

