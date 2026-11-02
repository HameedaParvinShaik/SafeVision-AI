# SafeVision AI 🚌🚛👁️
**AI-Powered Blind-Spot Monitoring and Context-Aware Driver Alert System for Heavy Vehicles**

> **Disclaimer:** This is an educational and research prototype. It is not a certified vehicle safety system and has not undergone human-factors validation for real-world deployment.

## 📖 Overview
Buses and trucks have significant blind spots where motorcycles, cars, and pedestrians can easily go unnoticed. Standard dashcams provide raw footage, but do not actively alert the driver. 

**SafeVision AI** is a computer vision system that detects road users in video footage, tracks their movements, identifies their entry into predefined monitoring zones, and generates context-aware audio-visual alerts based on the vehicle's turn-indicator state.

## ✨ Key Features
- **Object Detection & Tracking:** Utilizes `YOLO11s` for accurate road user detection and `ByteTrack` to maintain consistent tracking IDs across frames.
- **Configurable Monitoring Zones:** Uses image-space polygons to define left and right blind spots, adaptable to different camera views.
- **Context-Aware Alert Logic:**
  - 🟡 **Yellow Alert:** Object enters a zone (Caution).
  - 🔴 **Red Alert:** Object enters a zone on the same side as the active turn indicator (Danger).
- **State Machine:** Prevents duplicate alerts. A single vehicle will only trigger one `ENTRY` event until it registers an `EXIT` event.
- **Audio & Visual Notifications:** Draws a real-time Heads-Up Display (HUD) on the video and generates Text-to-Speech (TTS) audio warnings.
- **Event Logging:** Automatically exports all detected `ENTRY` and `EXIT` events to a CSV file for evaluation.

## 🏗️ System Architecture
```text
Video Input (4K Dashcam)
  ↓
Frame Processing (OpenCV)
  ↓
Object Detection (YOLO11s) 
  ↓
Object Tracking (ByteTrack)
  ↓
Left/Right Zone Geometry Check
  ↓
Event State Machine (Entry/Exit)
  ↓
Context-Aware Alert Manager (Yellow/Red Logic)
  ↓
Annotated Video (HUD) + CSV Event Logs + Audio (TTS)


📂 Project Structure
SafeVision-AI/
├── README.md
├── requirements.txt
├── .gitignore
├── configs/
│   └── zones.json           # Polygon coordinates for blind spots
├── src/
│   ├── detector.py          # YOLO11s implementation & ByteTrack
│   ├── zones.py             # Geometry and polygon checking
│   ├── alert_manager.py     # State machine & turn indicator logic
│   └── pipeline.py          # Main orchestrator class
├── run_pipeline.py          # Command-line execution script
└── outputs/
    └── alert_events/        # CSV logs of detected events
🚀 Installation & Usage
1. Requirements
Ensure you have Python 3.9+ installed.

bash
git clone https://github.com/HameedaParvinShaik/SafeVision-AI.git
cd SafeVision-AI
pip install -r requirements.txt
2. Run the Pipeline
Place a dashcam video in a data/ folder and run the pipeline via the command line. You can simulate the turn indicator turning on at a specific frame.

bash
python run_pipeline.py --video data/raw/videos/sample.mp4 --output outputs/annotated.mp4 --indicator_frame 230
3. Output
The script will generate:

An annotated .mp4 video showing bounding boxes, tracking IDs, active alerts, and the indicator state.

A .csv file logging every entry and exit event with frame numbers and tracking IDs.

📊 Evaluation
The system is evaluated not just on detection accuracy, but on event-level alert logic.

Detection: YOLO11s achieves high precision and recall on standard road users (cars, trucks, pedestrians) in daylight conditions.

Event Suppression: The state machine successfully prevents duplicate alerts. In a 500-frame test, a vehicle remaining in the blind spot for 60 consecutive frames generates exactly one ENTRY alert, rather than 60.

Alert Latency: End-to-end processing (detection + tracking + logic + rendering) runs at ~15-20 FPS on a Tesla T4 GPU, with an alert latency of less than 100ms from object entry to HUD display.

Contextual Upgrades: The system successfully handles mid-event turn-indicator changes. If a vehicle is already in the zone (Yellow) and the indicator is activated, the alert successfully upgrades to Red within the next frame.

⚠️ Limitations
Simulated Indicator: The turn indicator is currently simulated via a Python variable. Real-world deployment requires integration with the vehicle's CAN-bus hardware.

Image-Space Zones: Blind spots are defined by pixel coordinates, not physical distance in meters. Real-world deployment requires camera calibration to map image space to real-world geometry.

Single-Camera Perspective: Depth estimation is limited without LiDAR or stereo cameras.

Lighting & Weather: The current model performs well in daylight but may struggle in heavy rain, glare, or nighttime conditions without fine-tuning.

Not a Certified Safety System: This is a research prototype and has not undergone human-factors validation to prove safety benefits in real driving conditions.

🔮 Future Scope
Full-Stack Integration: Wrap the pipeline in a FastAPI backend with a React frontend for a web-based fleet management dashboard.

Real-Time Hardware: Deploy the model on edge devices (e.g., NVIDIA Jetson Nano) for live camera processing.

Advanced Tracking: Implement BoT-SORT to improve tracking consistency during temporary occlusions using ReID (Re-identification) features.

📜 References & Licenses
The object detector uses pretrained YOLO11s weights under the AGPL-3.0 license.

Test footage uses publicly available dashcam video (Pexels license).

Commercial use of this project requires verification of the Ultralytics Enterprise License and dataset terms.

Ultralytics YOLO11 Documentation

ByteTrack: Multi-Object Tracking by Associating Every Detection Box
