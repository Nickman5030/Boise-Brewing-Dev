"""
    This is a class to store the data that needs to be shared between combo_sensors.py and gui.py. This object is
    pickled and written to a file by interface.py

:author: Garrett Allen
"""


class SensorData(object):
    def __init__(self):
        self.goal = 80
        self.relay_state = 0  # 1 = On, 0 = Off
        self.sensor_state = 1 # 1 = On, 0 = Off
        self.reset = 0  # 1 = Trigger Reset, 0 = No reset
        self.relay_duration = 10  # seconds
        self.shutdown = 0  # 0 means leave on, 1 means turn off

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

    def toggle_shutdown(self):
        """
            toggles shutdown flag

        :return: None
        """

        self.shutdown = int(not self.shutdown)

    def get_shutdown_state(self):
        """
            Getter for shutdown attribute

        :return: Returns the current value of shutdown attribute
        """
        return self.shutdown
