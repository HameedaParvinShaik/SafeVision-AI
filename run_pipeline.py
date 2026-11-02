import argparse
import sys
import os

# Ensure the src directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.detector import VideoTracker
from src.pipeline import SafeVisionPipeline
from src.zones import load_zones

def main():
    parser = argparse.ArgumentParser(description='SafeVision AI Pipeline')
    parser.add_argument('--video', type=str, required=True, help='Path to input video')
    parser.add_argument('--output', type=str, required=True, help='Path to save annotated video')
    parser.add_argument('--zones', type=str, default='configs/zones.json', help='Path to zones JSON')
    parser.add_argument('--indicator_frame', type=int, default=-1, help='Frame to turn on RIGHT indicator')
    args = parser.parse_args()

    # Load zones
    zones = load_zones(args.zones)

    # Initialize Tracker
    tracker = VideoTracker(model_path='yolo11s.pt')

    # Initialize Pipeline
    pipeline = SafeVisionPipeline(tracker, zones)

    # Setup indicator schedule (simulate turning right)
    indicator_schedule = {}
    if args.indicator_frame > 0:
        indicator_schedule[args.indicator_frame] = 'RIGHT'

    # Run
    pipeline.process_video(args.video, args.output, indicator_schedule)

if __name__ == '__main__':
    main()
