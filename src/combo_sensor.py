import RPi.GPIO as GPIO
import time
from datetime import datetime
import interface
from math import ceil

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_PIR = 25
GPIO_BLUE = 27
GPIO_RED = 17
GPIO_GREEN = 22

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_PIR, GPIO.IN)  # PIR
GPIO.setup(GPIO_BLUE, GPIO.OUT)
GPIO.setup(GPIO_GREEN, GPIO.OUT)
GPIO.setup(GPIO_RED, GPIO.OUT)

# Ceiling on distance from US sensor
# Distances greater than this will be thrown out to account for door being open
# TODO: adjust based on distance from sensor to door/wall
MAX_DISTANCE = 250
MIN_DISTANCE = 150


def distance():
    """
    Uses the ultrasonic sensor to measure the distance from the sensor
    to whatever it is pointing at.
    :return:
    """
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2

    return distance


def find_average(arr, reverse=False):
    """
    find distance between sensor and object at end of polling. Finds final by default
    can set reverse True to find initial
    :param: array of value to find the average of
    :param: whether to reverse the array or not. Set True to find initial
    :return: averaged distance
    """
    array_vals = arr.copy()
    if reverse:
        array_vals.reverse()
    # for small arrays of valid distances
    if len(array_vals) == 0:
        divisor = 1
    elif len(array_vals) < 5:
        divisor = len(array_vals)
    else:
        divisor = 5
    new_array = array_vals[0:divisor]
    max_val = sum(new_array)
    max_val = max_val / divisor
    return max_val


def run_leds():
    """
    turns on all three Leds
    :return:
    """
    GPIO.output((GPIO_BLUE, GPIO_GREEN, GPIO_RED), GPIO.HIGH)


def stop_leds():
    """
    turns off all three leds
    :return:
    """
    GPIO.output((GPIO_BLUE, GPIO_GREEN, GPIO_RED), GPIO.LOW)


def run_sensors():
    """
    Runs PIR and ultrasonic sensors. The ultrasonic sensor reads after the
    the PIR sensor has triggered.
    :return:
    """
    try:
        time.sleep(2)  # to stabilize sensor
        count = 0
        total_count = 0
        start_time = datetime.now()
        while True:
            # get the value that will trigger a prize
            target_val = interface.get_goal()

            # Check if we are supposed to exit
            if interface.get_shutdown_state() == 0:
                raise KeyboardInterrupt

            # check if the sensor is set to be on or off
            if interface.get_sensor_state() == 1:
                current_time = datetime.now()
                if interface.get_relay_state() == 1:
                    if (current_time - start_time).total_seconds() >= interface.get_relay_duration():
                        interface.toggle_relay_state()
                        stop_leds()
                        start_time = datetime.now()

                if interface.get_reset() == 1:
                    # resets progress to goal
                    count = 0
                    # changes reset state back to zero
                    interface.toggle_reset()
                # Read from the PIR sensor
                if GPIO.input(25):
                    distance_array = []
                    # TODO: number of polls may need adjustment
                    for i in range(0, 50):
                        dist = distance()
                        # only add values less than the max distance. Helps with inaccurate reads, or reads from
                        # areas we don't care about
                        if MIN_DISTANCE < dist < MAX_DISTANCE:
                            distance_array.append(dist)
                        # TODO: polling frequency may need adjustment
                        time.sleep(.1)
                    sorted_distance_array = sorted(distance_array)

                    # We are cutting 10% from the front and back of the array
                    trim_val = ceil(len(sorted_distance_array) * 0.1)
                    initial = find_average(sorted_distance_array[trim_val:], reverse=True)
                    final = find_average(sorted_distance_array[:(trim_val * -1)])

                    # TODO: add possible padding value to account for standing in doorway
                    if (initial - final) >= 50:
                        count = count + 1
                        total_count = total_count + 1
                        print(f"{count}/{target_val}\tTotal: {total_count}")
                        print(f"{initial} - {final}")
                        if count == target_val:
                            interface.toggle_relay_state()

                            start_time = datetime.now()
                            run_leds()
                            count = 0
                    # Accounts for the occasional empty array, no valid values from ultrasonic
                    elif (initial - final) == 0:
                        continue

                    time.sleep(3)  # to avoid multiple detection
                time.sleep(0.1)  # loop delay, should be less than detection delay

    except:
        GPIO.cleanup()


if __name__ == "__main__":
    try:
        run_sensors()
    except KeyboardInterrupt:
        GPIO.cleanup()
