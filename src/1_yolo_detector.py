from ultralytics import YOLO
import os
import cv2


IMG_DIR = "data/processed/images"
OUT_DIR = "data/crops"

def detect_and_crop():

    os.makedirs(OUT_DIR, exist_ok=True)

    model = YOLO("yolov8s.pt")

    images = [
        f for f in os.listdir(IMG_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    for img_name in images:
        img_path = os.path.join(IMG_DIR, img_name)
        results = model.predict(img_path, conf=0.15, imgsz=640, verbose=False)

        boxes = results[0].boxes
        img = cv2.imread(img_path)

        idx = 0
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])

            crop = img[y1:y2, x1:x2]
            crop_name = f"{img_name.replace('.jpg','')}_crop{idx}.jpg"
            cv2.imwrite(os.path.join(OUT_DIR, crop_name), crop)

            idx += 1

if __name__ == "__main__":
    detect_and_crop()
