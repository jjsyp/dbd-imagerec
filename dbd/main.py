from screen.tracking import track_loop
import cProfile
import time

import tkinter as tk
from threading import Thread, Event

def run_program(stop_event):
    while not stop_event.is_set():
        track_loop()  
        time.sleep(0.001)  

stop_event = Event()

def start():
    global thread
    # Clear the stop event
    stop_event.clear()
    # Define and start the thread, set it as a daemon.
    thread = Thread(target=run_program, args=(stop_event,))
    thread.daemon = True
    thread.start()

def stop():
    # Set the stop event
    stop_event.set()

def quit_prog():
    stop()
    root.quit()

root = tk.Tk()

start_button = tk.Button(root, text="Start", command=start)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack()

quit_button = tk.Button(root, text="Quit", command=quit_prog)
quit_button.pack()

root.mainloop()