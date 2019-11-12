"""
    This is a scripted version of the Boise Brewing GUI, as an OO approach ended up with a God class.


:author: Garrett Allen
"""

import os
import tkinter as tk
from functools import partial

BB_BLUE = "#17286d"
BB_GOLD = "#f2d652"
APPLICATION_TITLE = "Door Sensor"
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 800


# Globals for use by sensor program
class SensorData(object):
    def __init__(self):
        self.goal = 0
        self.relay_state = 1  # 1 = On, 0 = Off
        self.sensor_state = 1 # 1 = On, 0 = Off
        self.reset = 0  # 1 = Trigger Reset, 0 = No reset
        self.relay_duration = 10  # seconds

    def all(self):
        """
            Returns a dictionary of all the current data points

        :return: Dict
        """
        return self.__dict__

    def get_goal(self):
        """
        :return: Current value of goal
        """
        return self.goal

    def set_goal(self, val):
        """
            Updates the value in goal

        :param val: Value to be assigned to goal
        :return: None
        """
        self.goal = val

    def get_sensor_state(self):
        return self.sensor_state

    def toggle_sensor_state(self):
        """
            Sets the on/off state of the sensors

            1 - ON
            0 - OFF

        :return: None
        """
        self.sensor_state = int(not self.sensor_state)

    def get_relay_state(self):
        return self.relay_state

    def toggle_relay_state(self):
        """
            Sets the on/off state of the sensors

            1 - ON
            0 - OFF

        :return: None
        """
        self.relay_state = int(not self.relay_state)

    def get_reset(self):
        """
        :return: Current value of the reset attribute
        """
        return self.reset

    def toggle_reset(self):
        """
            Toggles value of reset

            1 - Trigger a reset
            0 - Continue normal operation

        :return: None
        """
        self.reset = int(not self.reset)

    def get_relay_duration(self):
        """
        :return: Current value of the relay duration setting
        """
        return self.relay_duration

    def set_relay_duration(self, seconds):
        """
            Sets the value of relation to the provided number of seconds

        :param seconds: New duration to be set
        :return: None
        """
        self.relay_duration = seconds


# Static object that can be interacted with by the sensor program
sensor_data = SensorData()
        

