from aiogram import Bot, Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import *
from api_handler import *
from aiogram.utils.markdown import hbold, hitalic, hunderline, text, code
# from config import TOKEN_WEATHER
from datetime import datetime
import io
import asyncio
import json
import html
import re
from aiogram.utils.markdown import html_decoration as hd
from bs4 import BeautifulSoup
import re
from markdown import markdown
from config import *

vacanciessss = {}
hr_vacanciess = {}

category_keywords = {
 "Аналитика": {
    "keywords": [
      "аналитик", 'systems_analyst', 'data_analyst', 'business_analyst', 'bi-аналитик', 'бизнес-аналитик', 'marketing_analyst', 
      'bi_developer', 'bi-аналитик, аналитик данных'
    ],
    "subcategories": {
      "Системный аналитик": [
        "системн", "systems_analyst",  "uml"
      ],
      "Бизнес аналитик": [
        "бизнес", "business", 'бизнес-аналитик'
      ],
      "Data аналитик и BI": [
        'data_analyst', 'bi-аналитик', "bi_developer", 'bi-аналитик, аналитик данных'
      ],
      "Продуктовый аналитик": [
        "продуктов", "product", "a/b", "ab test", "a/b test", 'продуктовый аналитик'
      ],
      "Аналитик DWH": [
        "data engineer", "dwh", "data warehouse", "airflow", "data lake",
        "databricks", "spark", "hadoop", 'sql'
      ],
      "Веб-аналитик": [
        "веб", "web",
      ],
      "Аналитик (Другое)": []
  }
},
 "Тестирование": {
    "keywords": [
      "тестировщик", "tester", "qa", "quality assurance", "тестировщик-автоматизатор",
      "qa engineer", "инженер по тестирован", "ручн тестирован", "автоматизирован тестирован",
      "мобильн тестирован", "веб тестирован", "гейм тестирован", "api тестирован",
      "безопасност тестирован", "производительност тестирован", "нагрузочн тестирован",
      "интеграцион тестирован", "регрессион тестирован", "smoke тестирован", "приемочн тестирован",
      "quality manager", "qa lead", "qa architect", 'manual_testing', 'test_automation', 'qa_engineer'
    ],
    "subcategories": {
      "Ручное тестирование": [
        "ручн тестировщик", 'ручное', 'ручного', 'manual_testing'
      ],
      "Автоматизированное тестирование": [
        "автоматизатор тестирован", "automation tester", "qa automation", "test_automation"
      ],
     "Тестирование (Другое)": []
    }
},
 "Разработка": {
    "keywords": [
      "frontend", "front-end", "front end", "javascript", "js",
      "react", "angular", "vue", "typescript", 'software',
      "backend", 'devops', 'mobileapp_developer', "data_engineer", 'database_developer', 
      "fullstack", "full-stack", "full stack", "DevOps-инженер"
    ],
    "subcategories": {
      "Frontend разработка": [
        "frontend", "front-end", "front end", "javascript", "js",
        "react", "angular", "vue", "typescript", "ui developer"
      ],
      "Backend разработка": [
        "backend", "back-end", "back end", "server", "api",
        "python", "java", "php", "node", "nodejs", "net", "ruby", "go", "golang"
      ],
      "Fullstack разработка": [
        "fullstack", "full-stack", "full stack", 
      ],
      "Мобильная разработка": [
        "mobile", "android", "ios", "flutter", "react",
        "котлин", "kotlin", "swift", "mobileapp_developer"
      ],
      "DevOps": [
        "devops", "DevOps-инженер"
      ], 
      "Data engineer": [
        "data_engineer", 'database_developer'
      ],
  "Разработка (Другое)": []
    }
},
 "ML/AI/DS": {
    "keywords": [ 
      "ml engineer", "ml-engineer", "mlops", 'data_scientist', 'ml', 'ai', 'промт', 'дата-сайентист'
    ],
    "subcategories": {
      "Data Science": [
        "data science", "анализ данн", "дата-сайентист", "data_scientist", 'дата-сайентист'
      ],
      "ML Engineering & Mlops": [
        "ml engineer", "ml-engineer", "mlops", "model serving"
      ],
       "AI (Другое)": []
    }
},
 "Менеджмент": {
    "keywords": [
      'менеджер продукта', 'руководитель группы разработки', 'руководитель отдела аналитики', "руководитель проектов", 'project_manager',
      'project_director', 'product_manager', 'marketing_manager', 'account_manager'
    ],

    "subcategories": {
      "Продуктовый менеджмент": [
        "продуктов менеджер", "product manager", "PM", "product owner",
        "руководитель продукт", "head of product", 'product_manager'
      ],
      "Проектный менеджмент": [
        "проектн менеджер", "project manager", "PM", "руководитель проектов", 'project_manager', 'scrum_master', 'account_manager'
      ],
      "ИТ топ менеджмент": [
        'руководитель группы разработки',  'руководитель отдела аналитики', 'технический директор (сто)',  'project_director'
      ],

"Менеджер (Другое)": []
 }
    }
}



from aiogram import F
from aiogram.types import Message, FSInputFile
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

users = {}

selected_subcategories = {}

selected_cities = {}

user_expierence = {}

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.filters import Command
from aiogram import html as h
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Главное меню
main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поиск вакансий")],
    [KeyboardButton(text="AI ассистент")],
    [KeyboardButton(text="Опубликовать вакансию"), KeyboardButton(text="Помощь")]
], resize_keyboard=True)

# Меню категорий вакансий
categories_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Аналитика"), KeyboardButton(text="Разработка")],
    [KeyboardButton(text="Тестирование"), KeyboardButton(text="ML/AI/DS")],
    [KeyboardButton(text="Менеджмент")],
    [KeyboardButton(text="В главное меню"), KeyboardButton(text="Готово")]
], resize_keyboard=True)

expierence_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Нет опыта"), KeyboardButton(text="От 1 года до 3 лет")],
    [KeyboardButton(text="От 3 до 6 лет"), KeyboardButton(text="Более 6 лет")],
    [KeyboardButton(text="Назад в категории"),KeyboardButton(text="Готово")]
    
], resize_keyboard=True)





# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    # user_id = message.from_user.id
    user_id = str(message.from_user.id)
    await state.set_state(Form.user_id)
    await state.update_data(user_id=user_id) 
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку start")
    await check_and_add_user(user_id, message.from_user.first_name)


    
    

    welcome_text = (
    "👋 <b>Привет, {name}!</b>\n\n"
    "Я твой персональный HR-ассистент, который поможет найти работу мечты!\n\n"
    "📌 <b>Что я умею:</b>\n\n"
    "🔍 Искать вакансии по твоим критериям\n"
    "📝 Анализировать твоё резюме и давать рекомендации\n\n"
    "Для работы со мной просто используй кнопки меню ниже 👇\n\n"
    "<i>Если что-то пойдёт не так, ты всегда можешь перезапустить меня командой /start</i>\n\n"
    "Ваш feedback помогает нам становиться лучше! Ошибки и предложения принимаются через кнопку <b>Помощь</b>."
        ).format(name=message.from_user.first_name)


    await message.answer(welcome_text,  parse_mode="HTML", reply_markup=main_keyboard)
    logger.info(f"Пользователю {message.from_user.id} {message.from_user.username} отправлен welcome_text")


# Обработчик кнопки "Поиск вакансий"
@router.message(lambda message: message.text == "Поиск вакансий")
async def search_vacancies(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал поиск вакансий")
    await state.set_state(Form.category)
    await message.answer(
        "🔍 Давай подберем для тебя лучшие вакансии!\n"
        "Выбери категорию из списка:",
        reply_markup=categories_keyboard
        )


@router.message(Form.category, lambda message: message.text in category_keywords.keys())
async def handle_category(message: Message, state: FSMContext):
    category = message.text
    user_id = str(message.from_user.id)
    
    await state.update_data(current_category=category)
    
    # Инициализируем пустой набор подкатегорий для пользователя, если еще нет
    if user_id not in selected_subcategories:
        selected_subcategories[user_id] = set()
    

    await message.answer(
        f"📌 Ты выбрал категорию: <b>{category}</b>\n\n"
        "Теперь укажи подкатегории (можно выбрать несколько):",
        reply_markup=get_subcategories_keyboard(category, user_id),
        parse_mode="HTML"
    )


# Функция для создания клавиатуры подкатегорий
def get_subcategories_keyboard(category: str, user_id: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    subcategories = category_keywords[category]["subcategories"].keys()
    
    # Добавляем кнопки подкатегорий (по 2 в ряд)
    for subcategory in subcategories:
        # Проверяем, выбрана ли подкатегория для этого пользователя
        is_selected = user_id in selected_subcategories and subcategory in selected_subcategories[user_id]
        text_button = f"✅ {subcategory}" if is_selected else subcategory
        builder.add(KeyboardButton(text=text_button))
    
    builder.adjust(2)
    
    # Добавляем кнопки управления
    builder.row(
        KeyboardButton(text="Назад в категории"),
        KeyboardButton(text="Готово")
    )
    
    return builder.as_markup(resize_keyboard=True)

# Обработчик выбора подкатегорий
@router.message(
    Form.category,
    lambda message: any(
        message.text.replace("✅ ", "") in subcats 
        for cat in category_keywords.values() 
        for subcats in cat["subcategories"].keys()
    )
)
async def handle_subcategory(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    subcategory = message.text.replace("✅ ", "") 
    
    # Инициализируем множество подкатегорий для пользователя, если еще нет
    if user_id not in selected_subcategories:
        selected_subcategories[user_id] = set()
    
    # Добавляем или удаляем подкатегорию
    if subcategory in selected_subcategories[user_id]:
        selected_subcategories[user_id].remove(subcategory)
        action = "❌ Убрано из выбора"
    else:
        selected_subcategories[user_id].add(subcategory)
        action = "✅ Добавлено к выбору"
    
    # Получаем текущую категорию для обновления клавиатуры
    data = await state.get_data()
    current_category = data.get('current_category')
    
    selected = "\n".join(selected_subcategories.get(user_id, ["Пока ничего не выбрано"]))

    
    await message.answer(
        f"{action}: <b>{subcategory}</b>\n\n"
        f"<b>Твой текущий выбор:</b>\n\n{selected}\n\n"
        "Можешь продолжить выбирать или нажать <b>«Готово»</b>",
        reply_markup=get_subcategories_keyboard(current_category, user_id),
        parse_mode="HTML"
    )


@router.message(Form.category, lambda message: message.text == "Готово")
async def handle_subcategories_done(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку готово")
    
    if user_id not in selected_subcategories or not selected_subcategories[user_id]:
        await message.answer("⚠️ Ты не выбрал ни одной специализации.\n\n"
            "Пожалуйста, выбери хотя бы один вариант.")
        return
    
    selected = "\n".join(selected_subcategories[user_id])
   
    await message.answer(
        "📋 <b>Отлично! Твой выбор:</b>\n\n"
        f"{selected}\n\n"
        "Теперь укажи свой опыт работы:",
        reply_markup=expierence_keyboard,
        parse_mode="HTML"
    )

    await state.set_state(Form.waiting_for_experience)
    
    data = await state.get_data()
    if 'selected_cities' in data:
        selected_cities[user_id] = data['selected_cities']



@router.message(Form.waiting_for_experience)
async def handle_experience_selection(message: Message, state: FSMContext):
    global user_expierence
    user_id = str(message.from_user.id)
    
    # Инициализируем множество для пользователя, если его нет или если это строка
    if user_id not in user_expierence or isinstance(user_expierence[user_id], str):
        user_expierence[user_id] = set()
    
    if message.text == "Назад в категории":
        await state.set_state(Form.category)
        await message.answer("Возвращаемся к выбору категорий", reply_markup=categories_keyboard)
        return
    
    if message.text == "Готово":
        if not user_expierence.get(user_id):
            await message.answer("⚠️ Ты не выбрал ни одного варианта опыта.\n\n"
                               "Пожалуйста, выбери хотя бы один вариант или нажми «Назад в категории».")
            return
            
        selected = "\n".join(user_expierence[user_id])
        await message.answer(
            "📋 <b>Отлично! Твой выбор опыта:</b>\n\n"
            f"{selected}\n\n"
            "Теперь укажи города для поиска:",
            reply_markup=get_cities_keyboard(all_cities, user_id),
            parse_mode="HTML"
        )
        await state.set_state(Form.waiting_for_cities)
        return
    
    # Добавляем или удаляем опыт
    exp = message.text
    if exp in user_expierence[user_id]:
        user_expierence[user_id].remove(exp)
        action = "❌ Убрано из выбора"
    else:
        user_expierence[user_id].add(exp)
        action = "✅ Добавлено к выбору"
    
    # Формируем текст с выбранными вариантами
    selected = "\n".join(user_expierence.get(user_id, ["Пока ничего не выбрано"]))
    
    await message.answer(
        f"{action}: <b>{exp}</b>\n\n"
        f"<b>Твой текущий выбор:</b>\n\n{selected}\n\n"
        "Можешь продолжить выбирать или нажать <b>«Готово»</b>",
        reply_markup=expierence_keyboard,
        parse_mode="HTML"
    )

# Общий обработчик для кнопки "Назад в категории"
async def back_to_categories_common(message: Message, state: FSMContext):
    # Всегда переходим к выбору категорий
    await state.set_state(Form.category)
    await message.answer("Выберите категорию:", reply_markup=categories_keyboard)

# Обработчики для разных состояний
@router.message(Form.waiting_for_experience, lambda message: message.text == "Назад в категории")
async def back_to_categories_from_experience(message: Message, state: FSMContext):
    await back_to_categories_common(message, state)

# @router.message(Form.waiting_for_cities, lambda message: message.text == "Назад в категории")
# async def back_to_categories_from_cities(message: Message, state: FSMContext):
#     await back_to_categories_common(message, state)

@router.message(Form.waiting_for_cities, lambda message: message.text == "Назад в категории")
async def back_to_categories_from_cities(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    # Сохраняем выбранные города перед возвратом
    await state.update_data(selected_cities=selected_cities.get(user_id, set()))
    await back_to_categories_common(message, state)

@router.message(Form.category, lambda message: message.text == "Назад в категории")
async def back_to_categories_from_category(message: Message, state: FSMContext):
    await back_to_categories_common(message, state)
    
def get_cities_keyboard(all_cities,user_id: int = None) -> ReplyKeyboardMarkup:
    # builder = ReplyKeyboardBuilder()
    # builder.row(KeyboardButton(text="Назад в категории"))
    # builder.row(KeyboardButton(text="Начать поиск вакансий"))
    # builder.adjust(1)
    
    builder = ReplyKeyboardBuilder()
    
    # Кнопки управления
    builder.row(KeyboardButton(text="Назад в категории"))
    builder.row(KeyboardButton(text="Начать поиск вакансий"))
    
    # Добавляем кнопку "Удаленка" отдельной строкой
    remote_text = "✅ Удаленная работа" if (user_id and str(user_id) in selected_cities and "Удаленная работа" in selected_cities[str(user_id)]) else "Удаленная работа"

    builder.row(KeyboardButton(text=remote_text))
    
    # Полный список городов России (пример)
    all_cities_now = all_cities
    
    # Приоритетные города (должны быть в начале)
    priority_cities = ["Москва", "Санкт-Петербург", "Казань", "Новосибирск", "Екатеринбург", 'Красноярск', 
                       "Нижний Новгород", 'Челябинск', 'Уфа',
                       "Самара", "Ростов-на-Дону", 'Краснодар', "Омск", 'Воронеж', 'Пермь', 'Волгоград']
    

    sorted_cities = priority_cities # + sorted(

    for city in sorted_cities:
        if user_id and str(user_id) in selected_cities and city in selected_cities[str(user_id)]:
            text_button = f"✅ {city}"
        else:
            text_button = city
        builder.add(KeyboardButton(text=text_button))
    
    builder.adjust(2)
    
    # Добавляем кнопки управления

    return builder.as_markup(resize_keyboard=True)



@router.message(Form.waiting_for_cities, F.text, lambda message: message.text.replace("✅ ", "") in all_cities or message.text.replace("✅ ", "") == "Удаленная работа")
async def handle_city_selection(message: Message):
    user_id = str(message.from_user.id)
    city = message.text.replace("✅ ", "")  # Удаляем эмодзи если есть

   
    
    # Инициализируем множество для пользователя, если его нет
    if user_id not in selected_cities:
        selected_cities[user_id] = set()
    
    # Добавляем или удаляем город
    if city in selected_cities[user_id]:
        selected_cities[user_id].remove(city)
        action = "❌ Убрано из выбора"
    else:
        selected_cities[user_id].add(city)
        action = "✅ Добавлено к выбору"
    
    # Формируем список выбранных городов
    selected = "\n".join(selected_cities.get(user_id, ["Пока ничего не выбрано"]))

    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} выбрал {selected}")
    # Обновляем клавиатуру
    await message.answer(
        f"{action}: {city}\n\n"
        f"Текущий выбор:\n{selected}\n\n"
        "Продолжайте выбирать или нажмите «Начать поиск»",
        reply_markup=get_cities_keyboard(all_cities, user_id)
    )


@router.message(F.text == "Начать поиск вакансий")
async def handle_vacancy_search(message: Message, state: FSMContext, bot: Bot):
    user_id = str(message.from_user.id)
    
    # Проверяем, что пользователь выбрал города
    if not selected_cities.get(user_id):
        await message.answer(
            "⚠️ <b>Ой!</b>\n"
            "Ты не выбрал ни одного города для поиска.\n"
            "Пожалуйста, укажи хотя бы один город или выбери удаленную работу.\n",
            parse_mode="HTML", 
            reply_markup=get_cities_keyboard(all_cities, user_id)
        )
        return
    
    try:

        category = selected_subcategories[user_id]

        category_text =  "\n".join(f"• {category}" for category in selected_subcategories[user_id])
        
        # Формируем текст с выбранными городами
        cities_text = "\n".join(f"• {city}" for city in selected_cities[user_id])


        await message.answer(
            "🔍 <b>Начинаю поиск вакансий...</b>\n\n"
            f"<b>Категория:</b>\n{category_text}\n\n"
            # f"<b>Опыт работы:</b>\n{user_exp}\n\n"
            f"<b>Города:</b>\n{cities_text}\n\n"
            "Как только найду подходящие вакансии - сразу пришлю их тебе!\n\n"
            "⏳ <i>Внимание:</i> я не умею рассылать чаще, чем раз в 10 минут",
            parse_mode="HTML", 
            reply_markup=main_keyboard
        )
        
        await send_personalized_vacancies(bot)  
        logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} окончил настройку поиска вакансий")

    except:
         await message.answer(
            "😕 <b>Упс, что-то пошло не так</b>\n"
            "Попробуй начать поиск заново через меню."
            "Ошибка блин блинский\n",
            "Если меню не работает, отправь /start",
            parse_mode="HTML", reply_markup=main_keyboard
        )
         logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} столкнулся с ошибкой")
        
    
# Обработчик кнопки "В главное меню"
@router.message(lambda message: message.text == "В главное меню")
async def back_to_main(message: Message):
    user_id = message.from_user.id
    await message.answer("Возвращаемся в главное меню", reply_markup=main_keyboard)

@router.message(lambda message: message.text == "AI ассистент")
async def update_resume(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку AI ассистент")
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🔥 Прожарка резюме на основе вакансий")],
            [KeyboardButton(text="🎯 Общая оценка резюме")],
            [KeyboardButton(text="В главное меню")]
        ]
    )

    await message.answer(
    text=(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — твой AI помощник по карьере.\n\n"
        "✨ Я стараюсь быть максимально точным и опираюсь на реальные вакансии, "
        "но иногда могу ошибаться — если что-то покажется странным, "
        "сообщи пожалуйста по кнопке 'Помощь'!\n\n"
        "С чего начнём?"
    ),
    reply_markup=markup,
    parse_mode="HTML"
)



def escape_html(text):
    return markdown(text, extensions=['fenced_code'])


def clean_and_format(text: str) -> str:

    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  

    return text




@router.message(lambda message: message.text == "🎯 Общая оценка резюме")
async def general_resume_review(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Общая оценка резюме")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    await message.answer(
        text="📌 Отлично! Пришлите резюме в формате PDF для комплексной оценки",
        reply_markup=keyboard
    )
    await state.set_state(ResumeAnalysisStates.waiting_for_resume_total)
    logger.info(f"Пользователь {message.from_user.id} начал общую оценку резюме")

@router.message(F.document, ResumeAnalysisStates.waiting_for_resume_total)
async def handle_general_resume(message: Message, state: FSMContext):
    try:
        if not message.document.file_name.lower().endswith('.pdf'):
            await message.answer("❌ Файл должен быть в формате PDF!")
            return

        logger.info(f"Получен документ: {message.document.file_name}")
        await message.answer("🔍 Анализирую резюме... Обычно это занимает 3-5 минут")

        # Скачиваем и обрабатываем файл
        file = await message.bot.download(message.document.file_id)
        pdf_bytes = file.read()
        
        # Извлекаем текст и сохраняем в state
        extracted_text = extract_text_from_pdf(pdf_bytes)
        if not extracted_text:
            await message.answer("❌ Не удалось извлечь текст. Убедитесь, что файл не сканированный.")
            await state.clear()
            return
            
        await state.update_data(resume_text=extracted_text)
        await state.set_state(ResumeAnalysisStates.resume_text_stored)

        # Вызываем hot_resume для общей оценки
        analysis_result = await generating_answer_without_vacancy(extracted_text)  
        formatted_result = clean_and_format(analysis_result)

        logger.info(f"Пользователь {message.from_user.id} получил анализ {formatted_result}")
        
        await message.answer(formatted_result, parse_mode="HTML")
        await message.answer(
            "✅ Анализ завершен. Буду рад если вы поделитесь фидбеком о моей работе через кнопку 'Помощь'",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="В главное меню")]
                ],
                resize_keyboard=True
            )
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке резюме: {e}", exc_info=True)
        await message.answer("⚠️ Произошла ошибка анализа. Попробуйте другой файл.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="В главное меню")]
                ],
                resize_keyboard=True
            )
        )
        await state.clear()

