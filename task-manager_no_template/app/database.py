import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    #"host": os.getenv("DB_HOST"),
    "host": 'task-manager_no_template-db-1',
    "port": os.getenv("DB_PORT"),
}

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
