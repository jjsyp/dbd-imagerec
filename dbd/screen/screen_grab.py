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
    vertical_adjustment = -42        
    horizontal_adjustment = 40
    percentage /= 100

    box_width = full_screen_size[0]*percentage - 2*horizontal_adjustment
    box_height = full_screen_size[1]*percentage - 2*vertical_adjustment

    # Calculate the top left corner of the box to be captured. 
    top_left_x = (full_screen_size[0] - box_width) / 2
    top_left_y = (full_screen_size[1] - box_height) / 2

    # Calculate the bottom right corner of the box to be captured. 
    bottom_right_x = top_left_x + box_width
    bottom_right_y = top_left_y + box_height - 50

    # Grab the portion of the screen defined by the box
    img = ImageGrab.grab(bbox=(top_left_x, top_left_y, bottom_right_x, bottom_right_y))

    return img