@router.message(F.text, lambda message: message.text == "🔥 Прожарка резюме на основе вакансий")
async def start_resume_roast_from_existing(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Прожарка резюме на основе вакансий")
    await state.set_state(ResumeAnalysisStates.waiting_for_category)
    await message.answer(
        "🔍 Выберите категорию вакансий для анализа резюме:",
        reply_markup=get_roast_categories_keyboard()
    )

def get_roast_categories_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔥 Аналитика"), KeyboardButton(text="🔥 Разработка")],
            [KeyboardButton(text="🔥 Тестирование"), KeyboardButton(text="🔥 ML/AI/DS")],
            [KeyboardButton(text="🔥 Менеджмент")],
            [KeyboardButton(text="В главное меню")]
        ],
        resize_keyboard=True

    )

@router.message(F.text, lambda message: message.text[2:] in category_keywords.keys())
async def handle_roast_category(message: Message, state: FSMContext):
    """🔥 Обработчик выбора категории для прожарки"""
    category = message.text[2:]
    await state.update_data(roast_category=category)
    await state.set_state(ResumeAnalysisStates.waiting_for_subcategory)
    
    await message.answer(
        f"🔥 Выберите <b>ОДНУ</b> специализацию в категории <b>{category}</b>:\n"
        "Нажмите на нужную подкатегорию ниже 👇",
        reply_markup=get_roast_subcategories_keyboard(category),
        parse_mode="HTML"
    )

