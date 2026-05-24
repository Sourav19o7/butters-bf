import sqlite3
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS feedback ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, image_path TEXT, moondream_guess TEXT, correction TEXT
        )"""
    )

    conn.commit()
    conn.close()

def save_feedback(image_path, moondream_guess, correction):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().isoformat()

    cursor.execute(
        """INSERT INTO feedback(
        timestamp, image_path, moondream_guess, correction) 
        values (?, ?, ?, ?)""",
        (timestamp, image_path, moondream_guess, correction)
    )

    conn.commit()
    conn.close()