from ultralytics import YOLO
import cv2
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox: List[int] # [x1, y1, x2, y2]
    track_id: Optional[int] = None

class VideoTracker:
    def __init__(self, model_path='yolo11s.pt'):
        self.model = YOLO(model_path)
        # COCO IDs: 0=person, 1=bicycle, 2=car, 3=motorcycle, 5=bus, 7=truck
        self.target_classes = [0, 1, 2, 3, 5, 7]
        
    def process_frame(self, frame):
        results = self.model.track(
            frame, 
            persist=True, 
            tracker="bytetrack.yaml", 
            verbose=False,
            classes=self.target_classes
        )[0]
        
        detections = []
        
        if results.boxes is None or results.boxes.id is None:
            return detections
            
        for box in results.boxes:
            class_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            track_id = int(box.id[0].item()) if box.id is not None else None
            
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            bbox = [int(x1), int(y1), int(x2), int(y2)]
            
            # Ego-vehicle filter: Removes the dashboard hood if detected as a car
            is_ego = False
            if class_id == 2: 
                frame_height, frame_width = frame.shape[:2]
                box_width = x2 - x1
                box_height = y2 - y1
                if y2 > (frame_height - 50) and (box_width * box_height) > (frame_width * frame_height * 0.15):
                    is_ego = True
            
            if not is_ego:
                detections.append(
                    Detection(
                        class_id=class_id,
                        class_name=self.model.names[class_id],
                        confidence=round(conf, 2),
                        bbox=bbox,
                        track_id=track_id
                    )
                )
        return detections
