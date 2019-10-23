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
        self.counter = tk.IntVar()
        self.player_mark = tk.StringVar()
        self.message = tk.StringVar()
        self.relay_state = tk.StringVar()
        self.relay_button_text = tk.StringVar()
        self.geometry("800x480")
        self.configure(background=BB_BLUE)
        self.title(title)

        # Instance variables to be set up by configuration methods
        self.message_label = None
        self.goal_increase_label = None
        self.goal_decrease_label = None
        self.relay_label = None
        self.logo_canvas = None
        self.pixel = None
        self.logo_small = None
        self.logo_medium = None

        # Add BB logo to top left of GUI and as UI icon
        self.create_logos_and_icons()

        # Set up labels
        self.create_labels()

        # Set up buttons
        self.create_buttons()

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
        # Manage goal increments/decrements
        inc_by_one = tk.Button(self, text="+1", width=8, height=4, bg="gray", fg="green", padx=10, pady=10,
                               command=partial(self.display_message, "Trigger value increased."))
        inc_by_one.grid(column=0, row=2)

        inc_by_ten = tk.Button(self, text="+10", width=8, height=4, bg="gray", fg="green", padx=10, pady=10,
                               command=partial(self.display_message, "Trigger value increased."))
        inc_by_ten.grid(column=0, row=3)

        dec_by_one = tk.Button(self, text="-1", width=8, height=4, bg="gray", fg="red", padx=10, pady=10,
                               command=partial(self.display_message, "Trigger value decreased."))
        dec_by_one.grid(column=1, row=2)

        dec_by_ten = tk.Button(self, text="-10", width=8, height=4, bg="gray", fg="red", padx=10, pady=10,
                               command=partial(self.display_message, "Trigger value decreased."))
        dec_by_ten.grid(column=1, row=3)

        # Manage the relay duration, and on/off
        self.relay_state.set("Off")
        self.relay_button_text.set("Relay On")
        relay_on_off = tk.Button(self, textvariable=self.relay_button_text, width=8, height=4, bg="gray", fg="red",
                                 padx=10, pady=10, command=self.toggle_relay)
        relay_on_off.grid(column=3, row=2)

        relay_dur_inc = tk.Button(self, text="+10 sec", width=8, height=4, bg="gray", fg="green", padx=10, pady=10,
                                  command=partial(self.display_message, "Relay duration increased 10 seconds."))
        relay_dur_inc.grid(column=3, row=3)

        relay_dur_dec = tk.Button(self, text="-10 sec", width=8, height=4, bg="gray", fg="red", padx=10, pady=10,
                                  command=partial(self.display_message, "Relay duration decreased 10 seconds."))
        relay_dur_dec.grid(column=3, row=4)

    def create_labels(self):
        self.message_label = tk.Label(self, textvariable=self.message)
        self.message_label.grid(column=17, row=0, sticky="N", pady=10)
        self.message_label.configure(fg=BB_GOLD, bg=BB_BLUE)

        # Goal increment label
        self.goal_increase_label = tk.Label(self, text="Increase Goal")
        self.goal_increase_label.grid(column=0, row=1, sticky="N", pady=20)
        self.goal_increase_label.configure(bg=BB_BLUE, fg=BB_GOLD)

        # Goal decrement label
        self.goal_decrease_label = tk.Label(self, text="Decrease Goal")
        self.goal_decrease_label.grid(column=1, row=1, sticky="N", pady=20)
        self.goal_decrease_label.configure(bg=BB_BLUE, fg=BB_GOLD)

        # Manage relay label
        self.relay_label = tk.Label(self, text="Manage Relay")
        self.relay_label.grid(column=3, row=1, sticky="N", pady=20)
        self.relay_label.configure(bg=BB_BLUE, fg=BB_GOLD)


    def mark_and_update(self, button_id):
        if button_id not in self.clicked:
            self.current_player = int(not self.current_player)
            self.player_mark.set(self.player_marks[self.current_player])
            self.clicked.add(button_id)

    def display_message(self, msg):
        self.message.set(msg)

    def toggle_relay(self):
        current = self.relay_state.get()

        if current == "On":
            self.relay_state.set("Off")
            self.display_message("Relay {}".format(self.relay_state.get()))
            self.relay_button_text.set("Relay {}".format(current))

        elif current == "Off":
            self.relay_state.set("On")
            self.display_message("Relay {}".format(self.relay_state.get()))
            self.relay_button_text.set("Relay {}".format(current))


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
       This is the driver function of the GUI. This sets up the Root container instance.
       The second to last line is the method call that actually runs the GUI

    """

    # Sets up the root window
    root = Root()

    # This runs the gui so things actually show up
    root.mainloop()

if __name__ == "__main__":
    run()
