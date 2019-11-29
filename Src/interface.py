"""
    These methods are used by the sensor program and the GUI to communicate with each other. The information shared by
    the two is stored in a file Src/data/data_log.py

:author: Garrett Allen
"""

import os
import fcntl
import pickle
from sensor_data import SensorData as __SensorData


__DATA_FILE = os.path.join(os.getcwd(), "data", "data_log.py")


def __load_sensor_data():
    """
        Function to load the pickled class from the file for interaction with

    :return: Returns a usable, loaded instance of SensorData
    """
    while True:
        try:
            data_file = open(__DATA_FILE, "rb")
            fcntl.flock(data_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            loaded_data = pickle.load(data_file)
            data_file.close()
            return loaded_data

        except FileNotFoundError:
            return __SensorData()
        except OSError:
            # This happens if lock is unavailable, so just go to next iteration until the function returns
            continue


def __write_sensor_data(cls):
    """
        Writes the current state of SensorData class to a file to persist data

    :param cls: Instance of SensorData to be written to disk
    :return: None
    """
    while True:
        try:
            data_file = open(__DATA_FILE, "wb")
            fcntl.flock(data_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            pickle.dump(cls, data_file)
            data_file.close()
            break
        except OSError:
            # This happens if lock is unavailable, so just go to next iteration until the function returns
            continue

    # with open(__DATA_FILE, "wb") as data_file:
    #     pickle.dump(cls, data_file)



def all_attr():
    """
    :return: Dictionary of all the current attributes of the SensorData instance
    """
    data = __load_sensor_data()

    return data.all()


def get_goal():
    """
    :return: Current value of goal
    """
    data = __load_sensor_data()
    return data.get_goal()


def set_goal(val):
    """
        Updates the value in goal

    :param val: Value to be assigned to goal
    :return: None
    """
    data = __load_sensor_data()
    data.set_goal(val)
    __write_sensor_data(data)


def get_sensor_state():
    """
    :return: Current state of sensors (On/Off)
    """
    data = __load_sensor_data()
    return data.get_sensor_state()


def toggle_sensor_state():
    """
        Sets the on/off state of the sensors

        1 - ON
        0 - OFF

    :return: None
    """
    data = __load_sensor_data()
    data.toggle_sensor_state()
    __write_sensor_data(data)


def get_relay_state():
    """
    :return: Current state of relay
    """
    data = __load_sensor_data()
    return data.get_relay_state()


def toggle_relay_state():
    """
        Sets the on/off state of the sensors

        1 - ON
        0 - OFF

    :return: None
    """
    data = __load_sensor_data()
    data.toggle_relay_state()
    __write_sensor_data(data)


def get_reset():
    """
    :return: Current value of the reset attribute
    """
    data = __load_sensor_data()
    return data.get_reset()


def toggle_reset():
    """
        Toggles value of reset

        1 - Trigger a reset
        0 - Continue normal operation

    :return: None
    """
    data = __load_sensor_data()
    data.toggle_reset()
    __write_sensor_data(data)


def get_relay_duration():
    """
    :return: Current value of the relay duration setting
    """
    data = __load_sensor_data()
    return data.get_relay_duration()


def set_relay_duration(seconds):
    """
        Sets the value of relation to the provided number of seconds

    :param seconds: New duration to be set
    :return: None
    """
    data = __load_sensor_data()
    data.set_relay_duration(seconds)
    __write_sensor_data(data)
