from openai import OpenAI
from PyPDF2 import PdfReader
import io
import asyncpg
from typing import List
import asyncio
from datetime import datetime
from config import *

import requests

count_requests_in_day = 0

# if count_requests_in_day < 45:
#     client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=TOKEN_DEPS_THREE,
#     )
# elif count_requests_in_day < 90:
#     client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=TOKEN_DEPS_TWO,
#     )
# elif count_requests_in_day < 135:
#     client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=TOKEN_DEPS_THREE,
#     )

def get_client():
    """Возвращает клиента OpenAI с нужным токеном в зависимости от количества запросов"""
    global count_requests_in_day
    if count_requests_in_day < 45:
        api_key = TOKEN_DEPS_FOUR
    elif count_requests_in_day < 90:
        api_key = TOKEN_DEPS_THREE
    elif count_requests_in_day < 135:
        api_key = TOKEN_DEPS_TWO
    elif count_requests_in_day < 180:
        api_key = TOKEN_DEPS_ONE
    else:
        # Сбрасываем счетчик, если достигли лимита всех токенов
        count_requests_in_day = 0
        api_key = TOKEN_DEPS_THREE
    
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

client = get_client()



def extract_text_from_pdf(file: bytes) -> str:
    """Принимает PDF как bytes, возвращает извлеченный текст."""
    reader = PdfReader(io.BytesIO(file))
    text = " ".join([page.extract_text() for page in reader.pages])
    return text



