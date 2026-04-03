import cv2
from ultralytics import YOLO


# =========================
# 📏 DISTANCE FUNCTION
# =========================
def estimate_distance(pixel_width, real_width=0.15, focal=152):
    if pixel_width <= 0:
        return None  # 🔥 lebih aman dari 0 palsu
    return (real_width * focal) / pixel_width


class DetectionController:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

        # 1 kamera
        self.cam = cv2.VideoCapture(0)

        # resolusi ringan
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

    def process_frame(self, frame):
        nearest_obj = None
        min_distance = float("inf")

        results = self.model(frame, verbose=False)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = self.model.names[cls]

                if label in ['car', 'motorcycle']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    width = x2 - x1

                    distance = estimate_distance(width)

                    if distance is None:
                        continue

                    # cari paling dekat
                    if distance < min_distance:
                        min_distance = distance
                        nearest_obj = {
                            "label": label,
                            "distance": distance,
                            "bbox": (x1, y1, x2, y2)
                        }

        info = {"label": None, "distance": None}

        if nearest_obj:
            x1, y1, x2, y2 = nearest_obj["bbox"]
            label = nearest_obj["label"]
            distance = nearest_obj["distance"]

            text = f"{label} {distance:.1f}m"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255), 2)

            info["label"] = label
            info["distance"] = distance

        return frame, info

    def get_frame(self):
        ret, frame = self.cam.read()

        info = {"label": None, "distance": None}

        if not ret:
            return None, info

        frame, info = self.process_frame(frame)

        return frame, info