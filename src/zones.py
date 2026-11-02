import cv2
import numpy as np
import json

def load_zones(config_path):
    """Loads the zone polygon coordinates from a JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)

def is_point_in_polygon(point, polygon):
    """Checks if a point (x, y) is inside a polygon."""
    poly_array = np.array(polygon, np.int32)
    result = cv2.pointPolygonTest(poly_array, (float(point[0]), float(point[1])), False)
    return result >= 0
