import cv2
import numpy as np
from PIL import ImageGrab
from screeninfo import get_monitors
import time
from screen.circle_detect import detect_white_box
from screen.screen_grab import capture_percentage_of_primary_screen


def merge_lines(lines, distance_threshold, angle_threshold, length_threshold):
    merged_lines = []

    # Convert 'lines' from a numpy array of arrays to a simple list of lines
    lines_list = [list(line[0]) for line in lines if np.linalg.norm([line[0][0] - line[0][2], line[0][1] - line[0][3]]) <= length_threshold]

    # Sort the lines
    lines_list.sort(key = lambda line: ((line[0] + line[2])/2, (line[1] + line[3])/2))
    
    # Same merging code as before but works on lines of length <= length_threshold
    for line in lines_list:
        if len(merged_lines) > 0:
            last_line = merged_lines[-1]
            distance = np.linalg.norm(np.subtract(((line[0] + line[2])/2, (line[1] + line[3])/2), ((last_line[0] + last_line[2])/2, (last_line[1] + last_line[3])/2)))
            angle = abs(np.arctan2(line[3] - line[1], line[2] - line[0]) - np.arctan2(last_line[3] - last_line[1], last_line[2] - last_line[0]))
            if angle > np.pi:
                angle = 2*np.pi - angle
            if distance < distance_threshold and angle < angle_threshold:
                merged_lines[-1] = [(last_line[0] + line[0]) / 2, (last_line[1] + line[1]) / 2, (last_line[2] + line[2]) / 2, (last_line[3] + line[3]) / 2]
            else:
                merged_lines.append(line)
        else:
            merged_lines.append(line)

    return merged_lines

def track_line():
    # Usage:
    PERCENTAGE = 20  # Change the percentage as per your need
    MIN_LINE_LENGTH = 30
    MAX_LINE_GAP = 10

    # loop
    while True:
        # capture screen
        screenshot = capture_percentage_of_primary_screen(PERCENTAGE)
        screenshot_np = np.array(screenshot)

        # convert color space for cv2
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # convert color space to hsv (hue, saturation, value)
        hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)

        # lower mask
        lower_red = np.array([169, 250, 100])
        upper_red = np.array([179, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        # upper mask
        lower_red = np.array([0, 250, 100])
        upper_red = np.array([9, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

                # join the masks
        mask = mask0 + mask1

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(screenshot_cv, screenshot_cv, mask=mask)
 
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(res, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blurred,100,125,apertureSize = 3)

        # Dilate the image
        dilated = cv2.dilate(edges, None, iterations=1)

        # Detect lines
        lines = cv2.HoughLinesP(dilated,1,np.pi/180,50, minLineLength=MIN_LINE_LENGTH, maxLineGap=MAX_LINE_GAP)

        # Merge lines
        DISTANCE_THRESHOLD = 10
        ANGLE_THRESHOLD = np.pi/6
        LENGTH_THRESHOLD = 70

        boxes = detect_white_box(screenshot_cv)

        if lines is not None and boxes is not None:
            print(f"Detected {len(lines)} lines.")
            print(f"Detected {len(boxes)} white boxes.") 
            merged_lines = merge_lines(lines, DISTANCE_THRESHOLD, ANGLE_THRESHOLD, LENGTH_THRESHOLD)
            for x1, y1, x2, y2 in merged_lines:
                cv2.line(screenshot_cv, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.imwrite("screenshot.png", screenshot_cv)

            # Draw bounding box around each detected box
            for box in boxes:
                x, y, w, h = box
                screenshot_cv = cv2.rectangle(screenshot_cv,(x,y),(x+w,y+h),(0,255,0),2) 


        else:
            print("No lines detected")
            print("No white boxes detected")
            
        print("Next Frame -------------------------")

        # Draw bounding box around each detected box
        for box in boxes:
            x, y, w, h = box
            screenshot_cv = cv2.rectangle(screenshot_cv,(x,y),(x+w,y+h),(0,255,0),2)       
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break
   
        # Let's not burden the CPU too much
        time.sleep(3.0)  
