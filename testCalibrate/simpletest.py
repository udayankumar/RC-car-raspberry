# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# I have modified the example code to work with ESC specifically on RC cars.

# Author: Udayan Kumar (original author: Tony DiCola)
# License: Public Domain



# Be sure to secure the car before testing it. 
# I generally put it upside down on a small but thick book.

from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
#pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=0)

# Configure min and max servo pulse lengths
servo_min = 250  # Min pulse length out of 4096
servo_max = 350  # Max pulse length out of 4096

pulse_freq = 50

# TODO: Change this value to the channel your motor is connected on ADC. 
 
channel = 0


# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= pulse_freq       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(pulse_freq)

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(channel, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(channel, 0, servo_max)
    time.sleep(1)
