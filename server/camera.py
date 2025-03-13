CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CENTER_TOLERANCE = 10

def adjust_drone_position(bbox_center_x, bbox_center_y):
    """
    Adjusts the drone's position to keep the bounding box center aligned with the camera center.
    """
    offset_x = bbox_center_x - (CAMERA_WIDTH / 2)
    offset_y = bbox_center_y - (CAMERA_HEIGHT / 2)

    print(f"Bounding box offset: X={offset_x}, Y={offset_y}")

    roll_adjustment = pitch_adjustment = 0

    if abs(offset_x) > CENTER_TOLERANCE:
        roll_adjustment = -1 if offset_x < 0 else 1
        print(f"Adjusting roll: {roll_adjustment}")
        # Implement roll adjustment logic here

    if abs(offset_y) > CENTER_TOLERANCE:
        pitch_adjustment = -1 if offset_y < 0 else 1
        print(f"Adjusting pitch: {pitch_adjustment}")
        # Implement pitch adjustment logic here

    return roll_adjustment, pitch_adjustment