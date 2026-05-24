import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME=os.getenv("DATABASE_NAME")

def view_feedback():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """SELECT * FROM feedback ORDER BY timestamp DESC"""
    )

    feedbacks = cursor.fetchall()

    for feedback in feedbacks:
        print(f"Id : {feedback[0]}; timestamp : {feedback[1]}, image_path : {feedback[2]}")
        print(f"moondream_guess : {feedback[3]}")
        print(f"correct : {feedback[4]}")
        print("")

    conn.close()

if __name__ =="__main__":
    view_feedback()