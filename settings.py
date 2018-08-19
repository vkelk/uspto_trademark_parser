import os
from dotenv import load_dotenv


load_dotenv()
DB_USER = os.getenv("DB_USER") or 'postgres'
DB_PASSWORD = os.getenv("DB_PASSWORD") or None
DB_HOST = os.getenv("DB_HOST") or '127.0.0.1'
DB_NAME = os.getenv("DB_NAME") or 'trademark'

db_config = {
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST,
        'database': DB_NAME,
    }
