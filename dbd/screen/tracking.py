import time
import numpy as np
from screen.rectange_detect import detect_white_box
from screen.line_tracking import detect_lines, merge_lines
from screen.overlap import overlap
import ctypes


VK_SPACE = 0x20
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002

def press_space():
    ctypes.windll.user32.keybd_event(VK_SPACE, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(VK_SPACE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

def track_objects(PERCENTAGE, DISTANCE_THRESHOLD=10, ANGLE_THRESHOLD=np.pi/6, LENGTH_THRESHOLD=70):

    lines, screenshot_cv = detect_lines(PERCENTAGE)
    boxes = detect_white_box(screenshot_cv)

    if lines is not None and boxes is not None:
        line = None
        merged_lines = merge_lines(lines, DISTANCE_THRESHOLD, ANGLE_THRESHOLD, LENGTH_THRESHOLD)
        if merged_lines:  # Check if merged_lines is not empty
            line = merged_lines[-1]  # Assigns last line of merged_lines to line

    
        for box in boxes:
            x, y, w, h = box
            box_points = np.array([(x, y), (x, y+h), (x+w, y+h), (x+w, y)])

            if line is not None and overlap(line, box_points):
                press_space()
                time.sleep(.2) # Sleep for 200ms to prevent multiple key presses
                break
        
    return 

def track_loop(stop_event):
    PERCENTAGE = 16

    while not stop_event.is_set():
        track_objects(PERCENTAGE)


