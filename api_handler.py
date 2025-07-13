from openai import OpenAI
from PyPDF2 import PdfReader
import io
import asyncpg
from typing import List
import asyncio
from config import *

import requests

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=TOKEN_DEPS,
)



# def extract_text_from_pdf(file):
#     reader = PdfReader(file)
#     text = " ".join([page.extract_text() for page in reader.pages])
#     return text

def extract_text_from_pdf(file: bytes) -> str:
    """Принимает PDF как bytes, возвращает извлеченный текст."""
    reader = PdfReader(io.BytesIO(file))
    text = " ".join([page.extract_text() for page in reader.pages])
    return text



async def generating_answer_without_vacancy(pdf_file, temp = 0.8):
    prompt = f"""Ты — профессиональный HR-консультант с 10-летним опытом подбора персонала. 
    Проанализируй резюме кандидата и предложи конкретные улучшения. Отвечай развернуто и полностью, однако твой ответ должен содержать не более 2500 символов. 
    Отвечай очень грамотно со знанием русского языка. 
    Возможно входной файл будет низкого качества, не расстраивайся и не додумывай ничего нового, отвечай только по тому, что ты видишь. Если ты не можешь прочитать файл, ответь, что ты не можешь увидеть файл. 
    К датам не придирайся, у людей могли быть опечатки. Не повторяй то же самое, что есть в резюме, отвечай только аналитику.
    Ответь с красивым оформлением со стикерами, подходящими для telegram чата, но без markdown разметки. 
    Из форматирования текса используй только жирный шрифт, не используй курсив.
    Структура ответа:
    1. Анализ образования: релевантно ли для целевой должности или нет. Почему?
    2. Анализ дополнительных курсов, если они есть: Соответствуют ли они требованиям позиции? Какие навыки подтверждают?
    3. Анализ опыта работы: Есть ли конкретные метрики и достижения (KPI, рост продаж, успешные проекты)?
    4. Анализ инструментов и навыков: Достаточно ли их для должности? Какие ключевые отсутствуют? Соответствуют ли навыки заявленной в резюме должности?
    5. Насколько опыт и навыки соответствуют заявленной позиции? Какие пробелы нужно закрыть?
    6. Общий вывод
    7. На какую позицию может претендовать кандидат: junior, middle, senior
    8. Оценка резюме по шкале от 1 до 10.
    9. Рекомендации по доработке.
    Резюме для анализа ниже :
    {pdf_file}
    """

    loop = asyncio.get_event_loop()
    completion = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional
            "X-Title": "<YOUR_SITE_NAME>",      # Optional
            },
            model="deepseek/deepseek-r1-0528:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=temp
        )
    )

    return completion.choices[0].message.content

def hh(vacancy_id):
    vacancy_id = vacancy_id.split('/')[-1]
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    data = requests.get(url).json()
    return data['description']

async def get_db_connection():
    return await asyncpg.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

async def bd_user() -> List[str]:
    conn = await get_db_connection()
    try:
        records = await conn.fetch("SELECT user_id FROM users")
        return [str(record['user_id']) for record in records]
    finally:
        await conn.close()

async def bd_user_add(user_id: str, name: str):
    conn = await get_db_connection()
    try:
        await conn.execute(
            "INSERT INTO users (user_id, name) VALUES ($1, $2)",
            user_id, name
        )
    finally:
        await conn.close()

async def check_and_add_user(user_id: str, name: str):
    try:
        users_list = await bd_user()
        print(f"User {user_id} exists: {user_id in users_list}")
        if user_id not in users_list:
            await bd_user_add(user_id, name)
            print(f"User {user_id} added to DB")
    except Exception as e:
        print(f"Error in check_and_add_user: {e}")
        raise
