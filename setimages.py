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

if __name__ == '__main__':
    # Paths to the images you want to display
    root = tk.Tk()
    x_pos,y_pos = [],[]
    root.withdraw()
    image_pos_size = [tk.IntVar(root,0),tk.IntVar(root,0),tk.IntVar(root,0),tk.IntVar(root,0),tk.IntVar(root,0),tk.IntVar(root,0),tk.IntVar(root,0),tk.IntVar(root,0)]
    with mss.mss() as sct:
        # The screen part to capture
        monitors = get_monitors()
        for i, monitor in enumerate(monitors):
            print(f"Monitor {i + 1}:")
            print(f"Width: {monitor.width}, Height: {monitor.height}")
            print(f"X: {monitor.x}, Y: {monitor.y}")
            # Get the data of the monitor for mss
            monitor_pos_size = {
                "name":monitor.name,
                "top": monitor.y,
                "left": monitor.x,
                "width": monitor.width,
                "height": monitor.height,
            }
            # Grab the data
            sct_img = sct.grab(monitor_pos_size)
            # np.array(sct_img) returns an array of RGB values
            # Convert this array into a cv2 image of BGR values
            img_array = cv2.cvtColor(np.array(sct.grab(monitor_pos_size)),cv2.COLOR_BGR2RGB) # BGR Image
            create_image_window(root,img_array,image_pos_size,monitor_pos_size)
    
    # Start the Tk event loop
    root.mainloop()
    # get the smaller x and y coordinates of start and end points
    a = min(image_pos_size[0].get(),image_pos_size[2].get())
    b = min(image_pos_size[1].get(),image_pos_size[3].get())
    c = max(image_pos_size[0].get(),image_pos_size[2].get())
    d = max(image_pos_size[1].get(),image_pos_size[3].get())
    e = image_pos_size[4].get()
    f = image_pos_size[5].get()
    sct = mss.mss()
    range= {"top": b-abs(f), "left": a-abs(e), "width": c-a, "height": d-b}
    # Take a screenshot of the region
    # np.array(sct_img) returns an array of RGB values
    # Convert this array into a cv2 image of BGR values
    img= Image.fromarray(cv2.cvtColor(np.array(sct.grab(range)),cv2.COLOR_BGR2RGB))
    # Save the screenshot
    now = datetime.now()
    img.save(f"{now.hour}:{now.minute}:{now.second}_{now.day}_{now.month}_{now.year}-screenshot.png")
    
