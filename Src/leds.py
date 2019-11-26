# Turns on Blue LED light and keeps it on
# Pin 6 is the ground
# GPIO 17 is RED
# GPIO 27 is GREEN
# GPIO 22 is BLUE

# IMPORTANT run $sudo pigpiod before running this program
# usage $python3 simple_LED.py
import time

# import pigpio
#
# pi = pigpio.pi()
#
#
# def run_leds():
#     PIN = 22
#     BRIGHTNESS = 128
#
#     pi.set_PWM_dutycycle(PIN, BRIGHTNESS)
#     pi.write(1)
#
#
# def stop_leds():
#     pi.write(0)
#     # pi.stop()


import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)


def run_leds():
    GPIO.output(22, GPIO.HIGH)


def stop_leds():
    GPIO.output(22, GPIO.LOW)


