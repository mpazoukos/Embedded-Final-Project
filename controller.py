import tuio
import time
import socket
import math
import keyboard

from time import sleep

# All commands
forward = 'FF000100FF'.decode('hex')
backward = 'FF000200FF'.decode('hex')
stop = 'FF000000FF'.decode('hex')
r_left = 'FF000300FF'.decode('hex')
r_right = 'FF000400FF'.decode('hex')

#*******************************************
#******** CHANGE TO 1 TO ENABLE SSH ********
#******************************************* 
enable_socket = 1 

if enable_socket:
	# Connect to robot
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.1.1", 2001))
	
while True:
	if keyboard.is_pressed('w'): # Move Straight
		s.send('FF020150FF'.decode('hex')) # Left motor speed
		s.send('FF020250FF'.decode('hex')) # Right motor speed
		s.send(forward)
		sleep(0.05)
		s.send(stop)
	if keyboard.is_pressed('a'): # Turn Left
		s.send('FF020150FF'.decode('hex')) # Left motor speed
		s.send('FF020250FF'.decode('hex')) # Right motor speed
		s.send(r_right)
		sleep(0.05)
		s.send(stop)
	if keyboard.is_pressed('d'): # Turn Right
		s.send('FF020150FF'.decode('hex')) # Left motor speed
		s.send('FF020250FF'.decode('hex')) # Right motor speed
		s.send(r_left)
		sleep(0.05)
		s.send(stop)
	if keyboard.is_pressed('s'): # Reverse
		s.send('FF020130FF'.decode('hex')) # Left motor speed
		s.send('FF020230FF'.decode('hex')) # Right motor speed
		s.send(backward)
		sleep(0.05)
		s.send(stop)

			
