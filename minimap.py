import pygame
import numpy as np
from character import ViewCollision

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)

class Minimap:

	def __init__(self, surface, posX, posY, mapW, mapH):
		self._surface = surface
		self._posX = posX
		self._posY = posY
		self._blockSize = 32
		self._mapW = mapW
		self._mapH = mapH

		self._view: ViewCollission = None
		self._pos: np.array = None

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

	def draw_ray(self, pos, point, color = RED):
		from_point = (self._posX + int(pos[0]*self._blockSize), self._posY + int(pos[1]*self._blockSize))
		to_point = (self._posX + int(point[0]*self._blockSize), self._posY + int(point[1]*self._blockSize))
		pygame.draw.line(self._surface, color, from_point, to_point, 1)

	def update(self, plane: np.array, pos: np.array, view: ViewCollision):
		self._view = view
		self._pos = pos
		self._plane = plane

	def render(self):
		self.draw_grid()
		if self._view is not None and self._pos is not None:
			self.draw_player(self._pos)
			for point in self._view.points:
				self.draw_ray(self._pos, point)
		self.draw_ray(self._pos - self._plane, self._pos + self._plane, BLUE)

			