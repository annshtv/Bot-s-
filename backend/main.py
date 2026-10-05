from fastapi import FastAPI
# Импортируем FastAPI — библиотеку, с помощью которой создаём backend

from pydantic import BaseModel
# Импортируем BaseModel — он нужен, чтобы описывать,
# какие данные backend ожидает получить от frontend


app = FastAPI()
# Создаём само FastAPI-приложение


@app.get("/api/health")
# Создаём GET endpoint /api/health
# Он нужен для простой проверки, работает ли backend

def health():
    # Функция, которая выполняется,
    # когда кто-то обращается к /api/health

    return {"status": "ok"}
    # Возвращаем JSON-ответ
    # Если видим status: ok — значит backend работает


class BusinessDescription(BaseModel):
    # Создаём модель данных для запроса от frontend
    # Она описывает, какие данные нам должны прислать

    description: str
    # Ожидаем одно поле description
    # Тип str означает, что это обычный текст


@app.post("/api/generate-structure")
# Создаём POST endpoint /api/generate-structure
# Через него frontend будет отправлять описание бизнеса

def generate_structure(data: BusinessDescription):
    # Создаём функцию generate_structure
    # data — это данные, которые пришли от frontend
    # BusinessDescription говорит FastAPI,
    # что внутри data должно быть поле description

    description = data.description.lower()
    # Берём текст description
    # .lower() переводит весь текст в нижний регистр
    # Это нужно, чтобы "Кофейня", "КОФЕЙНЯ" и "кофейня"
    # обрабатывались одинаково


    if "кофе" in description or "кафе" in description:
        # Проверяем, есть ли в описании слово "кофе" или "кафе"
        # Если да — считаем, что это кофейня или кафе

        sections = [
            "Меню",
            "Бронирование",
            "Контакты",
            "Отзывы"
        ]
        # Создаём список разделов,
        # которые подойдут для кафе


    elif "салон" in description or "красот" in description:
        # Если условие выше не сработало,
        # проверяем, есть ли слова, связанные с салоном красоты

        sections = [
            "Услуги",
            "Запись",
            "Контакты",
            "Цены"
        ]
        # Создаём структуру,
        # подходящую для салона красоты


    else:
        # Если описание не подошло ни под кафе,
        # ни под салон красоты

        sections = [
            "Услуги",
            "О нас",
            "Контакты",
            "FAQ"
        ]
        # Возвращаем универсальный набор разделов
        # для любого другого бизнеса


    return {
        "sections": sections
    }
    # Возвращаем результат frontend в формате JSON
    # Например:
    # {
    #   "sections": ["Меню", "Бронирование", "Контакты", "Отзывы"]
    # }