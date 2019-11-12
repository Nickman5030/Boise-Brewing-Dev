import RPi.GPIO as GPIO
import time
#from gui import *

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_PIR = 25

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_PIR, GPIO.IN)  # PIR

# Ceiling on distance from US sensor
# Distances greater than this will be thrown out to account for door being open
# TODO: adjust based on distance from sensor to door/wall
MAX_DISTANCE = 210


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


def find_average(array_vals, reverse=False):
    """
    find distance between sensor and object at end of polling. Finds final by default
    can set reverse True to find initial
    :param: array of value to find the average of
    :param: whether to reverse the array or not. Set True to find initial
    :return: averaged distance
    """
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
        while True:
            # TODO: set the value that will trigger the prize
            #target_val = get_target_val(), get this from the gui
            target_val = 3
            # Read from the PIR sensor
            if GPIO.input(25):
                print("Motion Detected...")
                distance_array = []
                # TODO: number of polls may need adjustment
                for i in range(0, 30):
                    dist = distance()
                    # only add values less than the max distance. Helps with inaccurate reads, or reads from
                    # areas we don't care about
                    if dist < MAX_DISTANCE:
                        distance_array.append(dist)
                    # TODO: polling frequency may need adjustment
                    time.sleep(.1)
                initial = find_average(distance_array, reverse=True)
                final = find_average(distance_array)
                print("Initial: ", initial)
                print("Final: ", final)

                # TODO: add possible padding value to account for standing in doorway
                if (initial - final) > 0:
                    print("customer enters")
                    count = count + 1
                    total_count = total_count + 1
                    if count == target_val:
                        print("Target Achieved!")
                        count = 0
                # Accounts for the occasional empty array, no valid values from ultrasonic
                elif (initial - final) == 0:
                    continue
                else:
                    print("customer exits")

                print("progress to target {0}/{1}".format(count, target_val))
                print("total customers {0}".format(total_count))

                time.sleep(3)  # to avoid multiple detection
            time.sleep(0.1)  # loop delay, should be less than detection delay

    except:
        GPIO.cleanup()


if __name__ == "__main__":
    run_sensors()
