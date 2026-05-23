import cv2

for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        for _ in range(5):
            cap.read()

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(f"camera_{i}.jpeg",frame)