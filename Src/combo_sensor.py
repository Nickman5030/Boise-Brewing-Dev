import RPi.GPIO as GPIO
import time

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


def findInitial(arrayVals):
    """
    find the distane between sensor and object at start of polling
    :return: averaged distance
    """
    # for small arrays of valid distances
    if len(arrayVals) < 5:
        divisor = len(arrayVals)
    else:
        divisor = 5
    newArray = arrayVals[0:divisor]
    maxVal = sum(newArray)
    maxVal = maxVal / divisor
    return maxVal


def findFinal(arrayVals):
    """
    find distance between sensor and object at end of polling
    :return: averaged distance
    """
    arrayVals.reverse()
    # for small arrays of valid distances
    if len(arrayVals) < 5:
        divisor = len(arrayVals)
    else:
        divisor = 5
    newArray = arrayVals[0:divisor]
    maxVal = sum(newArray)
    maxVal = maxVal / divisor
    return maxVal


def run_sensors():
    """
    Runs PIR and ultrasonic sensors. The ultrasonic sensor reads after the
    the PIR sensor has triggered.
    :return:
    """
    try:
        time.sleep(2)  # to stabilize sensor
        count = 0
        while True:
            if GPIO.input(25):
                print("Motion Detected...")

                i = 0
                dArray = []
                # TODO: number of polls may need adjustment
                for i in range(0, 50):
                    dist = distance()
                    if dist < MAX_DISTANCE:
                        dArray.append(dist)
                        x = 1
                    i = i + 1
                    # TODO: polling frequency may need adjustment
                    time.sleep(.1)
                for item in dArray:
                    print(item)

                initial = findInitial(dArray)
                final = findFinal(dArray)
                print("Initial: ", initial)
                print("Final: ", final)

                # TODO: add possible padding value to account for standing in doorway
                if (initial - final) > 0:
                    print("customer enters")
                    count = count + 1
                else:
                    print("customer exits")

                print(count)

                time.sleep(3)  # to avoid multiple detection
            time.sleep(0.1)  # loop delay, should be less than detection delay

    except:
        GPIO.cleanup()


if __name__ == "__main__":
    run_sensors()
