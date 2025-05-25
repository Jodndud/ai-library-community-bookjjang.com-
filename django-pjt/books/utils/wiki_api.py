import json
import requests
import openai
from pathlib import Path
from django.conf import settings
import wikipediaapi
from pydantic import BaseModel
from books.models import Book  # ✅ Book 모델 import

class AuthorInfo(BaseModel):
    author_info: str
    author_works: str

wiki_wiki = wikipediaapi.Wikipedia(
    language='ko',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
)

def get_wikipedia_image(author_name):
    """Wikipedia 이미지 URL 가져오기"""
    URL = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": author_name,
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

def get_wikipedia_content(author_name):
    """Wikipedia 요약 텍스트 가져오기"""
    page = wiki_wiki.page(author_name)
    if not page.exists():
        return None
    return {
        "summary": page.summary,
        "url": page.fullurl,
    }

def process_author_info_by_book_pk(book_pk):
    """책 pk로 저자 정보를 Wikipedia에서 수집하고 저장"""
    try:
        book = Book.objects.get(pk=book_pk)
    except Book.DoesNotExist:
        print(f"[ERROR] Book with pk={book_pk} not found.")
        return None

    author_name = book.author
    wiki_data = get_wikipedia_content(author_name)
    if wiki_data:
        wiki_summary = wiki_data.get("summary", "")
        img_url = get_wikipedia_image(author_name)

        if img_url:
            response_img = requests.get(img_url)
            if response_img.status_code == 200:
                output_dir = Path(settings.MEDIA_ROOT) / "author_profiles"
                output_dir.mkdir(parents=True, exist_ok=True)
                original_filename = Path(img_url).name
                file_name = f"author_{book.pk}_{original_filename}"
                file_path = output_dir / file_name
                file_path.write_bytes(response_img.content)
                book.author_profile_img = str(Path("author_profiles") / file_name)
                print(f"[DEBUG] Saved image: {file_path}")
    else:
        wiki_summary = "위키피디아에서 정보를 찾을 수 없습니다."

    # GPT 작가 정보 생성
    author_info, author_works = generate_author_gpt_info(book, wiki_summary)

    # 저장
    book.author_info = author_info
    book.author_works = author_works
    book.save()
    return {
        "summary": wiki_summary,
        "author_info": author_info,
        "author_works": author_works,
    }

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
                    "content": """프롬프트 작성하기
                        예시:
                        {
                            "author_info": "작가 소개입니다.",
                            "author_works": "작품1, 작품2, 작품3"
                        }
                    """,
                },
                {"role": "user", "content": prompt},
            ],
            response_format=AuthorInfo,
            max_tokens=2040,
            temperature=0.5,
        )
        json_response = response.choices[0].message.content
        data = json.loads(json_response)
        return data.get("author_info", ""), data.get("author_works", "")
    except Exception as e:
        print("GPT 작가 정보 생성 에러:", e)
        return "작가 정보를 가져오지 못했습니다.", "작품 목록을 가져오지 못했습니다."
