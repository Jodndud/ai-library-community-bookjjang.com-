import json
import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_dalle_prompt(book, diary_emotion_text):
    """
    책 정보와 감정 텍스트를 받아 DALL·E 이미지 생성을 위한 프롬프트와 스타일을 반환합니다.
    실패 시 None을 반환합니다.
    """
    prompt = f"""
    다음은 독서 다이어리에서 감정을 분석하고, 키워드와 이미지 생성 프롬프트를 생성하는 작업입니다.

    <도서 정보>
    제목: {book.title}
    저자: {book.author}
    
    <감정 표현>
    {diary_emotion_text}
    
    아래와 같은 형식으로 출력해 주세요:
    {{
        "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
        "prompt": "이 키워드들을 바탕으로 생성된 DALL·E용 프롬프트입니다.",
        "style": "미니멀한 일러스트 스타일"
    }}
    """
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "도서 감정 분석 및 이미지 생성 프롬프트 작성기"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        json_response = response.choices[0].message.content
        data = json.loads(json_response)
        return data["prompt"], data["style"]
    except Exception as e:
        print("프롬프트 생성 실패:", e)
        return None

def generate_cover_image(book, diary_emotion_text):
    """
    책 정보와 감정 텍스트를 받아 AI 이미지 파일을 생성하여 InMemoryUploadedFile로 반환합니다.
    실패 시 None을 반환합니다.
    """
    result = generate_dalle_prompt(book, diary_emotion_text)
    if not result:
        print("generate_dalle_prompt가 None을 반환했습니다.")
        return None
    dalle_prompt, style = result

    full_prompt = f"{dalle_prompt}. 스타일: {style}."
    try:
        client = openai.OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            img_io = io.BytesIO(image_response.content)
            file_name = f"cover_{book.pk}.png"
            return InMemoryUploadedFile(
                file=img_io,
                field_name="cover_img",
                name=file_name,
                content_type="image/png",
                size=len(image_response.content),
                charset=None
            )
        else:
            print("이미지 다운로드 실패:", image_response.status_code)
            return None
    except Exception as e:
        print("DALL·E 이미지 생성 실패:", e)
        return None
