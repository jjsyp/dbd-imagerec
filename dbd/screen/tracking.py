import time
import cv2
import numpy as np
from screen.rectange_detect import detect_white_box
from screen.line_tracking import detect_lines, merge_lines


def track_objects(PERCENTAGE, DISTANCE_THRESHOLD=10, ANGLE_THRESHOLD=np.pi/6, LENGTH_THRESHOLD=70):
    lines, screenshot_cv = detect_lines(PERCENTAGE)
    boxes = detect_white_box(screenshot_cv)

    if lines is not None and boxes is not None:
        print(f"Detected {len(lines)} lines.")
        merged_lines = merge_lines(lines, DISTANCE_THRESHOLD, ANGLE_THRESHOLD, LENGTH_THRESHOLD)
        for x1, y1, x2, y2 in merged_lines:
            cv2.line(screenshot_cv, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        print(f"Detected {len(boxes)} white boxes.") 
        # Draw bounding box around each detected box
        for box in boxes:
            x, y, w, h = box
            screenshot_cv = cv2.rectangle(screenshot_cv, (x, y), (x+w, y+h), (0,255,255), 2)  # BGR for Yellow is (0, 255, 255)

        cv2.imwrite("screenshot.png", screenshot_cv)
    else:
        print("No lines or white boxes detected")

    return screenshot_cv

def track_loop():
    PERCENTAGE = 20 

    while True:
        track_objects(PERCENTAGE)

        print('Next Frame -------------------------')

        if cv2.waitKey(25) & 0xFF == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break

        time.sleep(0.5)