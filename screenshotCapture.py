import tkinter as tk  # import tkinter library
import sys,traceback
from PIL import Image,ImageTk
#ブランチテスト
#ドラッグした長方形を網掛けにして、Button リリースしたらポジションをプロパティにセットする。
class ScreenshotSelectionCanvas():
    def __init__(self,root,window,imgtk,monitor_pos_size,image_pos_size,type) -> None:
        # The root Tk widget, used to destroy the root window
        self.root = root

        # The canvas where the screenshot and selection rectangle are displayed
        self.canvas = tk.Canvas(window,width=monitor_pos_size['width'],height=monitor_pos_size['height'])

        # The position and size of the image, stored as tkinter.IntVar() objects
        self.image_pos_size = image_pos_size

        # The position where the mouse button was pressed
        self.pressed_x,self.pressed_y=0,0

        # The position where the mouse button was released
        self.released_x,self.released_y=0,0

        # The current mouse position
        self.x,self.y =0,0

        # The position of the monitor
        self.monitor_x,self.monitor_y=monitor_pos_size['left'],monitor_pos_size['top']  

        # The Tkinter.PhotoImage object to be displayed on the canvas
        self.canvas.image = imgtk
        self.canvas.create_image(0,0,image=imgtk,anchor="nw")

        # kill the window when double clicked
        self.canvas.bind("<Double-Button-1>", lambda e: self.root.destroy())

        # Bind the mouse button press event to the buttonpress method
        self.canvas.bind("<ButtonPress>", self.buttonpress)

        # Bind the mouse button release event to the appropriate method based on the type
        if type=="single":
            self.canvas.bind("<ButtonRelease>", self.release_stop)
        else:
            self.canvas.bind("<ButtonRelease>", self.release_continue)

        # Bind the mouse motion event to the dragging method
        self.canvas.bind("<B1-Motion>",self.dragging)

        # Display the canvas
        self.canvas.pack(expand=True)

        # Create a rectangle on the canvas, initially with size 0x0
        self.rectangle = self.canvas.create_rectangle(0,0,0,0,fill='red')

        # A flag to indicate whether the mouse button is pressed
        self.isclicked=False
    def render(self,x1,y1,x2,y2):
        self.rectangle =self.canvas.create_rectangle(x1,y1,x2,y2,fill="blue", stipple="gray25")
        self.canvas.grid(row=1,column=0)
        return self.rectangle
    def dragging(self,event):
        if self.isclicked is True:#Falseなら選ばない
            self.canvas.delete(self.rectangle)
            self.rectangle =self.render(self.pressed_x,self.pressed_y,event.x,event.y)

    def buttonpress(self,event):
        if not self.isclicked:
            self.pressed_x,self.pressed_y=event.x,event.y
            self.rectangle = self.render(self.pressed_x,self.pressed_y,event.x,event.y)
            self.isclicked=True
        else:
            self.canvas.delete(self.rectangle)
            self.isclicked=False
    def release_stop(self,event):
        self.canvas.delete(self.rectangle)
        self.isclicked=False
        self.image_pos_size[0].set(self.pressed_x)
        self.image_pos_size[1].set(self.pressed_y)
        self.image_pos_size[2].set(event.x)
        self.image_pos_size[3].set(event.y)
        self.image_pos_size[4].set(self.monitor_x)
        self.image_pos_size[5].set(self.monitor_y)
        print(self.image_pos_size[4].get(),self.image_pos_size[5].get(),self.image_pos_size[2].get(),self.image_pos_size[3].get())
        self.canvas.delete("all")
        self.root.destroy()

def main():
    try:
        root = tk.Tk()
        root.minsize(width=250, height=150)
        ScreenshotSelectionCanvas(root)

        root.mainloop()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()