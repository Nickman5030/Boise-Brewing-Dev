# Turns on Blue LED light and keeps it on
# Pin 6 is the ground
# GPIO 17 is RED
# GPIO 27 is BLUE
# GPIO 22 is GREEN

import time

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

GPIO.setup(22, GPIO.OUT)

GPIO.setup(17, GPIO.OUT)

def run_leds():
    GPIO.output((27, 22, 17), GPIO.HIGH)

def stop_leds():
    GPIO.output((27, 22, 17), GPIO.LOW)
    GPIO.cleanup()


if __name__ == "__main__":
    run_leds()
    time.sleep(5)
    stop_leds()
