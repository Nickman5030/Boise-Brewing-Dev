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
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


def run_sensors():
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
