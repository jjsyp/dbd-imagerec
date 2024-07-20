import cv2
import numpy as np
from PIL import ImageGrab
from screeninfo import get_monitors
import time


# Function to get the size of the screen
def get_screen_size():
    screen = ImageGrab.grab()
    return screen.size

# Initialize the screen size at the start of the program
full_screen_size = get_screen_size()

# Function to capture a percentage of the screen
def capture_percentage_of_primary_screen(percentage):
    vertical_adjustment = -40        
    horizontal_adjustment = 40

    box_size = (full_screen_size[0]*percentage/100 - 2*horizontal_adjustment, full_screen_size[1]*percentage/100 - 2*vertical_adjustment)

    # Calculate the top left corner of the box to be captured. 
    top_left = ((full_screen_size[0] - box_size[0]) / 2, (full_screen_size[1] - box_size[1]) / 2)

    # Calculate the bottom right corner of the box to be captured. 
    bottom_right = (top_left[0] + box_size[0], top_left[1] + box_size[1]-50)

    # Define the box to capture
    box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

    # Grab the portion of the screen defined by the box
    img = ImageGrab.grab(bbox=box)

    return img