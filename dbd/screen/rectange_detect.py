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

    # Apply a series of dilations and erosions to remove any small blobs of noise from the image
    erode_kernel = np.ones((3, 3), np.uint8)
    
    #cv2.imshow('Mask Before Erosion and Dilation', mask)
    #cv2.waitKey(0)

    mask = cv2.dilate(mask, None, iterations=1)
    mask = cv2.erode(mask, erode_kernel, iterations=2)

    #cv2.imshow('Mask After Erosion and Dilation', mask)
    #cv2.waitKey(0)

    # Find contours in the mask 
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
  
    # Process each contour
    for contour in contours:

        # Find bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)
        #print("Bounding box: ", x, y, w, h)
        #cv2.drawContours(screenshot_cv, [contour], -1, (0,255,0), 1)
        # Extract box content
        box_content = screenshot_cv[y:y+h, x:x+w]
        
        # Calculate its average color
        avg_color_per_row = np.average(box_content, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)  
    
        # If it's close enough to white (e.g., R, G, and B > 200 for a scale of 0 to 255)
        #if np.all(avg_color > 200):
            #print("Avg color: ", avg_color)
            #boxes.append([x, y, w, h])

        # Calculate area and remove small elements
        area = cv2.contourArea(contour)
        #print("Area: ", area)

        min_area_threshold = 25  # minimum threshold for area
        max_area_threshold = 100   # maximum threshold for area
    
        if min_area_threshold < area < max_area_threshold and np.all(avg_color > 50):
            # Find bounding box coordinates
            #print("Area 2: ", area)
            #print("Avg color: ", avg_color)
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append([x, y, w, h])

    return boxes