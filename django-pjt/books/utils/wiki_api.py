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


def normalize_author_name(name: str) -> str:
    """위키피디아 페이지 이름 보정: 작가 이름에 '(작가)' 추가"""
    return f"{name} (작가)"


def get_wikipedia_image(title):
    """Wikipedia 이미지 URL 가져오기 (title 기준)"""
    URL = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
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
    """Wikipedia 요약 텍스트 가져오기 (작가 식별 보정)"""
    suffixes = [' (작가)', ' (소설가)', ' (문학가)', ' (작가)', ' (인물)']
    possible_titles = [author_name] + [f"{author_name}{suffix}" for suffix in suffixes]

    for title in possible_titles:
        page = wiki_wiki.page(title)
        if page.exists():
            return {
                "summary": page.summary,
                "url": page.fullurl,
                "title": title,
            }
    return None

def process_author_info_by_book_pk(book_pk):
    """책 pk 기반으로 Author 모델까지 반영"""
    try:
        book = Book.objects.get(pk=book_pk)
    except Book.DoesNotExist:
        print(f"[ERROR] Book with pk={book_pk} not found.")
        return None

    raw_author_name = book.author
    wiki_author_name = normalize_author_name(raw_author_name)

    wiki_data = get_wikipedia_content(author_name)
    if wiki_data:
        wiki_summary = wiki_data.get("summary", "")
        wiki_title = wiki_data.get("title", author_name)
        img_url = get_wikipedia_image(wiki_title)

    photo_path = None
    if img_url:
        response_img = requests.get(img_url)
        if response_img.status_code == 200:
            output_dir = Path(settings.MEDIA_ROOT) / "author_profiles"
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = f"author_{book.pk}_{Path(img_url).name}"
            file_path = output_dir / filename
            file_path.write_bytes(response_img.content)
            photo_path = f"author_profiles/{filename}"
            print(f"[DEBUG] Saved image: {file_path}")

    # GPT 작가 소개 생성
    author_info, author_works = generate_author_gpt_info(book, wiki_summary)

    # Book 모델 저장
    book.author_info = author_info
    book.author_works = author_works
    if photo_path:
        book.author_profile_img = photo_path
    book.save()

    # Author 모델에도 저장 또는 생성
    from books.models import Author
    author, created = Author.objects.get_or_create(name=raw_author_name)
    author.bio = wiki_summary
    if photo_path:
        author.photo = photo_path
    author.save()

    return {
        "summary": wiki_summary,
        "author_info": author_info,
        "author_works": author_works,
    }


def generate_author_gpt_info(book, wiki_summary):
    prompt = f"""
    아래는 작가에 대한 정보입니다. 이를 바탕으로 작가 소개와 대표 작품 목록을 만들어 주세요.
    
    [작가 이름] {book.author}
    [책 제목] {book.title}
    [위키피디아 요약]
    {wiki_summary}

    응답 형식:
    {{
        "author_info": "작가 소개 문단 (3~5줄)",
        "author_works": "대표작1, 대표작2, 대표작3"
    }}
    """
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "다음 작가에 대한 소개와 대표 작품 목록을 JSON 형식으로 출력하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500,
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("author_info", ""), data.get("author_works", "")
    except Exception as e:
        print("GPT 작가 정보 생성 에러:", e)
        return "작가 정보를 가져오지 못했습니다.", "작품 목록을 가져오지 못했습니다."
