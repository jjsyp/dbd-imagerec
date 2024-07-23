from screen.tracking import track_loop
import cProfile
import time

import tkinter as tk
from threading import Thread

running = False

def run_program():
    try: 
        while running:
            track_loop()  # Add your necessary arguments
            time.sleep(0.0001)  # Or whatever interval you want
    except KeyboardInterrupt:
        stop()  # Or any other cleanup code you need

def start():
    global running
    running = True
    thread = Thread(target=run_program)
    thread.start()
    

def stop():
    global running
    running = False

root = tk.Tk()

start_button = tk.Button(root, text="Start", command=start)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack()

root.mainloop()