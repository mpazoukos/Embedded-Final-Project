import tuio
import time
import socket
import math

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

	
tracking = tuio.Tracking()
print "loaded profiles:", tracking.profiles.keys()
tmp2 = 0
tracking.update()

try:
  while 1:
    tracking.update()
    tmp = 0
    for obj in tracking.objects():
      if tmp == 0:
        robot = obj
	x_robot = round(robot.xpos,3) - 0.06
	#print("****** x Robot: " + str(x_robot) + "********")
	y_robot = -1*(round(robot.ypos,3) - 0.9)
	#print ("****** y Robot: " + str(y_robot) + "********")

	# Converting robot's angle to correct axis system
	angle_robot = -1*(math.floor(robot.angle) - 270)
	if angle_robot >= 360:
		angle_robot -= 360
	elif angle_robot < 0:
		angle_robot = 360 - (-angle_robot)
	if angle_robot == -0:
		angle_robot = 0
	print ("Angle of the Robot: " + str(angle_robot))
        tmp += 1
	
      else:
	print ("\n")
        base = obj
	x_base = round(base.xpos,5) - 0.06
	#print("****** x base: " + str(x_base) + "********")
	y_base = -1*(round(base.ypos,5) - 0.9)
	#print("****** y base: " + str(y_base) + "********")
	angle_base = math.floor(base.angle)	
	#print ("Angle of the base: " + str (angle_base))
	print ("\n")

        # Calculate Distance vectors
	x_vect = x_base - x_robot
	y_vect = y_base - y_robot
	dist = math.sqrt((x_base-x_robot)**2+(y_base-y_robot)**2)

	# Converting target's angle to correct axis system
	ang_vect = math.floor(math.atan2(x_vect,y_vect)*180/math.pi)
	ang_vect = -1*(ang_vect+270)



	if ang_vect < 0 and abs(ang_vect) > 360:
		ang_vect = 720 - abs(ang_vect)
	elif ang_vect < 0:
		ang_vect = 360-abs(ang_vect)
	elif ang_vect >= 360:
		ang_vect -= 360
	elif ang_vect < 0 and abs(ang_vect) > 360:
		ang_vect = 720 - abs(ang_vect)
	if ang_vect == -0:
		ang_vect = 0

	# Calculate angles
	right_angle = ang_vect - angle_robot
	if right_angle < 0:
		right_angle += 360
	left_angle = angle_robot - ang_vect
	if left_angle < 0:
		left_angle += 360

	# Print angles
	print("Left angle: " + str(left_angle))
	print("Right angle: " + str(right_angle))	
	
	print ("Angle of the Vector: " + str(ang_vect))
	print ("Distance: " + str(dist))

	if dist <= 0.1:
			tracking.update()
			s.send(stop)
			sleep(0.1)

	elif abs(ang_vect - angle_robot) <= 10:
		print("YOU ARE POINTING AT IT BABY")
		s.send(stop)
		s.send('FF020135FF'.decode('hex')) # Left motor speed
		s.send('FF020235FF'.decode('hex')) # Right motor speed
		sleep(0.01)
		s.send(forward)
		sleep(0.05)
		tracking.update()
		s.send(stop)
	else:
		rotate = False
		if dist > 0.18:
			if left_angle <= right_angle:
				if left_angle >= 80:
					rotate = True
				else:
					# Turn left
					s.send('FF020105FF'.decode('hex')) # Left motor speed
					s.send('FF020230FF'.decode('hex')) # Right motor speed
					sleep(0.01)
					s.send(forward)
					sleep(0.05)
					tracking.update()
					s.send(stop)
					
			else:
				if right_angle >= 80:
					rotate=True
				else:
				# Turn Right
					s.send('FF020130FF'.decode('hex')) # Left motor speed
					s.send('FF020205FF'.decode('hex')) # Right motor speed	
					sleep(0.01)
					s.send(forward)
					sleep(0.05)
					tracking.update()
					s.send(stop)
		else:
			rotate = True
		if rotate == True:
			if left_angle <= right_angle:
				s.send(r_left)
			else:
				s.send(r_right)
			sleep(0.01)
			tracking.update()
			s.send(stop)
	 
	
   
       
except KeyboardInterrupt:
	tracking.stop()
	s.send(stop)
