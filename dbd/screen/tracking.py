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
    #time.sleep(5)
    lines, screenshot_cv = detect_lines(PERCENTAGE)
    boxes = detect_white_box(screenshot_cv)

    if lines is not None and boxes is not None:
        line = None
        #print(f"Detected {len(lines)} lines.")
        merged_lines = merge_lines(lines, DISTANCE_THRESHOLD, ANGLE_THRESHOLD, LENGTH_THRESHOLD)
        for line in merged_lines:
            x1, y1, x2, y2 = line
            #print(line_points )
            #cv2.line(screenshot_cv, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        #print(f"Detected {len(boxes)} white boxes.") 
        # Draw bounding box around each detected box
        for box in boxes:
            x, y, w, h = box
            box_points = np.array([(x, y), (x, y+h), (x+w, y+h), (x+w, y)])
            #screenshot_cv = cv2.rectangle(screenshot_cv, (x, y), (x+w, y+h), (0,255,255), 2)  # BGR for Yellow is (0, 255, 255)
            
            if line is not None and overlap(line, box_points):
                #print("Overlap detected")
                #print("Overlap detected at " + str(time.time()))    
                press_space()
                #print("Pressed space at " + str(time.time()))
                #save a screenshot at the time of overlap
                #cv2.imwrite("screenshot_overlap.png", screenshot_cv)
                #pause for .3 second
                time.sleep(.2)
                break
            #else:
            #    break


        cv2.imwrite("screenshot.png", screenshot_cv)
        #print("Screenshot saved at time" + str(time.time()))
    #else:
        #print("No lines or white boxes detected")

    return screenshot_cv

def track_loop(stop_event):
    PERCENTAGE = 14
    
    #set time counter to current time
    start_time = time.time()

    while not stop_event.is_set():
        track_objects(PERCENTAGE)
        #print("time for iteration: " + str(time.time()))

        #exit after running for 1 minute
        if time.time() - start_time > 60:
            print("Exiting...")
            break