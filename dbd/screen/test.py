import cv2
import numpy as np
from PIL import ImageGrab
from screeninfo import get_monitors
import time

def capture_percentage_of_primary_screen(percentage):
    monitor = get_monitors()[0]  # Choose the primary monitor

    # Calculate the box size as a percentage of the monitor size
    box_size = (monitor.width * percentage / 100, monitor.height * percentage / 100)

    # Calculate the top left corner of the box to be captured
    top_left = ((monitor.width - box_size[0]) / 2, (monitor.height - box_size[1]) / 2)

    # Define the box to capture
    box = (top_left[0] + monitor.x, 
           top_left[1] + monitor.y, 
           top_left[0] + box_size[0] + monitor.x, 
           top_left[1] + box_size[1] + monitor.y)
    
    # Grab the specified portion of the screen
    img = ImageGrab.grab(bbox=box)

    return img

def capture_screen():
    # Usage:
    PERCENTAGE = 50  # Change the percentage as per your need

    # loop
    while True:
        # capture screen
        screenshot = capture_percentage_of_primary_screen(PERCENTAGE)
        screenshot_np = np.array(screenshot)

        # convert color space for cv2
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # Here NOW you can process screenshot_cv with OpenCV.
        # detect the circle/colored section/needle
        # decide to trigger the action

        # Display screen capture
        cv2.imshow('Screen Capture', screenshot_cv)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            print('Exiting...')
        
            cv2.destroyAllWindows()
            break

        # Let's not burden the CPU too much
        time.sleep(5.0)  # adjust accordingly or even 
        
capture_screen()