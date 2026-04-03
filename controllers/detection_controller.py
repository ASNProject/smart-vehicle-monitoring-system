import cv2
from ultralytics import YOLO


# KALIBRASI BAGIAN INI
def estimate_distance(pixel_width, real_width=0.15, focal=152):
    if pixel_width == 0:
        return 0
    return (real_width * focal) / pixel_width


class DetectionController:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

        self.cam1 = cv2.VideoCapture(0)
        self.cam2 = cv2.VideoCapture(1)

        self.cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.car_count = 0
        self.motor_count = 0

    def process_frame(self, frame):
        car_count = 0
        motor_count = 0

        car_distances = []
        motor_distances = []

        results = self.model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = self.model.names[cls]

                if label in ['car', 'motorcycle']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    width = x2 - x1
                    print("pixel width", width)

                    distance = estimate_distance(width)

                    if label == "car":
                        car_count += 1
                        car_distances.append(distance)
                    else:
                        motor_count += 1
                        motor_distances.append(distance)

                    text = f"{label} {distance:.2f}m"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, text, (x1, y1),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 255, 0), 2)

        return frame, car_count, motor_count, car_distances, motor_distances

    def get_frames(self):
        ret1, frame1 = self.cam1.read()
        ret2, frame2 = self.cam2.read()

        info1 = {
            "car_distances": [],
            "motor_distances": []
        }

        info2 = {
            "car_distances": [],
            "motor_distances": []
        }

        if ret1:
            frame1, _, _, cd1, md1 = self.process_frame(frame1)
            info1["car_distances"] = cd1
            info1["motor_distances"] = md1

        if ret2:
            frame2, _, _, cd2, md2 = self.process_frame(frame2)
            info2["car_distances"] = cd2
            info2["motor_distances"] = md2

        return frame1, frame2, info1, info2
