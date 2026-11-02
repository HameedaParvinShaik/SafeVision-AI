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
## 🎥 Demo
[![SafeVision AI Demo](https://img.youtube.com/vi/NZv6LAPPIxw/0.jpg)](https://youtu.be/NZv6LAPPIxw)

*Click the image above to watch the full pipeline demo. You will see the bounding boxes, the tracking IDs, the Heads-Up Display (HUD), and hear the real-time text-to-speech audio alerts for Yellow and Red warnings.*
## 🏗️ System Architecture

Video Input (4K Dashcam) ➔ Frame Processing (OpenCV) ➔ Object Detection (YOLO11s) ➔ Object Tracking (ByteTrack) ➔ Left/Right Zone Geometry Check ➔ Event State Machine (Entry/Exit) ➔ Context-Aware Alert Manager (Yellow/Red Logic) ➔ Annotated Video (HUD) + CSV Event Logs + Audio (TTS)

## 📂 Project Structure

SafeVision-AI/  
├── README.md  
├── requirements.txt  
├── .gitignore  
├── configs/  
│   └── zones.json (Polygon coordinates for blind spots)  
├── src/  
│   ├── detector.py (YOLO11s implementation & ByteTrack)  
│   ├── zones.py (Geometry and polygon checking)  
│   ├── alert_manager.py (State machine & turn indicator logic)  
│   └── pipeline.py (Main orchestrator class)  
├── run_pipeline.py (Command-line execution script)  
└── outputs/  
&nbsp;&nbsp;&nbsp;&nbsp;└── alert_events/ (CSV logs of detected events)  

## 🚀 Installation & Usage

### 1. Requirements
Ensure you have Python 3.9+ installed. 

```bash
git clone https://github.com/HameedaParvinShaik/SafeVision-AI.git
cd SafeVision-AI
pip install -r requirements.txt
