import cv2
import numpy as np
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


def detect_lines(PERCENTAGE, MIN_LINE_LENGTH=30, MAX_LINE_GAP=10):
    # capture screen
    screenshot =  capture_percentage_of_primary_screen(PERCENTAGE)
    
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    
    hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([169, 250, 100])
    upper_red = np.array([179, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([0, 250, 100])
    upper_red = np.array([9, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    mask = mask0 + mask1
    res = cv2.bitwise_and(screenshot_cv, screenshot_cv, mask=mask)
    
    blurred = cv2.GaussianBlur(res, (5, 5), 0)
    edges = cv2.Canny(blurred,100,125,apertureSize = 3)
    dilated = cv2.dilate(edges, None, iterations=1)
    
    lines = cv2.HoughLinesP(dilated,1,np.pi/180,50, minLineLength=MIN_LINE_LENGTH, maxLineGap=MAX_LINE_GAP)
    
    return lines, screenshot_cv