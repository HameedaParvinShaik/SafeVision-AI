import cv2
import time
import numpy as np
import pandas as pd
from .zones import is_point_in_polygon
from .alert_manager import ZoneEventManager, AlertManager

class SafeVisionPipeline:
    def __init__(self, tracker, zones_config):
        self.tracker = tracker
        self.zones = zones_config
        self.event_manager = ZoneEventManager()
        self.alert_manager = AlertManager()

    def process_video(self, video_path, output_path, indicator_schedule=None):
        if indicator_schedule is None:
            indicator_schedule = {}
            
        print(f"Starting pipeline for: {video_path}")
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        out_width, out_height = 1280, 720
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (out_width, out_height))
        
        frame_idx = 0
        current_indicator = "NONE"
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            # Simulate indicator changes
            if frame_idx in indicator_schedule:
                current_indicator = indicator_schedule[frame_idx]
                
            # 1. Detection & Tracking
            detections = self.tracker.process_frame(frame)
            
            # Convert dataclass to dict for the event manager
            det_dicts = [
                {'track_id': d.track_id, 'bbox': d.bbox, 'class_name': d.class_name} 
                for d in detections
            ]
            
            # 2. Event & Alert Logic
            events = self.event_manager.update(det_dicts, frame_idx, self.zones)
            alerts = self.alert_manager.process_events(events, current_indicator)
            
            # 3. Visualization
            vis_frame = cv2.resize(frame, (out_width, out_height))
            
            # Draw Zones
            cv2.polylines(vis_frame, [np.array(self.zones["left_blind_spot"], np.int32)], True, (0, 0, 255), 2)
            cv2.polylines(vis_frame, [np.array(self.zones["right_blind_spot"], np.int32)], True, (0, 255, 255), 2)
            
            # Draw Detections
            scale_x = out_width / width
            scale_y = out_height / height
            
            for det in detections:
                x1 = int(det.bbox[0] * scale_x)
                y1 = int(det.bbox[1] * scale_y)
                x2 = int(det.bbox[2] * scale_x)
                y2 = int(det.bbox[3] * scale_y)
                
                cv2.rectangle(vis_frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.putText(vis_frame, f"ID:{det.track_id}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Draw HUD
            cv2.putText(vis_frame, f"Indicator: {current_indicator}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            y_offset = 80
            for track_id, alert in self.alert_manager.active_alerts.items():
                color = (0, 0, 255) if alert['level'] == 'RED' else (0, 255, 255)
                alert_text = f"{alert['level']} ALERT: {alert['class_name']} on {alert['zone']}"
                
                (text_w, text_h), _ = cv2.getTextSize(alert_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                cv2.rectangle(vis_frame, (20, y_offset - 20), (30 + text_w, y_offset + 10), (0, 0, 0), -1)
                cv2.putText(vis_frame, alert_text, (25, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y_offset += 40

            out.write(vis_frame)
            
            if frame_idx % 100 == 0:
                print(f"Processed {frame_idx} frames...")
                
            frame_idx += 1
            
        cap.release()
        out.release()
        
        processing_time = time.time() - start_time
        print(f"Finished processing in {processing_time:.2f} seconds.")
        
        # Save events to CSV
        df_events = pd.DataFrame(self.event_manager.events)
        df_events['video_name'] = video_path.split('/')[-1]
        csv_path = output_path.replace('.mp4', '_events.csv')
        df_events.to_csv(csv_path, index=False)
        print(f"Events saved to: {csv_path}")
        
        return self.event_manager.events
