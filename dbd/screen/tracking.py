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

def press_space():
    ctypes.windll.user32.keybd_event(VK_SPACE, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(VK_SPACE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

def track_objects(PERCENTAGE, DISTANCE_THRESHOLD=10, ANGLE_THRESHOLD=np.pi/6, LENGTH_THRESHOLD=70):
    
    lines, screenshot_cv = detect_lines(PERCENTAGE)
    boxes = detect_white_box(screenshot_cv)

    if lines is not None and boxes is not None:
        line = None
        merged_lines = merge_lines(lines, DISTANCE_THRESHOLD, ANGLE_THRESHOLD, LENGTH_THRESHOLD)
        for line in merged_lines:
            x1, y1, x2, y2 = line

        #print(f"Detected {len(boxes)} white boxes.") 
        # Draw bounding box around each detected box
        for box in boxes:
            x, y, w, h = box
            box_points = np.array([(x, y), (x, y+h), (x+w, y+h), (x+w, y)])
            
            if line is not None and overlap(line, box_points):
                press_space()
                #pause for .3 second
                time.sleep(.3)
                break
            else:
                break


        cv2.imwrite("screenshot.png", screenshot_cv)

    return screenshot_cv

def track_loop():
    PERCENTAGE = 14
    
    while True:
        track_objects(PERCENTAGE)

        if 0xFF == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break