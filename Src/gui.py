"""
    This is the GUI program for Boise Brewing's Beer Reward sensors

:author: Garrett Allen
"""
from combo_sensor import GPIO
import interface
import os
import tkinter as tk
from subprocess import check_output
from signal import SIGKILL
from functools import partial


APPLICATION_TITLE = "Door Sensor"
BB_BLUE = "#17286d"
BB_GOLD = "#f2d652"
WINDOW_HEIGHT = 480
WINDOW_WIDTH = 800


# Private functions to be used by the GUI
def __set_text(var, msg):
    """
        Can be used to set the text of any StringVar variable

    :param var: A StringVar object
    :param msg: The message you want the var set to
    :return: None
    """
    var.set(msg)


def __toggle_on_off(btn_var, msg_var, toggle_type):
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


def __set_message_and_goal(label, msg, val, stats):
    """
        Assigns msg to label and then updates the SensorData goal field to val

    :param label: Tkinter Label instance whose value we want changed
    :param msg: Message to assign to label
    :param val: Value to change goal by
    :return: None
    """
    __set_text(label, msg)

    current_goal = interface.get_goal()
    goal_val = current_goal + val
    if goal_val < 0:
        goal_val = 0
    interface.set_goal(goal_val)
    __configure_and_set_stats_text(stats)


def __toggle_sensor(btn_label, msg_label):
    """
        Sets the on/off state of the sensors

        1 - ON
        0 - OFF

    :param btn_label: Button label to toggle
    :param msg_label: Message label at top of screen to show that something happened
    :return: None
    """
    interface.toggle_sensor_state()
    __toggle_on_off(btn_label, msg_label, "sensor")


def __toggle_relay(btn_label, msg_label):
    """
        Sets the on/off state of the sensors

        1 - ON
        0 - OFF

    :param btn_label: Button label to toggle
    :param msg_label: Message label at top of screen to show that something happened
    :return: None
    """

    interface.toggle_relay_state()
    __toggle_on_off(btn_label, msg_label, "relay")


def __toggle_reset_and_message(var, msg, stats):
    """
        Toggles value of reset

        1 - Trigger a reset
        0 - Continue normal operation

    :param var: Label that will have it's message set
    :param msg: Message to assign to the variable
    :return: None
    """
    interface.toggle_reset()
    __set_text(var, msg)
    __configure_and_set_stats_text(stats)


def __set_relay_duration(var, msg, seconds, stats):
    """
        Sets the value of relation to the provided number of seconds

    :param var: Label that will have it's message set
    :param msg: Message to assign to the variable
    :param seconds: New duration to be set
    :return: None
    """
    current_duration = int(interface.get_relay_duration())
    duration_val = current_duration + seconds
    if duration_val < 0:
        duration_val = 0
    interface.set_relay_duration(duration_val)
    __set_text(var, msg)
    __configure_and_set_stats_text(stats)


def __skip_goal(var, msg, stats):
    """
        Sets relay duration to 0, and increases the goal by 1

    :param var: Label that will have it's message set
    :param msg: Message to assign to the variable
    :return: None
    """
    interface.set_relay_duration(0)
    interface.set_goal(interface.get_goal() + 1)
    __set_text(var, msg)
    __configure_and_set_stats_text(stats)


def __get_stats():
    return interface.all_attr()


def __configure_and_set_stats_text(text_var):
    current_stats = __get_stats()
    goal = current_stats["goal"]
    relay_duration = current_stats["relay_duration"]
    stats_str = f"Goal: {goal}\tRelay Duration: {relay_duration}s"
    __set_text(text_var, stats_str)


def __shutdown(root):
    GPIO.cleanup()
    # send interrupt to the Sensors
    os.kill(int(check_output(["pgrep", "-f", "combo_sensor.py"])), SIGKILL)

    # close the GUI
    root.destroy()