def get_roast_subcategories_keyboard(category: str) -> ReplyKeyboardMarkup:
    """🔥 Клавиатура подкатегорий для прожарки"""
    builder = ReplyKeyboardBuilder()
    
    # Добавляем подкатегории с emoji
    for subcategory in category_keywords[category]["subcategories"].keys():
        builder.add(KeyboardButton(text=f"🔥 {subcategory}"))  
    
    builder.adjust(2)
    
    # Управляющие кнопки тоже с emoji
    builder.row(
        KeyboardButton(text="В главное меню")
    )
    
    return builder.as_markup(resize_keyboard=True)


hair_user = {}
@router.message(F.text, 
    ResumeAnalysisStates.waiting_for_subcategory,
    lambda message: any(
        message.text[2:] in subcats
        for cat in category_keywords.values()
        for subcats in cat["subcategories"].keys()
    )
)
async def handle_roast_subcategory_selection(message: Message, state: FSMContext):
    """🔥 Обработчик выбора подкатегории"""
    hair_user[message.from_user.id] = message.text[2:] 
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    await message.answer(
        text="📌 Отлично! Пришлите резюме в формате PDF для комплексной оценки",
        reply_markup=keyboard
    )
    await state.set_state(ResumeAnalysisStates.waiting_for_resume_fair)
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} начал прожарку резюме")

