from PIL import Image
from mss import mss

sct = mss()

# Function to get the size of the screen
def get_screen_size():
    monitor = sct.monitors[2]
    return monitor['width'], monitor['height']

# Initialize the screen size at the start of the program
full_screen_size = get_screen_size()

# Function to capture a percentage of the screen
def capture_percentage_of_primary_screen(percentage):
    percentage /= 100 

    box_width = full_screen_size[0]*percentage - 165
    box_height = full_screen_size[1]*percentage

    # Calculate the top left corner of the box to be captured. 
    top_left_x = ((full_screen_size[0] - box_width) / 2) 
    top_left_y = ((full_screen_size[1] - box_height) / 2) 

    # define the region to capture
    region = {'top': int(top_left_y)-15, 'left': int(top_left_x), 'width': int(box_width), 'height': int(box_height)}

    # Grab the portion of the screen defined by the box with mss
    with mss() as sct:
        img = sct.grab(region)

    # since mss return image in BGRA, we need to convert it to RGB
    img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
    return img