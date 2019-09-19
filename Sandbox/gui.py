import os
import tkinter as tk
from functools import partial


class Root(tk.Tk):
    """
       Inherits from the main Tk class of Tkinter. Does some basic configuration, such as setting up the grid,
       a counter variable, and the icon photo

    """

    def __init__(self, *args, **kwargs):
        # Configure the root application
        title = kwargs.pop("title")
        self.width = kwargs.pop("width")
        self.height = kwargs.pop("height")
        geometry = f"{self.width}x{self.height}"
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(geometry)
        self.title(title)
        self.tk.call("wm", "iconphoto", self._w,
                     tk.PhotoImage(file=os.path.join("images", "boise-brewing-medium-logo.png")))
        self.counter = tk.IntVar()
        # Create a 3 x 3 grid in the root window
        rows = 0
        while rows < 3:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1


def inc_button_click(counter):
    """
       Simple method used to increment a counter to show the buttons work
    """
    counter.set(counter.get() + 1)


def dec_button_click(counter):
    """
       Simple method used to decrement a counter to show the buttons work
    """
    counter.set(counter.get() - 1)


def run():
    """
       This is the driver function of the GUI. This sets up the Root container instance and assigns
       buttons to it. The very last line is the method call that actually runs the GUI

    """
    width = 800
    height = 480

    # Sets up the root window
    root = Root(title="Boise Brewing Door Sensor", width=width, height=height)

    # This is to allow us to size the buttons on pixels
    pixel = tk.PhotoImage(width=1, height=1)

    # Add the buttons to the display
    nw_button = tk.Button(root, text="Increase", command=partial(inc_button_click, root.counter), padx=0, pady=0,
                          image=pixel, compound="c", width=(width // 4), height=(height // 4))
    nw_button.grid(column=0, row=0)
    sw_button = tk.Button(root, text="Decrease", command=partial(dec_button_click, root.counter), padx=0, pady=0,
                          image=pixel, compound="c", width=(width // 4), height=(height // 4))
    sw_button.grid(column=0, row=2)
    se_button = tk.Button(root, text="Decrease", command=partial(dec_button_click, root.counter), padx=0, pady=0,
                          image=pixel, compound="c", width=(width // 4), height=(height // 4))
    se_button.grid(column=2, row=2)
    ne_button = tk.Button(root, text="Increase", command=partial(inc_button_click, root.counter), padx=0, pady=0,
                          image=pixel, compound="c", width=(width // 4), height=(height // 4))
    ne_button.grid(column=2, row=0)

    label = tk.Label(root, textvariable=root.counter)
    label.grid(column=1, row=1)

    # This runs the gui so things actually show up
    root.mainloop()


if __name__ == "__main__":
    run()
