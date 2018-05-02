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

x_arr = [0.85, 0.83, 0.77, 0.68, 0.56, 0.44, 0.32, 0.23, 0.17, 0.15]
y_arr = [0.5, 0.72, 0.84, 0.8, 0.62, 0.38, 0.2, 0.16, 0.28, 0.5]

if enable_socket:
	# Connect to robot
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("192.168.1.1", 2001))

	
tracking = tuio.Tracking()
print "loaded profiles:", tracking.profiles.keys()
tracking.update()
counter = 0

# Open and write in new file
output = open("traj.csv", "w")
output.write("x_val, y_val" + "\n")

try:
  while counter < 10:
    tracking.update()
    tmp = 0
    for obj in tracking.objects():
        robot = obj
	x_robot = round(robot.xpos,3) - 0.06
	y_robot = -1*(round(robot.ypos,3) - 0.9)
	if counter != 0:
		output.write(str(x_robot) + ", " + str(y_robot) + "\n")

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
	
	print ("\n")
	x_base = x_arr[counter]
	y_base = y_arr[counter]
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
	print("Robot X: " + str(x_robot))
	print("Robot Y: " + str(y_robot))
	print("\n")
	print("Target X: " + str(x_base))	
	print("Target Y: " + str(y_base))
	print("\n")	
	print ("Distance: " + str(dist))

	if dist <= 0.12:
			tracking.update()
			s.send(stop)
			sleep(0.1)
			if counter == 0:
				start_t = time.time()
			counter += 1

	elif abs(ang_vect - angle_robot) <= 10:
		# Straight
		s.send(stop)
		if counter == 0:
			s.send('FF020110FF'.decode('hex')) # Left motor speed
			s.send('FF020210FF'.decode('hex')) # Right motor speed
		else:
			s.send('FF020135FF'.decode('hex')) # Left motor speed
			s.send('FF020235FF'.decode('hex')) # Right motor speed
		sleep(0.01)
		s.send(forward)
		sleep(0.05)
		tracking.update()
		s.send(stop)
	else:
		rotate = False
		if dist > 0.05:
			if left_angle <= right_angle:
				if left_angle >= 70:
					rotate = True
				else:
					# Turn left
					s.send('FF020101FF'.decode('hex')) # Left motor speed
					s.send('FF020240FF'.decode('hex')) # Right motor speed
					sleep(0.01)
					s.send(forward)
					sleep(0.05)
					tracking.update()
					s.send(stop)
					
			else:
				if right_angle >= 60:
					rotate=True
				else:
				# Turn Right
					s.send('FF020140FF'.decode('hex')) # Left motor speed
					s.send('FF020201FF'.decode('hex')) # Right motor speed	
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
  s.send(stop)
  end_t = time.time()
  dt = (end_t - start_t)
  print("\n")
  print("Time elapsed: " + str(dt))
  output.close()
  exit(1)	 
	
   
       
except KeyboardInterrupt:
	tracking.stop()
	s.send(stop)
	exit(1)
