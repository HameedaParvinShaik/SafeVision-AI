from .zones import is_point_in_polygon

class ZoneEventManager:
    """State machine to track entry and exit events without duplicates."""
    def __init__(self):
        self.states = {}
        self.events = []

    def update(self, detections, frame_idx, zones):
        current_frame_events = []
        
        for det in detections:
            if det['track_id'] is None:
                continue
                
            # Calculate bottom-center anchor point
            anchor_x = int((det['bbox'][0] + det['bbox'][2]) / 2)
            anchor_y = det['bbox'][3]
            
            in_left = is_point_in_polygon((anchor_x, anchor_y), zones["left_blind_spot"])
            in_right = is_point_in_polygon((anchor_x, anchor_y), zones["right_blind_spot"])
            
            current_zone = "LEFT" if in_left else ("RIGHT" if in_right else None)
            
            for zone_name in ["LEFT", "RIGHT"]:
                state_key = (det['track_id'], zone_name)
                previous_state = self.states.get(state_key, "OUTSIDE")
                is_currently_in = (current_zone == zone_name)
                
                if previous_state == "OUTSIDE" and is_currently_in:
                    self.states[state_key] = "INSIDE"
                    event = {'type': 'ENTRY', 'frame': frame_idx, 'track_id': det['track_id'], 'class_name': det['class_name'], 'zone': zone_name}
                    self.events.append(event)
                    current_frame_events.append(event)
                elif previous_state == "INSIDE" and not is_currently_in:
                    self.states[state_key] = "OUTSIDE"
                    event = {'type': 'EXIT', 'frame': frame_idx, 'track_id': det['track_id'], 'class_name': det['class_name'], 'zone': zone_name}
                    self.events.append(event)
                    current_frame_events.append(event)
                    
        return current_frame_events

class AlertManager:
    """Handles the context-aware alert logic based on turn indicators."""
    def __init__(self):
        self.active_alerts = {}

    def process_events(self, events, turn_indicator):
        alerts = []
        for ev in events:
            track_id = ev['track_id']
            zone = ev['zone']
            
            if ev['type'] == 'ENTRY':
                # Determine alert level
                level = "RED" if turn_indicator == zone else "YELLOW"
                alert = {'track_id': track_id, 'zone': zone, 'level': level, 'class_name': ev['class_name']}
                self.active_alerts[track_id] = alert
                alerts.append(alert)
            elif ev['type'] == 'EXIT':
                if track_id in self.active_alerts:
                    del self.active_alerts[track_id]

        # Re-evaluate existing alerts if the indicator changes
        for track_id, alert in self.active_alerts.items():
            if turn_indicator == alert['zone'] and alert['level'] != "RED":
                alert['level'] = "RED"
                alerts.append({'track_id': track_id, 'zone': alert['zone'], 'level': 'RED', 'class_name': alert['class_name'], 're_evaluated': True})
        return alerts
