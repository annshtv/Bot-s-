from fastapi import FastAPI  # Подключаю FastAPI

app = FastAPI()  # Создаю backend-приложение


@app.get("/api/health")  # Проверка, работает ли backend
def health():
    return {"status": "ok"}  # Возвращает ok, если всё запустилось