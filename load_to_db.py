import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def load(values: list[tuple]) -> None:
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    conn = psycopg2.connect(
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )
    try:
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS raw_data(
            "userId" INTEGER,
            id INT PRIMARY KEY,
            title TEXT,
            body TEXT
        )""")

        conn.commit()

        cursor.executemany('INSERT INTO raw_data ("userId", id, title, body) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING', values)

        conn.commit()

        cursor.execute('SELECT COUNT(*) FROM raw_data')
        print("Всего строк в таблице:", cursor.fetchone()[0])

        cursor.close()
    finally:
        conn.close()
