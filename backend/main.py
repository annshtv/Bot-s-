import urllib.request
import urllib.error

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import json

from database import get_connection, create_tables


app = FastAPI()


# --------------------------------------------------
# CORS — связь frontend с backend
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    # Разрешаем локальный React/Vite frontend.
    # Подойдут localhost:5173, localhost:5174 и другие порты.
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


create_tables()
# Создаём таблицу и добавляем недостающие колонки


# --------------------------------------------------
# Проверка backend
# --------------------------------------------------

@app.get("/api/health")
def health():
    return {"status": "ok"}


# --------------------------------------------------
# Генерация структуры бота
# --------------------------------------------------

class BusinessDescription(BaseModel):
    # Текст с описанием бизнеса
    description: str


@app.post("/api/generate-structure")
def generate_structure(data: BusinessDescription):
    # Переводим текст в нижний регистр
    description = data.description.lower()

    if "кофе" in description or "кафе" in description:
        sections = [
            "Меню",
            "Бронирование",
            "Контакты",
            "Отзывы"
        ]

    elif "салон" in description or "красот" in description:
        sections = [
            "Услуги",
            "Запись",
            "Контакты",
            "Цены"
        ]

    else:
        sections = [
            "Услуги",
            "О нас",
            "Контакты",
            "FAQ"
        ]

    return {"sections": sections}


# --------------------------------------------------
# Одна услуга
# --------------------------------------------------

class ServiceItem(BaseModel):
    # Название услуги
    name: str

    # Цена услуги
    price: float = 0


# --------------------------------------------------
# Полная конфигурация Telegram-бота
# --------------------------------------------------

class BotConfig(BaseModel):
    # Название бизнеса
    business_name: str

    # Описание бизнеса
    description: str = ""

    # Язык бота: ru или kk
    language: str = "ru"

    # Включённые функции из экрана "Структура бота"
    features: list[str] = []

    # Услуги и их цены
    services: list[ServiceItem] = []

    # Телефон
    phone: str = ""

    # Адрес
    address: str = ""

    # График работы
    working_hours: str = ""

    # Telegram token от BotFather
    telegram_token: str = ""

    # Username Telegram-бота
    telegram_username: str = ""

    # Разделы меню Telegram-бота
    sections: list[str] = []


class TelegramTokenRequest(BaseModel):
    token: str


# --------------------------------------------------
# Общая проверка Telegram token
# --------------------------------------------------

def check_telegram_token(token: str):
    # Проверяем базовый формат токена
    if ":" not in token or not token.isascii():
        raise HTTPException(
            status_code=400,
            detail="Invalid Telegram bot token"
        )

    # Формируем адрес Telegram API
    url = f"https://api.telegram.org/bot{token}/getMe"

    try:
        # Отправляем запрос в Telegram
        with urllib.request.urlopen(url, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))

        # Если Telegram подтвердил токен
        if result.get("ok"):
            return result["result"]

        raise HTTPException(
            status_code=400,
            detail="Invalid Telegram bot token"
        )

    except urllib.error.HTTPError:
        raise HTTPException(
            status_code=400,
            detail="Invalid Telegram bot token"
        )

    except urllib.error.URLError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Telegram"
        )


# --------------------------------------------------
# Создание конфигурации
# --------------------------------------------------

@app.post("/api/bots")
def create_bot(bot: BotConfig):
    # Сначала проверяем Telegram token
    bot_info = check_telegram_token(bot.telegram_token)

    # Получаем настоящий username из Telegram
    telegram_username = bot_info.get("username", "")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bots (
            business_name,
            description,
            language,
            services,
            phone,
            address,
            telegram_token,
            sections,
            features,
            working_hours,
            telegram_username
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            bot.business_name,
            bot.description,
            bot.language,

            json.dumps(
                [service.model_dump() for service in bot.services],
                ensure_ascii=False
            ),

            bot.phone,
            bot.address,
            bot.telegram_token,

            json.dumps(bot.sections, ensure_ascii=False),
            json.dumps(bot.features, ensure_ascii=False),

            bot.working_hours,
            telegram_username
        )
    )

    connection.commit()

    # Получаем id новой записи
    bot_id = cursor.lastrowid

    connection.close()

    return {
        "id": bot_id,
        "message": "Bot created successfully",
        "telegram_username": telegram_username
    }


# --------------------------------------------------
# Получение полной конфигурации
# --------------------------------------------------

@app.get("/api/bots/{bot_id}")
def get_bot(bot_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM bots WHERE id = ?",
        (bot_id,)
    )

    bot = cursor.fetchone()

    connection.close()

    # Если записи нет — возвращаем 404
    if bot is None:
        raise HTTPException(
            status_code=404,
            detail="Bot not found"
        )

    return {
        "id": bot["id"],
        "business_name": bot["business_name"],
        "description": bot["description"],
        "language": bot["language"],

        "services": json.loads(bot["services"] or "[]"),

        "phone": bot["phone"],
        "address": bot["address"],

        "working_hours": bot["working_hours"] or "",

        "telegram_username": bot["telegram_username"] or "",

        "features": json.loads(bot["features"] or "[]"),

        "sections": json.loads(bot["sections"] or "[]"),

        "created_at": bot["created_at"]
    }


# --------------------------------------------------
# Конфигурация специально для Telegram-бота
# --------------------------------------------------

@app.get("/api/bots/{bot_id}/telegram-config")
def get_telegram_config(bot_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM bots WHERE id = ?",
        (bot_id,)
    )

    bot = cursor.fetchone()

    connection.close()

    if bot is None:
        raise HTTPException(
            status_code=404,
            detail="Bot not found"
        )

    return {
        "id": bot["id"],
        "business_name": bot["business_name"],
        "language": bot["language"],

        "services": json.loads(
            bot["services"] or "[]"
        ),

        "address": bot["address"],

        "working_hours": bot["working_hours"] or "",

        "features": json.loads(
            bot["features"] or "[]"
        ),

        "sections": json.loads(
            bot["sections"] or "[]"
        )
    }


# --------------------------------------------------
# Изменение конфигурации
# --------------------------------------------------

@app.put("/api/bots/{bot_id}")
def update_bot(bot_id: int, bot: BotConfig):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE bots
        SET
            business_name = ?,
            description = ?,
            language = ?,
            services = ?,
            phone = ?,
            address = ?,
            telegram_token = ?,
            sections = ?,
            features = ?,
            working_hours = ?,
            telegram_username = ?
        WHERE id = ?
        """,
        (
            bot.business_name,
            bot.description,
            bot.language,

            json.dumps(
                [service.model_dump() for service in bot.services],
                ensure_ascii=False
            ),

            bot.phone,
            bot.address,
            bot.telegram_token,

            json.dumps(bot.sections, ensure_ascii=False),
            json.dumps(bot.features, ensure_ascii=False),

            bot.working_hours,
            bot.telegram_username,

            bot_id
        )
    )

    # Если такой записи нет
    if cursor.rowcount == 0:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Bot not found"
        )

    connection.commit()
    connection.close()

    return {
        "id": bot_id,
        "message": "Bot configuration updated"
    }


# --------------------------------------------------
# Проверка Telegram token
# --------------------------------------------------

@app.post("/api/validate-token")
def validate_token(data: TelegramTokenRequest):
    # Используем общую функцию проверки
    bot_info = check_telegram_token(data.token)

    return {
        "valid": True,
        "message": "Bot connected successfully",
        "username": bot_info.get("username"),
        "first_name": bot_info.get("first_name")
    }