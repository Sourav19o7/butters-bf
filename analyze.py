import cv2
import requests
import base64
import time
import datetime
from feedback import init_db, save_feedback
from dotenv import load_dotenv
import os

load_dotenv()



CAMERA = os.getenv("CAMERA")
MODEL = os.getenv("MODEL")
OLLAMA_URL=os.getenv("OLLAMA_URL")
DELAY=3 #seconds
PROMPT="You are an expert in canine behavior and body language. Analyze this image of Butter, a Golden Retriever. Carefully observe her eyes (soft/hard, squinting, wide), ears (position: forward/back/relaxed), nose (twitching, sniffing, dry/wet), tail (height, movement, tension), posture (weight distribution, muscle tension, stance), and overall body language. In exactly one confident sentence, describe what Butter is most likely doing at this precise moment and what she wants or needs right now."

def generate_image():
    time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pathname = f"data/frames/{time}.jpg"
    return pathname

def capture_frame(image_path):
    cap = cv2.VideoCapture(CAMERA)
    for i in range(10):
        cap.read()
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(image_path,frame)
    cap.release()
    return frame

def encode_frame(frame):
    frame=cv2.resize(frame, (640, 480))
    _,buffer = cv2.imencode(".jpg", frame)
    image_b64 = base64.b64encode(buffer.tobytes()).decode("utf-8")
    return image_b64

def ask_moondream(image_b64, prompt):

    payload={
        "model" : MODEL,
        "stream": False,
        "messages" : [
            {
                "role" : "user",
                "content" : prompt,
                "images" : [
                    image_b64
                ]
            }
        ]
    }

    resp = requests.post(url=OLLAMA_URL, json=payload, timeout=30)


    ollama_res = resp.json()["message"]["content"]
    
    for word in ollama_res.split():
        print(word, end=" ", flush=True)
        time.sleep(0.05)
    print("")

    return ollama_res

if __name__== "__main__":

    #initialising feedback
    init_db()

    while True :
        image_path = generate_image()
        frame = capture_frame(image_path)

        # In the case where frame is none encode frame crashes
        if frame is None:
            continue

        image_b64 = encode_frame(frame)

        guess = ask_moondream(
            image_b64=image_b64,
            prompt=PROMPT
        )

        correction = input("Correct it (or press Enter to skip): ")

        if(correction):
            save_feedback(
                image_path=image_path,
                moondream_guess= guess,
                correction=correction
            )

        time.sleep(DELAY)