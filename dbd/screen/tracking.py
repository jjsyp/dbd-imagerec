import time
import cv2
import numpy as np
from screen.rectange_detect import detect_white_box
from screen.line_tracking import detect_lines, merge_lines
from screen.overlap import overlap
import pyautogui
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
import ctypes

VK_SPACE = 0x20
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002

class SkillCheckTracker:
    def __init__(self):
        self.last_overlap_time = 0

    def press_space(self):
        ctypes.windll.user32.keybd_event(VK_SPACE, 0, KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(VK_SPACE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

# Create global tracker instance
tracker = SkillCheckTracker()

def track_objects(PERCENTAGE, DISTANCE_THRESHOLD=10, ANGLE_THRESHOLD=np.pi/6, LENGTH_THRESHOLD=70):
    lines, screenshot_cv = detect_lines(PERCENTAGE)
    boxes = detect_white_box(screenshot_cv)

    if lines is not None and boxes is not None:
        line = None
        merged_lines = merge_lines(lines, DISTANCE_THRESHOLD, ANGLE_THRESHOLD, LENGTH_THRESHOLD)
        if merged_lines:
            line = merged_lines[-1]

        for box in boxes:
            x, y, w, h = box
            box_points = np.array([(x, y), (x, y+h), (x+w, y+h), (x+w, y)])
            
            if line is not None and overlap(line, box_points):
                tracker.press_space()
                tracker.last_overlap_time = time.time()
                break
            #else:
            #    break


        #cv2.imwrite("screenshot.png", screenshot_cv)
        #print("Screenshot saved at time" + str(time.time()))
    #else:
        #print("No lines or white boxes detected")

    return 

def track_loop(stop_event):
    PERCENTAGE = 13.5
    min_interval = 0.0005  # 0.5ms minimum interval
    
    while not stop_event.is_set():
        current_time = time.time()
        
        # Only process if enough time has passed since last overlap
        if current_time - tracker.last_overlap_time >= 0.05:  # Reduced cooldown to 50ms
            track_objects(PERCENTAGE)
        
        # Very small sleep to prevent CPU overload while maintaining responsiveness
        time.sleep(min_interval)