@router.message(F.document, ResumeAnalysisStates.waiting_for_resume_fair)
async def handle_general_resume(message: Message, state: FSMContext, bot):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    try:
        if not message.document.file_name.lower().endswith('.pdf'):
            await message.answer("❌ Файл должен быть в формате PDF!",
                reply_markup=keyboard)
            return

        logger.info(f"Получен документ: {message.document.file_name}")
        await message.answer("🔍 Анализирую резюме... Мне нужно 3-5 минут")

        # Скачиваем и обрабатываем файл
        file = await message.bot.download(message.document.file_id)
        pdf_bytes = file.read()
        
        # Извлекаем текст и сохраняем в state
        extracted_text = extract_text_from_pdf(pdf_bytes)

        analysis_result = await hot_resume(extracted_text, hair_user[message.from_user.id])
        # analysis_result = asyncio.create_task(hot_resume(extracted_text, hair_user[message.from_user.id]))
        formatted_result = clean_and_format(analysis_result)
        
        await message.answer(
            formatted_result,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.info(f"Ошибка у пользователя: {message.from_user.id} {message.from_user.username} при анализе резюме {e}")
        await message.answer(
            'Ошибка, пожалуйста, попробуйте еще раз, мы обязательно ознакомимся с ошибкой и постараемся ее устранить',
            parse_mode="HTML",
            reply_markup=keyboard)
   
    


@router.message(F.text == "Опубликовать вакансию")
async def handle_vacancy_search(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал на кнопку Опубликовать вакансию")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    
    await message.answer(
    "🌿 <b>Добрый день!</b>\n\n"
    "Мы рады, что вы решили разместить вакансию в нашем сервисе!\n\n"
    "📝 <b>Пожалуйста, напишите в чат с ботом следующую информацию:</b>\n\n"
    "• Наименование вакансии\n"
    "• Описание вакансии\n"
    "• Компания\n"
    "• Требуемые навыки\n"
    "• Опыт работы\n"
    "• Уровень зарплаты (по желанию)\n"
    "• Локация/удаленная работа\n"
    "• Ссылка на вакансию (если есть)\n\n"
    "💼 Наш менеджер рассмотрит вашу заявку и свяжется с вами в ближайшее время "
    "для уточнения деталей и публикации вакансии.\n\n"
    "<i>Благодарим за сотрудничество!</i>",
    parse_mode="HTML",
    reply_markup=keyboard
)


    await state.set_state(Form.waiting_for_description)

@router.message(Form.waiting_for_description)
async def process_vacancy_description(message: Message, state: FSMContext):
    if message.text == "В главное меню":
        await state.clear()
        await message.answer("Создание вакансии отменено", reply_markup=main_keyboard)
        return
    
    # Сохраняем данные (можно добавить в FSM storage)
    await state.update_data(vacancy_description=message.text)

    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} отправил текст вакансии")
    
    # Подтверждение получения
    await message.reply(
        "✅ <b>Вакансия получена!</b>\n\n"
        "Менеджер проверит информацию и свяжется с вами в течение 24 часов.\n"
        "Спасибо за доверие!",
        parse_mode="HTML",
        reply_markup=main_keyboard  # Убираем спец. клавиатуру
    )
    
    # Здесь можно добавить отправку уведомления менеджеру
    await forward_to_manager(message)
    
    await state.clear()

    
@router.message(Command("forward_vacancy"))  # Можно привязать к команде или другому фильтру
async def forward_to_manager(message: Message):
    MANAGER_CHAT_ID = -4959512272  # Замените на реальный ID чата/группы
    
    try:
        # 1. Пересылаем сообщение менеджеру
        forwarded_msg = await message.forward(
            chat_id=MANAGER_CHAT_ID
        )
        
        # 2. Отправляем поясняющее сообщение (привязанное к пересланному)
        await message.bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text=f"🚀 Новая вакансия от @{message.from_user.username}",
            reply_to_message_id=forwarded_msg.message_id  # Ответ именно на пересланное сообщение
        )
        
        # 3. Подтверждаем пользователю
        await message.reply("✅ Вакансия отправлена менеджеру!")
        logger.info(f"Вакансия отправлена в наш чат")
        
    except Exception as e:
        logger.info(f"Ошибка пересылки: {e}")
        await message.answer("⚠️ Не удалось отправить вакансию. Попробуйте позже.")
 

@router.message(F.text == "Помощь")
async def handle_trable(message: Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} {message.from_user.username} нажал кнопку Помощь")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В главное меню")]],
        resize_keyboard=True
    )
    
    await message.answer(
    "🛎 <b>Служба поддержки</b>\n\n"
        "Расскажите, с какой проблемой вы столкнулись?\n"
        "Опишите её как можно подробнее, и мы обязательно поможем!\n\n",
    parse_mode="HTML",
    reply_markup=keyboard
    )


    await state.set_state(Form.waiting_for_trable)

@router.message(Form.waiting_for_trable)
async def process_vacancy_description(message: Message, state: FSMContext):
    if message.text == "В главное меню":
        await state.clear()
        await message.answer("✅ Запрос в поддержку отменен)", reply_markup=main_keyboard)
        return
    
    # Сохраняем данные (можно добавить в FSM storage)
    await state.update_data(trable=message.text)
    
    # Подтверждение получения
    await message.reply(
        "💌 <b>Спасибо за обращение!</b>\n\n"
        "Ваше сообщение получено и передано в поддержку.\n"
        "Мы ответим вам в ближайшее время.\n",
        parse_mode="HTML",
        reply_markup=main_keyboard  # Убираем спец. клавиатуру
    )

    await forward_to_manager_trable(message)
    
    await state.clear()

