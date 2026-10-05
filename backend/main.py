from fastapi import FastAPI, HTTPException
# FastAPI создаёт backend
# HTTPException позволяет возвращать ошибки

from pydantic import BaseModel
# BaseModel описывает структуру входящих данных

import json
# Нужен для преобразования списков и объектов в JSON

from database import get_connection, create_tables
# Функции для работы с SQLite


app = FastAPI()
# Создаём приложение


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


# --------------------------------------------------
# Создание конфигурации
# --------------------------------------------------

@app.post("/api/bots")
def create_bot(bot: BotConfig):
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

            # model_dump превращает ServiceItem в обычный словарь
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
            bot.telegram_username
        )
    )

    connection.commit()

    # Получаем id новой записи
    bot_id = cursor.lastrowid

    connection.close()

    return {
        "id": bot_id,
        "message": "Bot configuration created"
    }


# --------------------------------------------------
# Получение конфигурации
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