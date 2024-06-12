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

    # loop
    while True:
        # capture screen
        screenshot = capture_percentage_of_primary_screen(PERCENTAGE)
        screenshot_np = np.array(screenshot)

        # convert color space for cv2
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # convert color space to hsv (hue, saturation, value)
        hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)

        # range for RED color in HSV, might need to be adjusted

        # lower mask (169-179)
        lower_red = np.array([169, 250, 140])
        upper_red = np.array([179, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        # upper mask (0-9)
        lower_red = np.array([0, 250, 140])
        upper_red = np.array([9, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # join the masks
        mask = mask0 + mask1

        # Erode and dilate to remove small noise
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(screenshot_cv, screenshot_cv, mask=mask)

        # find contours in the mask and initialize the current
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            print('Found a contour')
            # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                print('Found a circle')
                # draw the circle and centroid on the frame,
                cv2.circle(screenshot_cv, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(screenshot_cv, center, 5, (0, 0, 255), -1)

                # Save the image with a way of marking where the contour was detected
                cv2.imwrite("screenshot.png", screenshot_cv)

        # if the `q` key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # Display screen capture
        cv2.imshow('Screen Capture', screenshot_cv)
        

        if cv2.waitKey(25) & 0xFF == ord('q'):
            print('Exiting...')
            cv2.destroyAllWindows()
            break
            
        # Let's not burden the CPU too much
        time.sleep(5.0)  # adjust accordingly or even 
        
capture_screen()