@router.message(Command("forward_to_manager_trable"))  # Можно привязать к команде или другому фильтру
async def forward_to_manager_trable(message: Message):
    MANAGER_CHAT_ID = -4959512272  # Замените на реальный ID чата/группы
    
    try:
        # 1. Пересылаем сообщение менеджеру
        forwarded_msg = await message.forward(
            chat_id=MANAGER_CHAT_ID
        )
        
            
           
        # 2. Отправляем поясняющее сообщение (привязанное к пересланному)
        await message.bot.send_message(
            chat_id=MANAGER_CHAT_ID,
            text= (f"🆘 <b>Новый запрос в поддержку</b>\n\n"
                 f"🚀 Проблема у @{message.from_user.username}"
                 f"🆔 <b>ID:</b> {message.from_user.id}\n"
                f"📅 <b>Время:</b> {message.date.strftime('%d.%m %H:%M')}\n\n"
             # Ответ именно на пересланное сообщение
            ),
            parse_mode="HTML",
            reply_to_message_id=forwarded_msg.message_id 
        )
        logger.info(f"Проблема отправлена в наш чат")
        # 3. Подтверждаем пользователю
        await message.reply("✅ Ваша проблема отправлена менеджеру!")
        
    except Exception as e:
        logger.info(f"Ошибка пересылки: {e}")
        await message.answer("Упс... что-то пошло не так.")
 




# Бд ниже

async def hourly_db_update(bot: Bot):
    """Ежечасное обновление БД"""
    global vacanciessss
    global hr_vacanciess
    while True:
        logger.info(f"[{datetime.now()}] Запуск обновления БД...")

        vacanciessss, hr_vacanciess = await load_and_cache_vacancies()
        logger.info(f"[{datetime.now()}] Вакансии загружены")
        await send_personalized_vacancies(bot)  
        logger.info(f"[{datetime.now()}] Рассылка отправлена")
        await asyncio.sleep(3600)  # 1 час
    

async def hourly_db_save(bot: Bot):
    """Ежечасное сохранение в БД"""
    global vacanciessss
    global hr_vacanciess
    while True:
        logger.info(f"[{datetime.now()}] Запуск сохранения БД...")
        await save_selected_subcategories()
        logger.info(f"[{datetime.now()}] Сохранение в БД завершено")
        await asyncio.sleep(3600)  # 1 час
        

async def start_background_tasks(bot: Bot):
    """Запуск фоновых задач при старте"""
    global selected_subcategories
    global selected_cities
    global all_cities
    global user_expierence

    loaded_data, all_cities, selected_cities, user_expierence = await load_selected_subcategories()
    # vacanciessss = await load_and_cache_vacancxies()
    selected_subcategories.update(loaded_data)
    logger.info(f"[{datetime.now()}] Загружено {len(loaded_data)} пользовательских выборов из БД")
    asyncio.create_task(hourly_db_update(bot))
    asyncio.create_task(hourly_db_save(bot))
    asyncio.create_task(cleanup_memory(bot))


async def cleanup_memory(bot: Bot):
    """Раз в 2 дня чистим кеш"""
    global last_send_time, send_vacancies
    while True:
        await asyncio.sleep(172800) 
        logger.info(f"[{datetime.now()}] Запуск очистки last_send_time, send_vacancies")
        try:
            now = datetime.now()
            last_send_time = {k: v for k, v in last_send_time.items() if now - v < timedelta(days=3)}
            send_vacancies = {k: v for k, v in send_vacancies.items() if now - v[-1]['date'] < timedelta(days=3)}
        except Exception as e:
            logger.info(f"[{datetime.now()}] Cleanup error: {e}")
   


