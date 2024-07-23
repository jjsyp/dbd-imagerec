from screen.tracking import track_loop
import cProfile
import time

import tkinter as tk
from threading import Thread, Event

def run_program(stop_event):
    while not stop_event.is_set():
        #pr = cProfile.Profile()
        #pr.enable()
        track_loop()  
        #pr.disable()
        #pr.print_stats(sort='cumtime')
        time.sleep(0.001)  

stop_event = Event()
root = tk.Tk()
root.geometry('500x300')
root.title("<3 Alli")

status_label = tk.Label(root, text="Status: Not Running")
status_label.pack()

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

quit_button = tk.Button(root, text="Quit", command=quit_prog)
quit_button.pack()

root.mainloop()