if __name__ == "__main__":
    # Data variables for use by GUI
    logo_canvas_width = 175
    logo_canvas_height = 58

    # Set up root
    root = tk.Tk()
    root.title(APPLICATION_TITLE)
    root.geometry("{}x{}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
    root.configure(background=BB_BLUE)
    root.overrideredirect(True)

    # Set up the program icon and other images
    logo_small = tk.PhotoImage(file=os.path.join("images", "boise-brewing-small-logo.png"))
    logo_medium = tk.PhotoImage(file=os.path.join("images", "boise-brewing-medium-logo.png"))
    root.tk.call("wm", "iconphoto", root._w, logo_medium)

    # Set up text variables that require root existing first
    message = tk.StringVar()
    relay_toggle_text = tk.StringVar()
    relay_toggle_text.set("Off")
    sensor_toggle_text = tk.StringVar()
    sensor_toggle_text.set("Off")

    # Set up the display of of the stats display
    stats_text = tk.StringVar()
    __configure_and_set_stats_text(stats_text)

    # Create main containers
    logo_frame_top = tk.Frame(root, bg=BB_BLUE, width=800, height=60, pady=5)
    stats_frame = tk.Frame(root, bg=BB_BLUE, width=800, height=10, pady=5)
    button_frame = tk.Frame(root, bg=BB_BLUE, width=800, height=380, padx=5, pady=5)

    # Set layout of main containers
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    logo_frame_top.grid(row=0)
    stats_frame.grid(row=1)
    button_frame.grid(row=2)

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

    # Set up the labels for the stats bar
    stats_label = tk.Label(stats_frame, textvariable=stats_text, bg=BB_BLUE, fg="white", font="Times 12")

    # Set layout of the widgets for stats frame
    stats_label.grid(sticky="W")
    stats_frame.grid_rowconfigure(0, weight=1)
    stats_frame.grid_columnconfigure(0, weight=1)

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
                               command=partial(__set_message_and_goal, message, "Trigger value increased.", 1,
                                                  stats_text))
    goal_inc_10_btn = tk.Button(btn_col_0_frame, text="+10", width=8, height=4, bg="gray", fg="black", padx=10, pady=10,
                                command=partial(__set_message_and_goal, message, "Trigger value increased.", 10,
                                                  stats_text))

    col1_label = tk.Label(btn_col_1_frame, text="Decrease Goal", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    goal_dec_1_btn = tk.Button(btn_col_1_frame, text="-1", width=8, height=4, bg="gray", fg="black", padx=10, pady=10,
                               command=partial(__set_message_and_goal, message, "Trigger value decreased.", -1,
                                                  stats_text))
    goal_dec_10_btn = tk.Button(btn_col_1_frame, text="-10", width=8, height=4, bg="gray", fg="black", padx=10, pady=10,
                                command=partial(__set_message_and_goal, message, "Trigger value decreased.", -10,
                                                  stats_text))

    col2_label = tk.Label(btn_col_2_frame, text="Goal Reset/Skip", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    goal_reset_btn = tk.Button(btn_col_2_frame, text="Reset", width=8, height=4, bg="gray", fg="black", padx=10,
                               pady=10, command=partial(__toggle_reset_and_message, message, "Trigger value reset.",
                                                  stats_text))
    goal_skip_btn = tk.Button(btn_col_2_frame, text="Skip", width=8, height=4, bg="gray", fg="black", padx=10,
                              pady=10, command=partial(__skip_goal, message, "Trigger skipped",
                                                       stats_text))

    col3_label = tk.Label(btn_col_3_frame, text="Manage Relay", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    relay_toggle_btn = tk.Button(btn_col_3_frame, textvariable=relay_toggle_text, width=8, height=4, bg="gray",
                                 fg="black", padx=10, pady=10,
                                 command=partial(__toggle_relay, relay_toggle_text, message))
    relay_inc_dur_btn = tk.Button(btn_col_3_frame, text="Longer", width=8, height=4, bg="gray",
                                  fg="black", padx=10, pady=10,
                                  command=partial(__set_relay_duration, message, "Relay Duration Increased.", 5,
                                                  stats_text))
    relay_dec_dur_btn = tk.Button(btn_col_3_frame, text="Shorter", width=8, height=4, bg="gray",
                                  fg="black", padx=10, pady=10,
                                  command=partial(__set_relay_duration, message, "Relay Duration Decreased.", -5,
                                                  stats_text))

    col4_label = tk.Label(btn_col_4_frame, text="Sensors On/Off", font="Times 14", bg=BB_BLUE, fg=BB_GOLD)
    sensor_toggle_btn = tk.Button(btn_col_4_frame, textvariable=sensor_toggle_text, width=8, height=4, bg="gray",
                                  fg="black", padx=10, pady=10,
                                  command=partial(__toggle_sensor, sensor_toggle_text, message))
    gui_close_btn = tk.Button(btn_col_4_frame, text="Close", width=8, height=4, bg="gray", fg="red", padx=10, pady=10,
                              command=partial(__shutdown, root))

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
    gui_close_btn.grid(row=3)

    root.mainloop()
