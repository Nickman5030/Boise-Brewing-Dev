import os
import tkinter as tk
from functools import partial

BB_BLUE = "#17286d"
BB_GOLD = "#f2d652"
APPLICATION_TITLE = "Door Sensor"


class Root(tk.Tk):
    """
       Inherits from the main Tk class of Tkinter. Does some basic configuration, such as setting up the grid,
       a counter variable, and the icon photo

    """
    player_marks = {
        1: "X",
        0: "O"
    }

    def __init__(self, *args, **kwargs):
        # Set up pre-creation variables
        title = kwargs.pop("title", APPLICATION_TITLE)
        self.current_player = 1
        self.clicked = set()

        # Initialize the class
        tk.Tk.__init__(self, *args, **kwargs)

        # Set up post-creation variables and class attributes
        self.configure_vars(title)

        # Add BB logo to top left of GUI and as UI icon
        self.create_logos_and_icons()

        # Set up labels
        self.create_labels()

        # Create a 3 x 3 grid in the root window
        self.create_grid()

    def create_logos_and_icons(self):
        # Open and store the images as attributes
        self.logo_small = tk.PhotoImage(file=os.path.join("images", "boise-brewing-small-logo.png"))
        self.logo_medium = tk.PhotoImage(file=os.path.join("images", "boise-brewing-medium-logo.png"))
        # This is to allow us to size the buttons on pixels
        self.pixel = tk.PhotoImage(width=1, height=1)

        # Assign the images to their respective places
        self.tk.call("wm", "iconphoto", self._w, self.logo_medium)
        self.logo_canvas = tk.Canvas(self)
        self.logo_canvas.configure(bg=BB_BLUE, width=175, height=58, bd=0, highlightthickness=0)
        self.logo_canvas.grid(column=0, row=0, sticky="NW")
        self.logo_canvas.create_image(87, 30, anchor="center", image=self.logo_small)

    def create_buttons(self):
        nw_button = tk.Button(self, text="Update", command=partial(self.display_message, "Updated!"), padx=0, pady=0,
                              image=self.pixel, compound="c", width=60, height=20)
        nw_button.grid(column=0, row=1, sticky="W")

    def create_labels(self):
        self.message_label = tk.Label(self, textvariable=self.message)
        self.message_label.grid(column=17, row=0, sticky="N", pady=10)
        self.message_label.configure(fg=BB_GOLD, bg=BB_BLUE)

    def create_grid(self):
        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1

    def configure_vars(self, title):
        self.counter = tk.IntVar()
        self.player_mark = tk.StringVar()
        self.message = tk.StringVar()
        self.geometry("800x480")
        self.configure(background=BB_BLUE)
        self.title(title)

    def mark_and_update(self, button_id):
        if button_id not in self.clicked:
            self.current_player = int(not self.current_player)
            self.player_mark.set(self.player_marks[self.current_player])
            self.clicked.add(button_id)

    def display_message(self, msg):
        self.message.set(msg)


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

    # Sets up the root window
    root = Root()




    # Add the buttons to the display

    # sw_button = tk.Button(root, text="Decrease", command=partial(dec_button_click, root.counter), padx=0, pady=0,
    #                       image=pixel, compound="c", width=(width // 4), height=(height // 4))
    # sw_button.grid(column=0, row=2)
    # se_button = tk.Button(root, text="Decrease", command=partial(dec_button_click, root.counter), padx=0, pady=0,
    #                       image=pixel, compound="c", width=(width // 4), height=(height // 4))
    # se_button.grid(column=2, row=2)
    # ne_button = tk.Button(root, textvariable=root.player_mark, command=partial(root.mark_and_update, "tr"), padx=0,
    #                       pady=0, image=pixel, compound="c", width=(width // 4), height=(height // 4),
    #                       foreground=BB_GOLD, background=BB_BLUE)
    # ne_button.grid(column=2, row=0)



    # label = tk.Label(root, textvariable=root.counter)
    # label.grid(column=1, row=1)

    # This runs the gui so things actually show up
    root.mainloop()


if __name__ == "__main__":
    run()
