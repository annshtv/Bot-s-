import sqlite3
# Подключаем встроенную библиотеку Python для работы с SQLite


DATABASE_NAME = "botly.db"
# Имя файла базы данных


def get_connection():
    # Создаём соединение с базой данных

    connection = sqlite3.connect(DATABASE_NAME)

    # Позволяет получать данные по названиям колонок
    connection.row_factory = sqlite3.Row

    return connection
    # Возвращаем готовое соединение


def create_tables():
    # Создаём таблицу bots, если её ещё нет

    connection = get_connection()

    cursor = connection.cursor()
    # Cursor выполняет SQL-команды


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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    connection.commit()
    # Сохраняем изменения


    connection.close()
    # Закрываем соединение
    