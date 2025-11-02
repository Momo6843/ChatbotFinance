import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv(r"C:\Users\lenovo\Desktop\chatbotFinance\.env")

conn = psycopg2.connect(
    database="ragfinance",
    user="postgres",
    password="006750",
    host="localhost",
    port=5433
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Création tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    tags TEXT[],
    upload_date TIMESTAMP DEFAULT NOW()
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions_history (
    id SERIAL PRIMARY KEY,
    question TEXT,
    answer TEXT,
    pdf_name TEXT,
    page_numbers TEXT[],
    asked_at TIMESTAMP DEFAULT NOW()
);
""")
conn.commit()
