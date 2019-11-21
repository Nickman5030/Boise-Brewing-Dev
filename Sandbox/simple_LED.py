#Turns on Blue LED light and keeps it on
import pigpio

PIN=24
BRIGHTNESS=128

pi = pigpio.pi()
pi.set_PWM_dutycycle(PIN, BRIGHTNESS)

pi.stop()
