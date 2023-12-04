import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors
import numpy as np
import cv2
import mss
from sys import exit
#from tscreenshot_in_rectangle import take_screenshot_in_rectangle as tsir
import screenshotCapture as sc
from datetime import datetime
def create_image_window(root,img_array,image_pos_size,monitor_pos_size):
    """
    Create a new window to display a screenshot.

    Parameters:
    root (Tk): The root Tk widget.
    img_array (numpy.ndarray): The screenshot as a numpy array.
    image_pos_size (list): The position and size of the image.
    monitor_pos_size (dict): The position and size of the monitor.

    Returns:
    None
    """
    # Create a Tk root widget
    window = tk.Toplevel()
    
    # Load the image
    img = Image.fromarray(img_array)
    # Create a PhotoImage object from the Image object
    imgtk= ImageTk.PhotoImage(img)
    sc.ScreenshotSelectionCanvas(root,window,imgtk,monitor_pos_size,image_pos_size,"single")
    window.geometry(f"{monitor_pos_size['width']}x{monitor_pos_size['height']}+{monitor_pos_size['left']}+{monitor_pos_size['top']}")
    # Make the window transparent
    window.overrideredirect(True)
# initialize the root window and the image position and size
def initialize_root():
    root = tk.Tk()
    root.withdraw()
    image_pos_size = [tk.IntVar(root,0) for _ in range(8)]
    return root, image_pos_size
# get the data of the monitor for mss
def get_monitor_data(monitor):
    return {
        "name": monitor.name,
        "top": monitor.y,
        "left": monitor.x,
        "width": monitor.width,
        "height": monitor.height,
    }
# capture the screenshot
def capture_screenshot(sct, monitor_data):
    sct_img = sct.grab(monitor_data)
    return cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGR2RGB)
# create the image window every monitor
def create_windows(root, sct):
    monitors = get_monitors()
    for monitor in monitors:
        monitor_data = get_monitor_data(monitor)
        img_array = capture_screenshot(sct, monitor_data)
        create_image_window(root, img_array, image_pos_size, monitor_data)
# get the coordinates of the screenshot of designated region
def get_coordinates(image_pos_size):
    a = min(image_pos_size[0].get(), image_pos_size[2].get())
    b = min(image_pos_size[1].get(), image_pos_size[3].get())
    c = max(image_pos_size[0].get(), image_pos_size[2].get())
    d = max(image_pos_size[1].get(), image_pos_size[3].get())
    e = image_pos_size[4].get()
    f = image_pos_size[5].get()
    return {"top": b-abs(f), "left": a-abs(e), "width": c-a, "height": d-b}
# save the screenshot
def save_screenshot(sct, range):
    img = Image.fromarray(cv2.cvtColor(np.array(sct.grab(range)), cv2.COLOR_BGR2RGB))
    now = datetime.now()
    img.save(f"{now.hour}--{now.minute}--{now.second}_{now.day}_{now.month}_{now.year}-screenshot.png")

if __name__ == '__main__':
    root, image_pos_size = initialize_root()
    with mss.mss() as sct:
        create_windows(root, sct)
    root.mainloop()
    range = get_coordinates(image_pos_size)
    with mss.mss() as sct:
        save_screenshot(sct, range)

