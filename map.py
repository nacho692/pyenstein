import numpy as np
import utils
import pygame
import character as chr
from typing import NamedTuple

class ViewCollision(NamedTuple):
    points: list[np.array]
    dire: np.array
    pos: np.array
    plane: np.array

class Map:
    def __init__(self, screen, screen_w, screen_h, room_map):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen = screen
        self.room_map = room_map
        self.view: ViewCollision | None = None

    def update(self, char: chr.Character):
        plane = utils.normalize(utils.perpendicular(char.dire), 1)
        points = []
        for _, r in enumerate(np.linspace(-1, 1, self.screen_w)):
            point, _ = utils.raycast(char.dire + plane*r, char.pos, self.room_map)
            points.append(point)

        self.view = ViewCollision(
            plane=plane,
            pos=char.pos,
            dire=char.dire,
            points=points
        )

    def render(self):
        if self.view == None:
            return
        
        plane = self.view.plane
        pos = self.view.pos
        cam0 = pos - plane
        cam1 = pos + plane

        for i, point in enumerate(self.view.points):
            # Distance to camera plane (line)
            h = 1/np.linalg.norm(np.cross(cam0-cam1, cam1-point))/np.linalg.norm(cam0-cam1)*self.screen_h
            rect = [i, self.screen_h/2 - h/2, 1, h]
            pygame.draw.rect(self.screen, utils.GREEN, rect, 1)
	