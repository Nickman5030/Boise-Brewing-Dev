"""
    These methods are used by the sensor program and the GUI to communicate with each other. The information shared by
    the two is stored in a file Src/data/data_log.py

:author: Garrett Allen
"""

import os
import pickle
from sensor_data import SensorData as __SensorData


__DATA_FILE = os.path.join(os.getcwd(), "data", "data_log.py")


def __load_sensor_data():
    """
        Function to load the pickled class from the file for interaction with

    :return: Returns a usable, loaded instance of SensorData
    """
    try:
        with open(__DATA_FILE, "rb") as data_file:
            return pickle.load(data_file)
    except FileNotFoundError:
        return __SensorData()


def __write_sensor_data(cls):
    """
        Writes the current state of SensorData class to a file to persist data

    :param cls: Instance of SensorData to be written to disk
    :return: None
    """
    with open(__DATA_FILE, "wb") as data_file:
        pickle.dump(cls, data_file)


def all_attr():
    """
    :return: Dictionary of all the current attributes of the SensorData instance
    """
    data = __load_sensor_data()

    return data.__dict__


def get_goal():
    """
    :return: Current value of goal
    """
    data = __load_sensor_data()
    return data.goal


def set_goal(val):
    """
        Updates the value in goal

    :param val: Value to be assigned to goal
    :return: None
    """
    data = __load_sensor_data()
    data.goal = val
    __write_sensor_data(data)


def get_sensor_state():
    """
    :return: Current state of sensors (On/Off)
    """
    data = __load_sensor_data()
    return data.sensor_state


def toggle_sensor_state():
    """
        Sets the on/off state of the sensors

        1 - ON
        0 - OFF

    :return: None
    """
    data = __load_sensor_data()
    data.sensor_state = int(not data.sensor_state)
    __write_sensor_data(data)


def get_relay_state():
    """
    :return: Current state of relay
    """
    data = __load_sensor_data()
    return data.relay_state


def toggle_relay_state():
    """
        Sets the on/off state of the sensors

        1 - ON
        0 - OFF

    :return: None
    """
    data = __load_sensor_data()
    data.relay_state = int(not data.relay_state)
    __write_sensor_data(data)


def get_reset():
    """
    :return: Current value of the reset attribute
    """
    data = __load_sensor_data()
    return data.reset


def toggle_reset():
    """
        Toggles value of reset

        1 - Trigger a reset
        0 - Continue normal operation

    :return: None
    """
    data = __load_sensor_data()
    data.reset = int(not data.reset)
    __write_sensor_data(data)


def get_relay_duration():
    """
    :return: Current value of the relay duration setting
    """
    data = __load_sensor_data()
    return data.relay_duration


def set_relay_duration(seconds):
    """
        Sets the value of relation to the provided number of seconds

    :param seconds: New duration to be set
    :return: None
    """
    data = __load_sensor_data()
    data.relay_duration = seconds