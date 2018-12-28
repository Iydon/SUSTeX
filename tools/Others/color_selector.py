from PIL import ImageGrab, ImageTk
import pyautogui as pag
import tkinter as tk


class Event():
    """
    Event.
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class color_selector():
    """
    Color selector.
    """
    def __init__(self):
        # Initialize
        self.root           = tk.Tk()
        self.root.overrideredirect(True)
        self.screen         = ImageGrab.grab()
        self.image          = ImageTk.PhotoImage(image=self.screen)
        self.sw,self.sh     = self.screen.size # screen (weight|height).
        self.canvas         = tk.Canvas(self.root, width=self.sw, height=self.sh)
        self.last_x         = 0
        self.last_y         = 0
        self.selector       = self.canvas.create_oval((0,0,0,0))
        self.canvas.pack()
        # Daw the screen.
        self.canvas.create_image((self.sw/2, self.sh/2), image=self.image)
        self.canvas.bind("<ButtonPress>", self.handle_select)
        self.canvas.bind("<Motion>", self.reset_selector)
        x,y = self.get_mouse_coords()
        e   = Event(x, y)
        self.reset_selector(e)

    def handle_select(self, e):
        """
        Handle the action `select'.
        """
        print(r"\definecolor{color-name}{RGB}{%s,%s,%s}"%(self.selector_color_rgb))
        self.root.quit()

    def get_mouse_coords(self):
        """
        Get the coordinates of the mouse in real time.
        """
        return pag.position()

    def create_mouse_box(self, coords):
        """
        Create mouse box.
        """
        x,y = coords
        R = 32
        if x<self.sw/2:
            x1,x2 = x, x+2*R
        else:
            x1,x2 = x-2*R, x
        if y<self.sh/2:
            y1,y2 = y, y+2*R
        else:
            y1,y2 = y-2*R, y
        return (x1, y1, x2, y2)

    def get_select_color(self, coords):
        """
        Get the color selected.
        """
        return self.screen.getpixel(coords)

    def rgb2hex_str(self, rgb):
        """
        Convert RGB to hex string.
        """
        r,g,b = [hex(e)[2:] for e in rgb]
        return ("#%2s%2s%2s"%(r,g,b)).replace(" ","0")

    def reset_selector(self, e):
        """
        Reset the selector.
        """
        x,y = e.x, e.y
        if not (self.last_x==x and self.last_y==y):
            self.last_x = x
            self.last_y = y
            coords = (x, y)
            box    = self.create_mouse_box(coords)
            color  = self.get_select_color(coords)
            fill   = self.rgb2hex_str(color)
            self.selector_color_rgb = color
            self.canvas.delete(self.selector)
            self.selector = self.canvas.create_oval(box, fill=fill)


if __name__ == "__main__":
    app = color_selector()
    app.root.mainloop()