async def generating_answer_without_vacancy(pdf_file, temp = 0.8):
    global count_requests_in_day

    client = get_client()

    count_requests_in_day+=1

    logger.info(f"[{datetime.now()}] Число запросов за день: {count_requests_in_day}") 

    # prompt = f"""Ты — профессиональный HR-консультант с 10-летним опытом подбора персонала. 
    # Проанализируй резюме кандидата и предложи конкретные улучшения. Отвечай развернуто и полностью, однако твой ответ должен содержать не более 2500 символов. 
    # Отвечай очень грамотно со знанием русского языка. 
    # Возможно входной файл будет низкого качества, не расстраивайся и не додумывай ничего нового, отвечай только по тому, что ты видишь. Если ты не можешь прочитать файл, ответь, что ты не можешь увидеть файл. 
    # К датам не придирайся, у людей могли быть опечатки. Не повторяй то же самое, что есть в резюме, отвечай только аналитику.
    # Жесткое правило: ответь с красивым оформлением со стикерами, подходящими для telegram чата, но без markdown разметки. Не используй '#'.
    # Из форматирования текса используй только жирный шрифт, не используй курсив.
    # Структура ответа:
    # 1. Анализ образования: релевантно ли для целевой должности или нет. Почему?
    # 2. Анализ дополнительных курсов, если они есть: Соответствуют ли они требованиям позиции? Какие навыки подтверждают?
    # 3. Анализ опыта работы: Есть ли конкретные метрики и достижения (KPI, рост продаж, успешные проекты)?
    # 4. Анализ инструментов и навыков: Достаточно ли их для должности? Какие ключевые отсутствуют? Соответствуют ли навыки заявленной в резюме должности?
    # 5. Насколько опыт и навыки соответствуют заявленной позиции? Какие пробелы нужно закрыть?
    # 6. Общий вывод
    # 7. На какую позицию может претендовать кандидат: junior, middle, senior
    # 8. Оценка резюме по шкале от 1 до 10.
    # 9. Рекомендации по доработке.
    # Резюме для анализа ниже :
    # {pdf_file}
    # """
    prompt = f"""
        Ты — HR-эксперт с 10+ лет опыта в подборе IT-специалистов. Проведи профессиональный аудит резюме и дай конкретные рекомендации по улучшению.

        **Основные правила:**
        1. Формат ответа: Telegram-сообщение (без Markdown, только emoji + жирный текст. Не используй одиночные '*')
        2. Объем: 2000-2500 символов
        3. Тон: профессиональный, но дружелюбный
        4. Основа: только факты из резюме (без домыслов)

        **Структура анализа (используй эти emoji для разделов):**
        🎓 **Образование** 
        - Релевантность для целевой позиции
        - Пробелы/сильные стороны
        - Рекомендации по доп.образованию

        📚 **Курсы и сертификаты** (если есть)
        - Соответствие требованиям рынка
        - Какие навыки подтверждают
        - Ценность для работодателя

        💼 **Опыт работы**
        - Конкретные достижения (цифры, проекты)
        - Пропущенные метрики (что стоит добавить)
        - Карьерная прогрессия

        🛠 **Технические навыки**
        - Соответствие позиции
        - Ключевые недостающие технологии
        - Баланс hard/soft skills

        📊 **Соответствие рынку**
        - Уровень (Junior/Middle/Senior)
        - Конкурентоспособность зарплатных ожиданий
        - ТОП-3 недостатка для целевой позиции

        🌟 **Итоговая оценка**
        - Общий балл (1-10)
        - Потенциал роста
        - Срочные/долгосрочные рекомендации

        **Стиль оформления:**
        - Используй emoji для визуального разделения
        - Жирный текст для заголовков (без #)
        - Маркированные списки вместо сплошного текста
        - Не более 3-5 пунктов в каждом разделе

        **Важно:**
        - Если текст нечитаем — сообщи об этом сразу
        - Не повторяй содержание резюме дословно
        - Давай конкретные примеры улучшений
        - Избегай общих фраз ("улучшите резюме")

        Резюме для анализа:
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

async def bd_user_add(user_id: str, name: str, username: str):
    conn = await get_db_connection()
    try:
        await conn.execute(
            "INSERT INTO users (user_id, name, username) VALUES ($1, $2, $3)",
            user_id, name, username
        )
    finally:
        await conn.close()

async def check_and_add_user(user_id: str, name: str, username: str):
    try:
        users_list = await bd_user()
        print(f"User {user_id} exists: {user_id in users_list}")
        if user_id not in users_list:
            await bd_user_add(user_id, name, username)
            print(f"User {user_id} added to DB")
    except Exception as e:
        print(f"Error in check_and_add_user: {e}")
        raise

import asyncpg

async def load_vacancies_for_analysis(vacancy_category):
    """
    Загружает вакансии и пользовательские выборки из БД,
    возвращает кортеж (vacancies_cache, user_selections)
    """
    conn = None
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # 1. Загрузка вакансий
        records = await conn.fetch(
            f"SELECT title, salary, skills, location, experience, link FROM vacans WHERE new_category like '%{vacancy_category}' and date >= CURRENT_DATE - INTERVAL '3 day'"
        )
        logger.info(f"[{datetime.now()}] Скачали последние вакансии для анализа в функции Прожарки резюме") 
        return records
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Ошибка загрузки данных: {e}") 
        return {}, {}
    finally:
        if conn:
            await conn.close()


async def hot_resume(pdf_text, vacancy_category,  temp = 0.8):
    global count_requests_in_day

    client = get_client()

    count_requests_in_day+=1

    logger.info(f"[{datetime.now()}] Число запросов за день: {count_requests_in_day}") 

    logger.info(f"[{datetime.now()}] Зашли в функцию hot_resume") 
    
    vacancies = await load_vacancies_for_analysis(vacancy_category)
    logger.info(f"[{datetime.now()}] Перешли к промту") 
    prompt = f"""
        Ты — HR-эксперт с 10+ лет опыта в IT-рекрутинге. 
        Проанализируй резюме для позиции {vacancy_category} и дай рекомендации, которые увеличат шансы на отклик на 50%. 

        **Жесткие правила:**
        1. Только факты из резюме (не додумывай)
        2. Сравнивай с вакансиями {vacancies[:25]}, Не используй в ответах тег <record>, используй только названия и ссылки
        3. Пиши как личный консультант (без шаблонов)
        4. Макс. 2500 символов
        5. Из тегов используй только <b> для выделения жирного текста, строго не используй курсив и теги <think>. Не используй в ответе '#'.

        **Структура ответа (Telegram-форматирование):**
        🎯 <b>Главная проблема</b>: 1-2 предложения
        📊 <b>Число подходящих вакансий</b>: "За последнюю неделю было X подходящих вашему описанию вакансий"
        💼 <b>Соответствие роли</b>: 3 пункта (совпадение/нехватка)
        💰 <b>Зарплатный потолок</b>: "Без доработок: X ₽ | С исправлениями: Y ₽". Если вакансий меньше 5, то пропусти этот пункт.
        🛠 <b>ТОП-3 исправления</b> (конкретные примеры):
        1. Заменить "фраза из резюме" → "оптимизированная версия"
        2. Добавить навык "самый частый skill из вакансий"
        3. Удалить "нерелевантный пункт"
        📈 <b>Быстрый чек</b>: "После правок +% откликов"
        🔗 <b>Ресурсы</b>: Совет что необходимо выучить
        4. Наиболее релевантные вакансии за последнюю неделю: ссылки только из текстов вакансий, который тебе прислали.

        Резюме:
        {pdf_text}
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
    text = completion.choices[0].message.content
    logger.info(f"[{datetime.now()}] Полученная генерация {text}") 

    return text
