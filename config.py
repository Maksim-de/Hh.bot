import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Чтение токена из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN_DEPS= os.getenv("TOKEN_DEPS")
host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
# if not TOKEN_WEATHER:
#     raise ValueError("Переменная окружения TOKEN_WEATHER не установлена!")