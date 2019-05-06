import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)

class Minimap:

	def __init__(self, surface, posX, posY, mapW, mapH):
		self._surface = surface
		self._posX = posX
		self._posY = posY
		self._blockSize = 32
		self._mapW = mapW
		self._mapH = mapH

	def draw_grid(self):
		for i in range(1, self._mapW):
			from_point =  (self._posX + i*self._blockSize, self._posY)
			to_point = (i*self._blockSize + self._posX, self._posY + self._mapH*self._blockSize)
			pygame.draw.line(self._surface, RED, from_point, to_point, 1)

		for j in range(1, self._mapH):
			from_point = (self._posX, self._posY + j*self._blockSize)
			to_point = (self._posX + self._mapW*self._blockSize, j*self._blockSize)
			pygame.draw.line(self._surface, RED, from_point, to_point, 1)

	def draw_player(self, pos):
		pygame.draw.circle(self._surface, GREEN, (self._posX + int(pos[0]*self._blockSize), self._posY + int(pos[1]*self._blockSize)), 1)


	def draw_ray(self, pos, point):
		from_point = (self._posX + int(pos[0]*self._blockSize), self._posY + int(pos[1]*self._blockSize))
		to_point = (self._posX + int(point[0]*self._blockSize), self._posY + int(point[1]*self._blockSize))
		pygame.draw.line(self._surface, RED, from_point, to_point, 1)