async def save_selected_subcategories():
    if not selected_subcategories:
        return
    
    conn = None
    try:
        conn = await asyncpg.connect(
            host= host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # Создаем копии словарей для безопасной итерации
        users_to_update = selected_subcategories.copy()
        cities_to_update = selected_cities.copy()
        exp_to_update = user_expierence.copy()

        async with conn.transaction():
            # Обновляем подкатегории
            for user_id, subcategories in users_to_update.items():
                await conn.execute(
                    "UPDATE users SET new_category = $1 WHERE user_id = $2",
                    json.dumps(list(subcategories), ensure_ascii=False),
                    str(user_id)
                )

            # Обновляем города
            for user_id, cities in cities_to_update.items():
                await conn.execute(
                    "UPDATE users SET cities = $1 WHERE user_id = $2",
                    json.dumps(list(cities), ensure_ascii=False),
                    str(user_id)
                )

            # Обновляем опыт
            for user_id, exp in exp_to_update.items():
                await conn.execute(
                    "UPDATE users SET experience = $1 WHERE user_id = $2",
                    json.dumps(list(exp), ensure_ascii=False),
                    str(user_id)
                )
        
        logger.info(f"[{datetime.now()}] Успешно сохранены данные для {len(users_to_update)} пользователей")

    
    except ValueError as e:  # Заменили json.JSONEncodeError
        logger.info(f"[{datetime.now()}] Ошибка кодирования JSON: {e}")
    except asyncpg.PostgresError as e:
        logger.info(f"[{datetime.now()}] Ошибка базы данных:  {e}")
    except Exception as e:
        logger.info(f"[{datetime.now()}] Неожиданная ошибка:  {e}")
    finally:
        if conn:
            await conn.close()



# При перезапуске
async def load_selected_subcategories() -> dict:
    """
    Загружает сохраненные подкатегории из базы данных
    Возвращает словарь в формате {user_id: set(subcategories)}
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
        
        # Загружаем данные из базы
        records = await conn.fetch(
            "SELECT user_id, new_category FROM users WHERE new_category IS NOT NULL"
        )
        city_list = await conn.fetch(
            "SELECT distinct location FROM vacans"
        )


        city_list = [record['location'] for record in city_list]
        city_list = [city for city in city_list if city is not None]

        city_for_users = await conn.fetch(
            "SELECT user_id, cities FROM users WHERE cities IS NOT NULL"
        )

        expierence_for_users = await conn.fetch(
            "SELECT user_id, experience FROM users WHERE experience IS NOT NULL"
        )


        # Формируем словарь selected_subcategories
        loaded_data = {}
        for record in records:
            try:
                if record['new_category']:
                    # Декодируем JSON и преобразуем список в set
                    loaded_data[record['user_id']] = set(json.loads(record['new_category']))
            except json.JSONDecodeError as e:
                logger.info(f"[{datetime.now()}] Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
        logger.info(f"[{datetime.now()}] Успешно загружено пользователей {len(loaded_data)} записей из БД")

        loaded_data_city = {}
        for record in city_for_users:
            try:
                if record['cities']:
                    # Декодируем JSON и преобразуем список в set
                    loaded_data_city[record['user_id']] = set(json.loads(record['cities']))
            except json.JSONDecodeError as e:
                logger.info(f"[{datetime.now()}] Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
        logger.info(f"[{datetime.now()}] Успешно загружено городов {len(loaded_data_city)} записей из БД")
        user_expierence = {}
        for record in expierence_for_users:
            try:
                if record['experience']:
                    # Декодируем JSON и преобразуем список в set
                    user_expierence[record['user_id']] = set(json.loads(record['experience']))
                    # user_expierence[record['user_id']] = set((record['experience']))
                    # user_expierence[record['user_id']] = record['experience']
            except:
                logger.info(f"[{datetime.now()}] Ошибка декодирования для user_id {record['user_id']}: {e}")
                continue
        logger.info(f"[{datetime.now()}] Успешно загружено опыта {len(user_expierence)} записей из БД")    
        
        return loaded_data, city_list, loaded_data_city, user_expierence
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Ошибка при загрузке из БД: {e}") 
        return {}
    finally:
        if conn:
            await conn.close()



# Загрузка актуальных вакансий

async def load_and_cache_vacancies():
    """
    Загружает обычные и HR-вакансии из БД,
    возвращает кортеж (vacancies_cache, hr_vacancies_cache)
    """
    conn = None
    logger.info(f"[{datetime.now()}] Начали кешировать вакансии") 
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        # 1. Загрузка обычных вакансий
        records = await conn.fetch(
            "SELECT id, title, company, skills, location, experience, new_category, date, link "
            "FROM vacans WHERE date >= CURRENT_DATE - INTERVAL '3 day' AND (is_hr != TRUE or is_hr is Null)" 
        )
        
        # Кэшируем обычные вакансии
        vacancies = {
            str(record['id']): {
                'title': record['title'],
                'company': record['company'],
                'skills': record['skills'],
                'location': record['location'],
                'experience': record['experience'],
                'categories': record['new_category'].split("|")[1],
                'date': record['date'],
                'link': record['link'],
                'is_hr': False
            }
            for record in records
        }
        
        # 2. Загрузка HR-вакансий
        hr_records = await conn.fetch(
            "SELECT id, title, company, skills, location, description, date, link, contact, experience, new_category "
            "FROM vacans WHERE date >= CURRENT_DATE - INTERVAL '3 day' AND is_hr = TRUE"
        )
        
        # Кэшируем HR-вакансии
        hr_vacancies = {
            str(record['id']): {
                'title': record['title'],
                'company': record['company'],
                'skills': record['skills'],
                'location': record['location'],
                'experience': record['experience'],
                'categories': record['new_category'].split("|")[1],
                'description': record['description'],
                'date': record['date'],
                'link': record['link'],
                'is_hr': True,
                'contact': record['contact']
            }
            for record in hr_records
        }
        logger.info(f"[{datetime.now()}] Вакансии успешно закешированы (обычные: {len(vacancies)}, HR: {len(hr_vacancies)})") 
        return vacancies, hr_vacancies
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Ошибка загрузки данных: {e}") 
        return {}, {}
    finally:
        if conn:
            await conn.close()



from datetime import datetime, timedelta



# Глобальный словарь для хранения времени последней рассылки
last_send_time = {}
send_vacancies = {}
vacancy_counter = {}


async def send_vacancies_to_user(bot: Bot, user_id: int, vacancies: list):
    """Отправляет вакансии пользователю с возможной задержкой"""
    for i, vac in enumerate(vacancies, 1):
        # message = [
        #     "🔔 <b>Новые вакансии:</b>\n",
        #     f"✨ <b>{vac['title']}</b>\n",
        #     f"🏛 <i>{vac['company']}</i>\n\n",
        #     f"🌍 <b>Локация:</b> {vac['location']}\n",
        #     f"📆 <b>Опыт:</b> {vac['experience']}\n",
        #     f"💼 <b>Навыки:</b> {vac['skills'][:200]} ...\n\n",
        #     f"🔗 <a href='{vac['link']}'>Подробнее о вакансии</a>\n"
            
        # ]
        message = (
            f"🏢 <b>Должность:</b> {vac['title']}\n"
            f"🏛 <b>Компания:</b> <i>{vac['company']}</i>\n\n"
            
            "📍 <b>Локация:</b> {location}\n"
            "📅 <b>Требуемый опыт:</b> {experience}\n\n"
            
            "🛠 <b>Ключевые навыки:</b>\n"
            "{skills}\n\n"
            
            "🔗 <a href='{link}'>Посмотреть вакансию</a>\n"
            "──────────────────"
        ).format(
            location=vac.get('location', 'Не указано'),
            experience=vac.get('experience', 'Не указан'),
            skills= vac['skills'][:300],
            link=vac['link']
        )
        
        await bot.send_message(
            chat_id=user_id,
            text="".join(message),
            parse_mode="HTML"
        )
        await asyncio.sleep(1.5)
        
        # Если пользователь в списке для задержки и это каждая 3-я вакансия
        if i % 5 == 0:
            logger.info(f"[{datetime.now()}] ⏳ Отправлено 5 вакансии, пауза 10 минут для пользователя {user_id}..") 
            await asyncio.sleep(600)  # Задержка только для этого пользователя

async def send_hr_vacancies_to_user(bot: Bot, user_id: int, vacancies: list):
    """Отправляет HR-вакансии пользователю с возможной задержкой"""

    for i, vac in enumerate(vacancies, 1):
        # message = [
        #     "🔔 <b>Специальные HR-вакансии:</b>\n",
        #     f"✨ <b>{vac['title']}</b>\n",
        #     f"🏛 <i>{vac['company']}</i>\n\n",
        #     f"🌍 <b>Локация:</b> {vac['location']}\n",
        #     f"💼 <b>Навыки:</b> {vac['skills'][:150]}\n",
        #     f"📝 <b>Описание:</b> {vac['description'][:500]} ...\n\n",
        #     f"🔗 <b>Контакты для связи:</b> {vac['contact']}\n"
        # ]
        
        message = (
            "🌟 <b>Прямая вакансия от HR</b> 🌟\n"
            "══════════════════════\n"
            f"🎯 <b>Должность:</b> {vac['title']}\n"
            f"🏢 <b>Компания:</b> {vac['company']}\n"
            f"🌎 <b>Локация:</b> {vac.get('location', 'Не указана')}\n\n"
            
            "🔹 <b>Требуемые навыки:</b>\n"
            f"{(vac['skills'][:200])}\n\n"
            
            "📌 <b>Описание вакансии:</b>\n"
            f"{vac['description'][:600]}\n\n"
            
            "📞 <b>Контакты для отклика:</b>\n"
            f"   {vac['contact']}\n"

        )
        
        await bot.send_message(
            chat_id=user_id,
            text="".join(message),
            parse_mode="HTML"
        )
        await asyncio.sleep(1)

        print('Отправлена hr вакансия')
        
        if i % 3 == 0:
            logger.info(f"[{datetime.now()}] ⏳ Отправлено 3 HR-вакансии, пауза 10 минут для пользователя {user_id}..") 
            await asyncio.sleep(600)




async def send_personalized_vacancies(bot: Bot):
    """Рассылает только новые вакансии, появившиеся с последней проверки"""
    global vacancy_counter
    logger.info(f"[{datetime.now()}] Начало рассылки вакансий") 

    try:
        current_time = datetime.now()
        
        # 1. Фильтрация свежих вакансий
        fresh_vacancies = {}
        fresh_hr_vacancies = {}

        for vid, v in vacanciessss.items():
            try:
                try:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S')
                
                if vacancy_date >= current_time - timedelta(hours=24):
                    fresh_vacancies[vid] = v
            except Exception as e:
                logger.info(f"[{datetime.now()}] Ошибка парсинга даты для вакансии {vid}: {e}") 
                continue


        for vid, v in hr_vacanciess.items():
            try:
                try:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    vacancy_date = datetime.strptime(str(v['date']), '%Y-%m-%d %H:%M:%S')
                
                if vacancy_date >= current_time - timedelta(hours=24):
                    fresh_hr_vacancies[vid] = v
            except Exception as e:
                logger.info(f"[{datetime.now()}] Ошибка парсинга даты для вакансии {vid}: {e}") 
                continue
        
        

        if not fresh_vacancies and not fresh_hr_vacancies:
            logger.info(f"[{datetime.now()}]  Нет новых вакансий для рассылки") 
            return
            
        # 2. Создаем задачи для каждого пользователя
        tasks = []
        for user_id, user_categories in selected_subcategories.items():
            user_cities = selected_cities.get(user_id, set())
            
            # Фильтруем вакансии для пользователя
            # matched_vacancies = [
            # v for v in fresh_vacancies.values()
            # if (v.get('location') is not None and  # Проверяем, что location не None
            #     v['location'] in user_cities and
            #     any(cat in v['categories'] for cat in user_categories) and
            #     (v.get('experience') == user_expierence.get(user_id) or v.get('experience') == 'Не указано'))
            # ]

            matched_vacancies = [
                v for v in fresh_vacancies.values()
                if (v.get('location') is not None and
                v['location'] in user_cities and
                any(cat in v['categories'] for cat in user_categories) and
                (v.get('experience') in user_expierence.get(user_id, set()) or 
                v.get('experience') == 'Не указано'))
                ]

            matched_hr_vacancies = [
                v for v in fresh_hr_vacancies.values()
                if (v.get('location') is not None and  
                v['location'] in user_cities and
                any(cat in v['categories'] for cat in user_categories) and
                (v.get('experience') or user_expierence.get(user_id, set()) or v.get('experience') == 'Не указано'))
            ]
            

            # Исключаем уже отправленные
            previously_sent_links = {vac['link'] for vac in send_vacancies.get(user_id, [])}
            new_matched_vacancies = [vac for vac in matched_vacancies if vac['link'] not in previously_sent_links]

            new_matched_hr_vacancies = [vac for vac in matched_hr_vacancies if vac['link'] not in previously_sent_links]

            # Обновляем информацию об отправленных вакансиях
            
            if user_id in last_send_time:
                time_since_last_send = current_time - last_send_time[user_id]
                if time_since_last_send < timedelta(minutes=10):
                    logger.info(f"[{datetime.now()}] Пропускаем рассылку для {user_id} - не прошло 10 минут") 
                    continue
            

            if new_matched_hr_vacancies:
                task = asyncio.create_task(
                     send_hr_vacancies_to_user(bot, user_id, new_matched_hr_vacancies))
                tasks.append(task)

            if new_matched_vacancies:
                    # Запускаем асинхронную задачу отправки
                task = asyncio.create_task(
                    send_vacancies_to_user(bot, user_id, new_matched_vacancies)
                    )
                tasks.append(task)
                    
            

            if new_matched_vacancies or new_matched_hr_vacancies:
                if user_id not in send_vacancies:
                    send_vacancies[user_id] = []
                send_vacancies[user_id].extend(new_matched_vacancies + new_matched_hr_vacancies)
                last_send_time[user_id] = current_time

                
        # Ожидаем завершения всех задач
        await asyncio.gather(*tasks)
        
    except Exception as e:
        logger.info(f"[{datetime.now()}] Критическая ошибка в рассылке: {e}") 



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
    logger.info(f"[{datetime.now()}] Зашли в функцию hot_resume") 
    
    vacancies = await load_vacancies_for_analysis(vacancy_category)
    logger.info(f"[{datetime.now()}] Перешли к промту") 
    prompt = f"""
        Ты — HR-эксперт с 10+ лет опыта в IT-рекрутинге. 
        Проанализируй резюме для позиции {vacancy_category} и дай рекомендации, которые увеличат шансы на отклик на 50%. 

        **Жесткие правила:**
        1. Только факты из резюме (не додумывай)
        2. Сравнивай с вакансиями {vacancies[:25]}
        3. Пиши как личный консультант (без шаблонов)
        4. Макс. 2500 символов
        5. Не используй курсив, используй теги <b> для выделения жирного текста.

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
