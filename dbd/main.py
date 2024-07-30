import cProfile
from screen.tracking import track_loop
import time
from screen.screen_grab import get_screen_size

import tkinter as tk
from threading import Thread, Event


def run_program(stop_event):
    while not stop_event.is_set():
        
        # pr = cProfile.Profile()
        # pr.enable()
        track_loop(stop_event)
        # pr.disable()
        # pr.print_stats(sort='cumtime')  
        time.sleep(0.001)  

stop_event = Event()
root = tk.Tk()
root.geometry('500x300')
root.title("Dead by Daylight Skill Check Bot")

status_label = tk.Label(root, text="Status: Not Running")
status_label.pack()
monitor_label = tk.Label(root, text="")
monitor_label.pack()

def check_monitor():
    monitor_width, monitor_height = get_screen_size()
    monitor_details = f"Monitor details: Width = {monitor_width}, Height = {monitor_height}"
    monitor_label.config(text=monitor_details)
    root.update()
    

def update_status(status):
    status_text = "Status: Running" if status else "Status: Not Running"
    status_label.config(text=status_text)
    root.update()

def start():
    global thread
    # Clear the stop event
    stop_event.clear()
    # Define and start the thread, set it as a daemon.
    thread = Thread(target=run_program, args=(stop_event,))
    thread.daemon = True
    thread.start()
    update_status(True)

def stop():
    # Set the stop event
    stop_event.set()
    update_status(False)

def quit_prog():
    stop()
    root.quit()

start_button = tk.Button(root, text="Start", command=start)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack()

check_monitor_button = tk.Button(root, text="Check Monitor", command=check_monitor)
check_monitor_button.pack()

quit_button = tk.Button(root, text="Quit", command=quit_prog)
quit_button.pack()

root.mainloop()