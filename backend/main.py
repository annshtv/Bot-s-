from fastapi import FastAPI, HTTPException
# FastAPI создаёт backend
# HTTPException позволяет возвращать ошибки, например 404

from pydantic import BaseModel
# BaseModel описывает данные, которые приходят от frontend

import json
# Нужен, чтобы сохранять списки в SQLite как JSON-текст

from database import get_connection, create_tables
# Импортируем функции для подключения к базе и создания таблицы


app = FastAPI()
# Создаём FastAPI-приложение


create_tables()
# При запуске backend создаём таблицу bots, если её ещё нет


@app.get("/api/health")
def health():
    return {"status": "ok"}


class BusinessDescription(BaseModel):
    description: str
# Модель данных для генерации структуры


@app.post("/api/generate-structure")
def generate_structure(data: BusinessDescription):

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


class BotConfig(BaseModel):
    # Описываем данные одного создаваемого бота

    business_name: str
    description: str = ""
    language: str = "ru"
    services: list[str] = []
    phone: str = ""
    address: str = ""
    telegram_token: str = ""
    sections: list[str] = []


@app.post("/api/bots")
def create_bot(bot: BotConfig):
    # Создаём новую конфигурацию бота

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
            sections
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            bot.business_name,
            bot.description,
            bot.language,
            json.dumps(bot.services, ensure_ascii=False),
            bot.phone,
            bot.address,
            bot.telegram_token,
            json.dumps(bot.sections, ensure_ascii=False)
        )
    )

    connection.commit()

    bot_id = cursor.lastrowid
    # Получаем id созданного бота

    connection.close()

    return {
        "id": bot_id,
        "message": "Bot configuration created"
    }


@app.get("/api/bots/{bot_id}")
def get_bot(bot_id: int):
    # Получаем бота по его id

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
        "description": bot["description"],
        "language": bot["language"],
        "services": json.loads(bot["services"]),
        "phone": bot["phone"],
        "address": bot["address"],
        "sections": json.loads(bot["sections"]),
        "created_at": bot["created_at"]
    }


@app.put("/api/bots/{bot_id}")
def update_bot(bot_id: int, bot: BotConfig):
    # Обновляем уже существующую конфигурацию

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
            sections = ?
        WHERE id = ?
        """,
        (
            bot.business_name,
            bot.description,
            bot.language,
            json.dumps(bot.services, ensure_ascii=False),
            bot.phone,
            bot.address,
            bot.telegram_token,
            json.dumps(bot.sections, ensure_ascii=False),
            bot_id
        )
    )

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