#Turns on Blue LED light and keeps it on
# Pin 6 is the ground
# GPIO 17 is RED
# GPIO 27 is GREEN
# GPIO 22 is BLUE
import pigpio

PIN=22
BRIGHTNESS=128

pi = pigpio.pi()
pi.set_PWM_dutycycle(PIN, BRIGHTNESS)

pi.stop()
