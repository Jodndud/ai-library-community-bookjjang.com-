import json
import requests
import openai
import re
from pathlib import Path
from django.conf import settings
import wikipediaapi
from pydantic import BaseModel
from books.models import Book, Author
from typing import Optional, Dict, Tuple
from bs4 import BeautifulSoup


class AuthorInfo(BaseModel):
    author_info: str
    author_works: str


wiki_wiki = wikipediaapi.Wikipedia(
    language='ko',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
)


def get_wikipedia_content(author_name: str) -> Optional[Dict]:
    page = wiki_wiki.page(author_name)
    if not page.exists():
        return None
    return {
        "summary": page.summary,
        "url": page.fullurl,
    }


def get_commons_image(author_name: str) -> Optional[str]:
    """
    위키미디어 커먼즈 API를 사용해 작가 이름으로 이미지 검색 후
    대표 이미지 URL을 반환합니다.
    """
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": author_name,
        "gsrlimit": 1,  # 가장 관련 높은 1개 결과만
        "prop": "imageinfo",
        "iiprop": "url",
    }
    headers = {
        "User-Agent": "MyBookApp/1.0 (your-email@example.com)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for _, page in pages.items():
            imageinfo = page.get("imageinfo", [])
            if imageinfo:
                return imageinfo[0].get("url")
    except Exception as e:
        print(f"[ERROR] Wikimedia Commons 이미지 요청 실패: {e}")
    return None


def save_author_image_for_author(author: Author, img_url: str) -> Optional[str]:
    headers = {
        "User-Agent": "MyBookApp/1.0 (youremail@example.com) Python requests",
        "Referer": "https://ko.wikipedia.org/"
    }
    try:
        response_img = requests.get(img_url, headers=headers, timeout=5)
        response_img.raise_for_status()
        output_dir = Path(settings.MEDIA_ROOT) / "author_profiles"
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"author_{author.id}_{Path(img_url).name}"
        file_path = output_dir / filename
        file_path.write_bytes(response_img.content)
        return f"author_profiles/{filename}"
    except Exception as e:
        print(f"[WARN] 이미지 저장 실패: {e}")
        return None


def extract_json_from_response(response_text: str) -> dict:
    try:
        # 코드블록 마크다운이나 불필요한 문자 제거
        json_text_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if not json_text_match:
            return {}
        json_text = json_text_match.group()
        return json.loads(json_text)
    except Exception as e:
        print(f"[ERROR] JSON 파싱 실패: {e}")
        return {}


def generate_author_gpt_info_for_author(author: Author, wiki_summary: str) -> Tuple[str, str]:
    prompt = f"""
아래 작가 정보를 참고하여 작가 소개와 대표작 목록을 JSON 형식으로 생성해주세요.

<작가 정보>
작가 이름: {author.name}
위키피디아 요약: {wiki_summary}

응답 예시:
{{
  "author_info": "작가 소개 문장입니다. 작가의 업적과 특징을 포함해주세요.",
  "author_works": "대표작1, 대표작2, 대표작3"
}}
    """
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "작가 소개와 대표작을 위 JSON 형식으로 출력해주세요."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.5,
        )
        json_response = response.choices[0].message.content
        print("[GPT 응답]:", json_response)
        data = extract_json_from_response(json_response)

        author_info = data.get("author_info", "작가 정보를 가져오지 못했습니다.")
        author_works = data.get("author_works", "")

        # 기본 예시 값은 빈 문자열로 처리
        # 대표작이 '작품1', '작품2' 같은 의미 없는 값으로 보일 경우 빈 문자열로 처리
        if re.fullmatch(r"(작품\d+(,\s*작품\d+)*|\s*)", author_works.strip()):
            author_works = ""


        return author_info, author_works

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[ERROR] GPT 작가 정보 생성 실패 (Author 기반): {e}")
        return "작가 정보를 가져오지 못했습니다.", ""


def process_wikipedia_info_for_author(author: Author) -> str:
    wiki_data = get_wikipedia_content(author.name)
    if wiki_data:
        wiki_summary = wiki_data.get("summary", "")
        image_url = get_commons_image(author.name)

        if image_url:
            photo_path = save_author_image_for_author(author, image_url)
            if photo_path:
                author.photo = photo_path
                author.save()
    else:
        wiki_summary = "위키피디아에서 정보를 찾을 수 없습니다."

    return wiki_summary


def process_author_info_by_book_pk(book_pk: int) -> Optional[dict]:
    book = Book.objects.filter(pk=book_pk).first()
    if not book:
        return None

    author, _ = Author.objects.get_or_create(name=book.author)
    wiki_data = get_wikipedia_content(author.name)

    wiki_summary = wiki_data.get("summary", "") if wiki_data else "위키피디아에서 정보를 찾을 수 없습니다."
    author_info, author_works = generate_author_gpt_info_for_author(author, wiki_summary)

    author.bio = author_info
    author.save()

    author_photo_url = f"{settings.MEDIA_URL}{author.photo}" if author.photo else None
    wiki_url = wiki_data.get("url", "") if wiki_data else ""

    return {
        "author_name": author.name,
        "author_info": author.bio,
        "author_works": author_works,
        "author_photo_url": author_photo_url,
        "wiki_url": wiki_url,
    }
