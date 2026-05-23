import cv2
import requests
import base64
import time
import json

CAMERA = 1
MODEL = "moondream"
OLLAMA_URL="http://localhost:11434/api/chat"
DELAY=3 #seconds
PROMPT="You are an expert in canine behavior and body language. Analyze this image of Butter, a Golden Retriever. Carefully observe her eyes (soft/hard, squinting, wide), ears (position: forward/back/relaxed), nose (twitching, sniffing, dry/wet), tail (height, movement, tension), posture (weight distribution, muscle tension, stance), and overall body language. In exactly one confident sentence, describe what Butter is most likely doing at this precise moment and what she wants or needs right now."

def capture_frame():
    cap = cv2.VideoCapture(CAMERA)
    for i in range(10):
        cap.read()
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("image.jpg",frame)
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

if __name__== "__main__":
    while True :
        frame = capture_frame()

        # In the case where frame is none encode frame crashes
        if frame is None:
            continue

        image_b64 = encode_frame(frame)

        ask_moondream(
            image_b64=image_b64,
            prompt=PROMPT
        )
        time.sleep(DELAY)