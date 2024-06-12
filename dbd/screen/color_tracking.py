import cv2
import numpy as np
from PIL import ImageGrab
from screeninfo import get_monitors
import time

def capture_percentage_of_primary_screen(percentage):
    screen = ImageGrab.grab()
    full_screen_size = screen.size

    # Define the size of the box you want to capture as a percentage
    percentage = 50  # capture 50% of the screen

    box_size = (full_screen_size[0]*percentage/100, full_screen_size[1]*percentage/100)

    # Calculate the top left corner of the box to be captured
    top_left = ((full_screen_size[0] - box_size[0]) / 2, (full_screen_size[1] - box_size[1]) / 2)

    # Calculate the bottom right corner of the box to be captured
    bottom_right = (top_left[0] + box_size[0], top_left[1] + box_size[1])

    # Define the box to capture
    box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

    # Grab the center portion of the screen
    img = ImageGrab.grab(bbox=box)

    return img

def capture_screen():
    # Usage:
    PERCENTAGE = 50  # Change the percentage as per your need
    MIN_LINE_LENGTH = 20
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

        edges = cv2.Canny(blurred,50,150,apertureSize = 3)

        # Dilate the image
        dilated = cv2.dilate(edges, None, iterations=2)

        lines = cv2.HoughLinesP(dilated,1,np.pi/180,50, minLineLength=MIN_LINE_LENGTH, maxLineGap=MAX_LINE_GAP)


        if lines is not None:
            print(f"Detected {len(lines)} lines.") 
            for line in lines:
                for x1, y1, x2, y2 in line:
                    length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    if length >= 1:  # length filter
                        cv2.line(screenshot_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.imwrite("screenshot.png", screenshot_cv)
        else:
            print("No lines detected")
            
        print("Next Frame -------------------------")
        
        # Display screen capture
        cv2.imshow('Screen Capture', screenshot_cv)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break
   
        # Let's not burden the CPU too much
        time.sleep(3.0)  

capture_screen()