import json
import requests
import openai
from pathlib import Path
from django.conf import settings
import wikipediaapi
from pydantic import BaseModel
from books.models import Book, Author
from typing import Optional, Dict


# OpenAI 클라이언트 (최상단 한 번만 생성)
client = openai.OpenAI()

wiki_wiki = wikipediaapi.Wikipedia(
    language='ko',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
)

def normalize_author_name(name: str) -> str:
    """작가명에 '(작가)'를 붙여 위키피디아 페이지 이름 보정"""
    return f"{name} (작가)"

def get_wikipedia_image(title: str) -> Optional[str]:
    """위키피디아에서 대표 이미지 URL을 가져옵니다."""
    URL = "https://ko.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "format": "json",
        "piprop": "original",
    }
    try:
        response = requests.get(URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for _, page_data in pages.items():
            original = page_data.get("original", {})
            if original:
                return original.get("source")
    except Exception as e:
        print(f"[ERROR] Wikipedia 이미지 호출 실패: {e}")
    return None

def get_wikipedia_content(author_name: str) -> Optional[Dict]:
    """작가명 보정 후 위키피디아 요약 정보를 반환합니다."""
    suffixes = [' (작가)', ' (소설가)', ' (문학가)', ' (인물)']
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

def generate_author_gpt_info(book: Book, wiki_summary: str) -> tuple[str, str]:
    """GPT에 작가 소개 및 대표작 3권 이상 리스트 생성 요청"""
    prompt = f"""
    아래는 작가에 대한 정보입니다. 이 정보를 바탕으로 다음 내용을 JSON 형식으로 작성해 주세요.

    1. 작가 소개: 3~5줄 분량으로, 작가의 주요 특징과 업적을 포함
    2. 대표 작품 목록: 3권 이상의 작품 제목을 콤마(,)로 구분하여 나열

    [작가 이름]: {book.author}
    [책 제목]: {book.title}
    [위키피디아 요약]: 
    {wiki_summary}

    응답 형식:
    {{
        "author_info": "작가 소개 문단",
        "author_works": "대표작1, 대표작2, 대표작3"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "작가 소개와 대표 작품 목록을 JSON 형식으로 출력하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600,
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("author_info", ""), data.get("author_works", "")
    except Exception as e:
        print(f"[ERROR] GPT 작가 정보 생성 실패: {e}")
        return "작가 정보를 가져오지 못했습니다.", "대표 작품 목록을 가져오지 못했습니다."

def process_author_info_by_book_pk(book_pk: int) -> Optional[Dict]:
    """책 PK로 작가 정보 수집 후 DB 반영 및 딕셔너리 반환"""
    try:
        book = Book.objects.get(pk=book_pk)
    except Book.DoesNotExist:
        print(f"[ERROR] Book(pk={book_pk}) 존재하지 않음")
        return None

    raw_author_name = str(book.author)
    wiki_author_name = normalize_author_name(raw_author_name)
    wiki_data = get_wikipedia_content(wiki_author_name)

    if not wiki_data:
        print(f"[WARN] Wikipedia 데이터 없음: {wiki_author_name}")
        wiki_summary = ""
        wiki_title = wiki_author_name
    else:
        wiki_summary = wiki_data.get("summary", "")
        wiki_title = wiki_data.get("title", wiki_author_name)

    # 이미지 다운로드 및 저장
    img_url = get_wikipedia_image(wiki_title)
    photo_path = None
    if img_url:
        try:
            response_img = requests.get(img_url, timeout=5)
            response_img.raise_for_status()

            output_dir = Path(settings.MEDIA_ROOT) / "author_profiles"
            output_dir.mkdir(parents=True, exist_ok=True)

            filename = f"author_{book.pk}_{Path(img_url).name}"
            file_path = output_dir / filename
            file_path.write_bytes(response_img.content)

            photo_path = f"author_profiles/{filename}"
            print(f"[DEBUG] 이미지 저장됨: {file_path}")
        except Exception as e:
            print(f"[WARN] 이미지 저장 실패: {e}")

    # GPT를 통한 작가 소개 및 대표작 생성
    author_info, author_works = generate_author_gpt_info(book, wiki_summary)

    # Book 모델 업데이트
    book.author_info = author_info
    book.author_works = author_works
    if photo_path:
        book.author_profile_img = photo_path
    book.save()

    # Author 모델 업데이트 또는 생성
    author_obj, _created = Author.objects.get_or_create(name=raw_author_name)
    author_obj.bio = wiki_summary
    if photo_path:
        author_obj.photo = photo_path
    author_obj.save()

    return {
        "author_name": raw_author_name,
        "author_info": author_info,
        "author_works": author_works,
        "author_photo_url": photo_path and str(settings.MEDIA_URL) + photo_path or None,
        "wiki_url": wiki_data.get("url") if wiki_data else None,
    }
