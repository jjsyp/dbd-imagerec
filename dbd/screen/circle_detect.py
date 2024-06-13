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
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=1)

    # Find contours in the mask 
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
  
    # Process each contour
    for contour in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(contour)
        if area > 1:
            # Find bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append([x, y, w, h])

    return boxes