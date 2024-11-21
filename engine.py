import numpy as np
import pygame
import math

from pygame.locals import *
from minimap import Minimap
from character import ViewCollision

import utils as u

# This is the map as seen from above, I consider the first block as position (x,y) = (0,0)
roomMap = [ \
[1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,1],
[1,0,0,0,1,0,0,0,1],
[1,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1]]

blockSize = 32;
screenH = 600
screenW = 800

# PyGame screen
pygame.init()
screen = pygame.display.set_mode((screenW, screenH), 0, 32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
pygame.display.set_caption("Engine")

# Starting position
pos = np.array([1.5, 1.5])

# Looking right
dire = np.array([0., -1.])
dire = u.normalize(dire, 1)

# Plane
plane = u.perpendicular(dire)
plane = u.normalize(plane, 1)


minimap = Minimap(screen, screenW-len(roomMap[0])*32, 0, len(roomMap[0]), len(roomMap))

time_delta = 0
while True:
	frame_start = pygame.time.get_ticks()

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()

	pressed = pygame.key.get_pressed()

	rotation = 0
	if pressed[K_LEFT]:
		rotation = -10
		print("left", dire)
	if pressed[K_RIGHT]:
		rotation = 10
		print("right", dire)
	if pressed[K_UP]:
		pos += dire*0.1
	if pressed[K_DOWN]:
		pos -= dire*0.1

	dire = u.rotate(dire, rotation)
	plane = u.normalize(u.perpendicular(dire), 1)

	screen.fill(BLACK)
	
	cam0 = pos - plane
	cam1 = pos + plane
	points = []
	for i, r in enumerate(np.linspace(-1, 1, screenW)):
		point, dist = u.raycast(dire + plane*r, pos, roomMap)
		# Distance to camera plane (line)
		h = 1/np.linalg.norm(np.cross(cam0-cam1, cam1-point))/np.linalg.norm(cam0-cam1)*screenH
		points.append(point)
		rect = [i, screenH/2 - h/2, 1, h]
		pygame.draw.rect(screen, GREEN, rect, 1)
	
	minimap.update(plane, pos, ViewCollision(points))
	minimap.render()

	pygame.display.update()

	time_delta = pygame.time.get_ticks() - frame_start
