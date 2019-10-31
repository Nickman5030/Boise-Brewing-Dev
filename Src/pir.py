import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN) #PIR

try:
    time.sleep(2) # to stabilize sensor
    count = 0
    while True:
        print("No motion...")
        if GPIO.input(25):
            print("Motion Detected...")
            count += 1
            time.sleep(3) #to avoid multiple detection
        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()