if __name__ == "__main__":
    # Functions to be used by the GUI
    def set_text(var, msg):
        """
            Can be used to set the text of any StringVar variable

        :param var: A StringVar object
        :param msg: The message you want the var set to
        :return: None
        """
        var.set(msg)


    def toggle_on_off(btn_var, msg_var, toggle_type):
        """
            Sets the message displayed on the button to opposite of current state. Sets user feedback message to provided
            text

        :param btn_var: Variable that is used to display the text on the button itself
        :param msg_var: Variable that controls messages displayed at top of GUI
        :param toggle_type: Specifies which button is being toggled to display proper messages
        :return: None
        """
        msg = ""
        if toggle_type == "relay":
            msg = "Relay"
        elif toggle_type == "sensor":
            msg = "Sensor"

        current_btn_text = btn_var.get()
        if current_btn_text == "Off":
            btn_var.set("On")
            msg_var.set("{} Off".format(msg))
        else:
            btn_var.set("Off")
            msg_var.set("{} On".format(msg))


    # Data variables for use by GUI
    logo_canvas_width = 175
    logo_canvas_height = 58

    # Set up root
    root = tk.Tk()
    root.title(APPLICATION_TITLE)
    root.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
    root.configure(background=BB_BLUE)

    # Set up the program icon and other images
    logo_small = tk.PhotoImage(file=os.path.join("images", "boise-brewing-small-logo.png"))
    logo_medium = tk.PhotoImage(file=os.path.join("images", "boise-brewing-medium-logo.png"))
    root.tk.call("wm", "iconphoto", root._w, logo_medium)

    # Set up text variables that require root existing first
    message = tk.StringVar()
    relay_toggle_text = tk.StringVar()
    relay_toggle_text.set("Off")
    sensor_toggle_text = tk.StringVar()
    sensor_toggle_text.set("On")

    # Create main containers
    logo_frame_top = tk.Frame(root, bg=BB_BLUE, width=800, height=60, pady=5)
    button_frame = tk.Frame(root, bg=BB_BLUE, width=800, height=400, padx=5, pady=5)

    # Set layout of main containers
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    logo_frame_top.grid(row=0)
    button_frame.grid(row=1)

    # Widgets for the Logo Frame
    logo_canvas = tk.Canvas(logo_frame_top, bg=BB_BLUE, width=logo_canvas_width, height=logo_canvas_height, bd = 0,
                            highlightthickness = 0)
    logo_canvas.create_image(logo_canvas_width / 2, logo_canvas_height / 2, anchor="center",
                             image=logo_small)
    message_label = tk.Label(logo_frame_top, textvariable=message, bg=BB_BLUE, fg=BB_GOLD, font="Times 16 bold")

    # Set layout of the widgets in the Logo Frame
    logo_canvas.grid()
    logo_canvas.grid_rowconfigure(0, weight=1)
    logo_canvas.grid_columnconfigure(0, weight=1)
    message_label.grid()
    logo_canvas.grid_rowconfigure(1, weight=1)

    # Create Frames for button widgets
    btn_col_0_frame = tk.Frame(button_frame, bg=BB_BLUE, width=140, height=350, padx=10)
    btn_col_1_frame = tk.Frame(button_frame, bg=BB_BLUE, width=140, height=350, padx=10)
    btn_col_2_frame = tk.Frame(button_frame, bg=BB_BLUE, width=140, height=350, padx=10)
    btn_col_3_frame = tk.Frame(button_frame, bg=BB_BLUE, width=140, height=350, padx=10)
    btn_col_4_frame = tk.Frame(button_frame, bg=BB_BLUE, width=140, height=350, padx=10)

    # Layout for button frame widgets
    btn_col_0_frame.grid(row=0, column=0, sticky="ns")
    btn_col_1_frame.grid(row=0, column=1, sticky="ns")
    btn_col_2_frame.grid(row=0, column=2, sticky="nsew")
    btn_col_3_frame.grid(row=0, column=3, sticky="ns")
    btn_col_4_frame.grid(row=0, column=4, sticky="ns")

    # Create the buttons and the column labels
    col0_label = tk.Label(btn_col_0_frame, text="Increase Goal", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    goal_inc_1_btn = tk.Button(btn_col_0_frame, text="+1", width=8, height=4, bg="gray", fg="black", padx=10, pady=10,
                               command=partial(set_text, message, "Trigger value increased."))
    goal_inc_10_btn = tk.Button(btn_col_0_frame, text="+10", width=8, height=4, bg="gray", fg="black", padx=10, pady=10,
                                command=partial(set_text, message, "Trigger value increased."))

    col1_label = tk.Label(btn_col_1_frame, text="Decrease Goal", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    goal_dec_1_btn = tk.Button(btn_col_1_frame, text="-1", width=8, height=4, bg="gray", fg="black", padx=10, pady=10,
                               command=partial(set_text, message, "Trigger value decreased."))
    goal_dec_10_btn = tk.Button(btn_col_1_frame, text="-10", width=8, height=4, bg="gray", fg="black", padx=10, pady=10,
                                command=partial(set_text, message, "Trigger value decreased."))

    col2_label = tk.Label(btn_col_2_frame, text="Goal Reset/Skip", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    goal_reset_btn = tk.Button(btn_col_2_frame, text="Reset", width=8, height=4, bg="gray", fg="black", padx=10,
                               pady=10, command=partial(set_text, message, "Trigger value reset."))
    goal_skip_btn = tk.Button(btn_col_2_frame, text="Skip", width=8, height=4, bg="gray", fg="black", padx=10,
                              pady=10, command=partial(set_text, message, "Trigger skipped"))

    col3_label = tk.Label(btn_col_3_frame, text="Manage Relay", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    relay_toggle_btn = tk.Button(btn_col_3_frame, textvariable=relay_toggle_text, width=8, height=4, bg="gray",
                                 fg="black", padx=10, pady=10,
                                 command=partial(toggle_on_off, relay_toggle_text, message, "relay"))
    relay_inc_dur_btn = tk.Button(btn_col_3_frame, text="Longer", width=8, height=4, bg="gray",
                                  fg="black", padx=10, pady=10,
                                  command=partial(set_text, message, "Relay Duration Increased."))
    relay_dec_dur_btn = tk.Button(btn_col_3_frame, text="Shorter", width=8, height=4, bg="gray",
                                  fg="black", padx=10, pady=10,
                                  command=partial(set_text, message, "Relay Duration Decreased."))

    col4_label = tk.Label(btn_col_4_frame, text="Sensors On/Off", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    sensor_toggle_btn = tk.Button(btn_col_4_frame, textvariable=sensor_toggle_text, width=8, height=4, bg="gray",
                                  fg="black", padx=10, pady=10,
                                  command=partial(toggle_on_off, sensor_toggle_text, message, "sensor"))

    # Layout for buttons and labels
    col0_label.grid(row=1)
    goal_inc_1_btn.grid(row=2)
    goal_inc_10_btn.grid(row=3)

    col1_label.grid(row=1)
    goal_dec_1_btn.grid(row=2)
    goal_dec_10_btn.grid(row=3)

    col2_label.grid(row=1)
    goal_reset_btn.grid(row=2)
    goal_skip_btn.grid(row=3)

    col3_label.grid(row=1)
    relay_toggle_btn.grid(row=2)
    relay_inc_dur_btn.grid(row=3)
    relay_dec_dur_btn.grid(row=4)

    col4_label.grid(row=1)
    sensor_toggle_btn.grid(row=2)

    root.mainloop()
