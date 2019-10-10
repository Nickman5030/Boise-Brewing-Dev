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
            print("No motion...")
            if GPIO.input(25):
                print("Motion Detected...")
                print(distance())
                count += 1
                time.sleep(3)  # to avoid multiple detection
            time.sleep(0.1)  # loop delay, should be less than detection delay

    except:
        GPIO.cleanup()


if __name__ == "__main__":
    run_sensors()
