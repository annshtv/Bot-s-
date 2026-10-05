import sqlite3
# Встроенная библиотека Python для работы с SQLite


DATABASE_NAME = "botly.db"
# Файл нашей базы данных


def get_connection():
    # Создаём подключение к базе данных
    connection = sqlite3.connect(DATABASE_NAME)

    # Позволяет обращаться к колонкам по имени:
    # bot["business_name"] вместо bot[1]
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    # Подключаемся к базе
    connection = get_connection()
    cursor = connection.cursor()

    # Создаём основную таблицу, если её ещё нет
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            description TEXT,
            language TEXT,
            services TEXT,
            phone TEXT,
            address TEXT,
            telegram_token TEXT,
            sections TEXT,
            features TEXT,
            working_hours TEXT,
            telegram_username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Получаем список колонок существующей таблицы
    cursor.execute("PRAGMA table_info(bots)")
    columns = [column["name"] for column in cursor.fetchall()]

    # Эти проверки нужны потому, что botly.db у нас уже существует.
    # Если новой колонки ещё нет, добавляем её.

    if "features" not in columns:
        cursor.execute("ALTER TABLE bots ADD COLUMN features TEXT")

    if "working_hours" not in columns:
        cursor.execute("ALTER TABLE bots ADD COLUMN working_hours TEXT")

    if "telegram_username" not in columns:
        cursor.execute("ALTER TABLE bots ADD COLUMN telegram_username TEXT")

    # Сохраняем изменения
    connection.commit()

    # Закрываем соединение
    connection.close()