import numpy as np
import pygame
import sys
import time

edge_norm = 80

pos_vec = np.array([350, 500])
point2_vec = np.array([-100, 0])

point2 = pos_vec + point2_vec

def recursive_shape_generator(RotMtx, point, vector, point2, point_array):  #initial vector is the common edge
	
	new_vec = np.matmul(RotMtx, vector) #Rotate the vector by multiply it with rotation matrix
	new_point = point + new_vec			#determine the next point as a sum of the current point and rotated vector
	point_array.append(new_point)		#push it to the point list
	
	if(np.linalg.norm(point2-new_point) < 0.0001):	#if the next point is(neglet the error) the initial point then: stop
		return new_point
	else:
		return recursive_shape_generator(RotMtx, new_point, -new_vec, point2, point_array)	#Else turn the vector for the point and use it again

polygons = []
lower_bound = 3
upper_bound = 13

for n in range(lower_bound, upper_bound+1):
	angle = (n-2)*np.pi/n
	RotMtx = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])
	point_set = [pos_vec]
	recursive_shape_generator(RotMtx, pos_vec, point2_vec, point2, point_set)
	polygons.append(point_set)


screen = pygame.display.set_mode((625, 550))
RED = (255, 0, 0)
WHITE = (255, 255, 255)

direction = -1
current = 0

while True: 

	for event in pygame.event.get(): 
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill(WHITE)
	
	if(current == 0 or current == len(polygons)):
		direction *= -1
		
	off_set = np.array(polygons)[:current+1]

	for polygon in off_set:
		n = len(polygon)
		for i in range(n+1):
			pygame.draw.line(screen, RED, (polygon[i%n][0], polygon[i%n][1]), (polygon[(i+1)%n][0], polygon[(i+1)%n][1]), 1)	
	
	current += direction
	time.sleep(0.1)
	
	pygame.display.flip()

