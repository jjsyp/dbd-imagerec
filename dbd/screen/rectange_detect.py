import cv2
import numpy as np

def detect_white_box(screenshot_cv):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)

    # Define range for white color
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 255, 255])

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(screenshot_cv, screenshot_cv, mask=mask)

    # Apply a series of dilations and erosions to remove any small blobs of noise from the image
    erode_kernel = np.ones((9, 9), np.uint8)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, erode_kernel, iterations=1)

    # Find contours in the mask 
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
  
    # Process each contour
    for contour in contours:

        # Find bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)

        # Extract box content
        box_content = screenshot_cv[y:y+h, x:x+w]

        # Calculate its average color
        avg_color_per_row = np.average(box_content, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)  
    
        # If it's close enough to white (e.g., R, G, and B > 200 for a scale of 0 to 255)
        if np.all(avg_color > 200):
            boxes.append([x, y, w, h])

        # Calculate area and remove small elements
        area = cv2.contourArea(contour)

        min_area_threshold = 50  # minimum threshold for area
        max_area_threshold = 600  # maximum thre shold for area
    
        if min_area_threshold < area < max_area_threshold:
            # Find bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append([x, y, w, h])

    return boxes