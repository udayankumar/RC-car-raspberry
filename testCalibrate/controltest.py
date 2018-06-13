
# Helps to figure out Max and Min values for ESC
# Using Right and Left Arrow keys, one can figure out Max and Min turn values
# Using Up and Down Arrow keys, one can settle on a speed limits suitable for the future task.
# Modified from http://www.codehaven.co.uk/using-arrow-keys-with-inputs-python/
# Author: Udayan Kumar
from __future__ import division
import curses
import time
# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=0)

# Configure min and max servo pulse lengths 
#TODO: adjust them for your car and motor
turn_servo_right = 360  # Min pulse length out of 4096
turn_servo_left = 200  # Max pulse length out of 4096

move_esc_back = 350  # Min pulse length out of 4096
move_esc_fwd = 50  # Max pulse length out of 4096

pulse_freq = 50
# Set frequency to 50hz, good for esc.
pwm.set_pwm_freq(pulse_freq)
 

def getCenter():
	return 280
def getStop():
	return 250

current_turn_position = getCenter()
current_movement = getStop()


# get the curses screen window
screen = curses.initscr()
 
# turn off input echoing
curses.noecho()
 
# respond to keys immediately (don't wait for enter)
curses.cbreak()
 
# map arrow keys to special values
screen.keypad(True)
 
# press s to stop 
try:
    while True:
        char = screen.getch()
	screen.clear()
	move = False
        if char == ord('q'):
            break
        elif char == curses.KEY_RIGHT:
	    if current_turn_position > turn_servo_left:
		current_turn_position -= 1 
		move = True
            screen.addstr(0, 0, 'right '+ str(current_turn_position) )       
        elif char == curses.KEY_LEFT:
            # print doesn't work with curses, use addstr instead
	    if current_turn_position < turn_servo_right:
		current_turn_position += 1 
		move = True
            screen.addstr(0, 0, 'left ' + str(current_turn_position) )
        elif char == curses.KEY_UP:
	    if current_movement > move_esc_fwd:
		current_movement -= 1 
		move = True
            screen.addstr(0, 0, 'up   ' + str(current_movement))       
        elif char == curses.KEY_DOWN:
	    if current_movement < move_esc_back:
		current_movement += 1 
		move = True
            screen.addstr(0, 0, 'down    ' + str(current_movement))       
	elif char == ord('s'):
	    # stop everything 
	    current_movement = getStop() 
	    current_turn_position  = getCenter()
            screen.addstr(0, 0, 'up    ' + str(current_movement) + ' and down ' + str(current_turn_position))       
	    move = True
	    
	if move:
		pwm.set_pwm(0, 0, current_turn_position)
		pwm.set_pwm(1, 0, current_movement)
finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()


