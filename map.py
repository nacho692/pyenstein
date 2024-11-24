import numpy as np
import utils
import pygame
import character as chr
from typing import NamedTuple


class Side(enumerate):
    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3


class WallCollision(NamedTuple):
    side: Side
    position: np.array


class ViewCollision(NamedTuple):
    collisions: list[WallCollision]
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
        collisions: list[WallCollision] = []
        for _, r in enumerate(np.linspace(-1, 1, self.screen_w)):
            point, collision_side = utils.raycast(char.dire + plane * r, char.pos, self.room_map)

            side = Side.WEST
            if collision_side == "x":
                if char.pos[0] - point[0] > 0:
                    side = Side.WEST
                else:
                    side = Side.EAST
            elif collision_side == "y":
                if char.pos[1] - point[1] > 0:
                    side = Side.SOUTH
                else:
                    side = Side.NORTH

            collisions.append(WallCollision(side, point))

        self.view = ViewCollision(plane=plane, pos=char.pos, dire=char.dire, collisions=collisions)

    def render(self):
        if self.view is None:
            return

        plane = self.view.plane
        pos = self.view.pos
        cam0 = pos - plane
        cam1 = pos + plane

        for i, col in enumerate(self.view.collisions):

            # Distance to camera plane (line)
            h = (
                1
                / np.linalg.norm(np.cross(cam0 - cam1, cam1 - col.position))
                / np.linalg.norm(cam0 - cam1)
                * self.screen_h
            )
            rect = [i, self.screen_h / 2 - h / 2, 1, h]
            color = utils.DARK_RED
            if col.side == Side.WEST:
                color = utils.GREEN
            elif col.side == Side.EAST:
                color = utils.RED
            elif col.side == Side.NORTH:
                color = utils.DARK_GREEN

            pygame.draw.rect(self.screen, color=color, rect=rect, width=1)
