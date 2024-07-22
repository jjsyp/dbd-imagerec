import cv2
import numpy as np
from PIL import ImageGrab, Image
from screeninfo import get_monitors
import time
from mss import mss

sct = mss()

# Function to get the size of the screen
def get_screen_size():
    monitor = sct.monitors[2]
    for monitor_number, monitor_info in enumerate(sct.monitors):
        print(f"Monitor {monitor_number}: {monitor_info}")
    return monitor['width'], monitor['height']

# Initialize the screen size at the start of the program
full_screen_size = get_screen_size()

# Function to capture a percentage of the screen
def capture_percentage_of_primary_screen(percentage):
    vertical_adjustment = -42        
    horizontal_adjustment = 40
    percentage /= 100

    box_width = full_screen_size[0]*percentage
    box_height = full_screen_size[1]*percentage

    # Calculate the top left corner of the box to be captured. 
    top_left_x = (full_screen_size[0] - box_width) / 2
    top_left_y = (full_screen_size[1] - box_height) / 2

    # Calculate the bottom right corner of the box to be captured. 
    bottom_right_x = top_left_x + box_width
    bottom_right_y = top_left_y + box_height
    bottom_right_y = top_left_y + box_height - 50

    # define the region to capture
    region = {'top': int(top_left_y), 'left': int(top_left_x), 'width': int(box_width), 'height': int(box_height)}

    # Grab the portion of the screen defined by the box with mss
    img = sct.grab(region)

    # since mss return image in BGRA, we need to convert it to RGB
    img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
    print("Captured screen at " + str(time.time()) + "in screen_grab.py")
    return img