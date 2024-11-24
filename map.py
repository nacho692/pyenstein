import numpy as np
import utils
import pygame
import character as chr
import math
from typing import NamedTuple
import textures.base_texture as txt


class Side(enumerate):
    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3


class WallCollision(NamedTuple):
    side: Side
    position: np.array
    x: int


class ViewCollision(NamedTuple):
    collisions: list[WallCollision]
    dire: np.array
    pos: np.array
    plane: np.array


class Map:
    def __init__(self, screen: pygame.Surface, screen_w, screen_h, room_map):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen = screen
        self.room_map = room_map
        self.view: ViewCollision | None = None
        self.texture = txt.Texture()

    def update(self, char: chr.Character):
        plane = utils.normalize(utils.perpendicular(char.dire), 1)
        collisions: list[WallCollision] = []
        for x, r in enumerate(np.linspace(-1, 1, self.screen_w)):
            point, collision_side = utils.raycast(char.dire + plane * r, char.pos, self.room_map)
            if point is None:
                continue

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

            collisions.append(WallCollision(side, point, x))

        self.view = ViewCollision(plane=plane, pos=char.pos, dire=char.dire, collisions=collisions)

    def render(self):
        if self.view is None:
            return

        plane = self.view.plane
        pos = self.view.pos
        cam0 = pos - plane
        cam1 = pos + plane

        blit_seq = []
        for col in self.view.collisions:

            # Distance to camera plane (line)
            h = (
                1
                / np.linalg.norm(np.cross(cam0 - cam1, cam1 - col.position))
                / np.linalg.norm(cam0 - cam1)
                * self.screen_h
            )
            # rect = [i, self.screen_h / 2 - h / 2, 1, h]

            # color = utils.DARK_RED
            # if col.side == Side.WEST:
            #     color = utils.GREEN
            # elif col.side == Side.EAST:
            #     color = utils.RED
            # elif col.side == Side.NORTH:
            #     color = utils.DARK_GREEN

            collision_tile = list(map(math.ceil, col.position - (1.0, 1.0)))
            x, y = col.position - collision_tile
            if x == 1:
                x = 0
            if y == 1:
                y = 0
            if col.side in (Side.NORTH, Side.SOUTH):
                tex_surface = self.texture.darken_val(x * self.texture.size()[0], 0, self.texture.size()[1], 1)
            else:
                tex_surface = self.texture.val(y * self.texture.size()[0], 0, self.texture.size()[1], 1)

            blit_seq.append((pygame.transform.scale(tex_surface, (1, h)), (col.x, self.screen_h / 2 - h / 2)))
            # pygame.draw.rect(self.screen, color=color, rect=rect, width=1)

        self.screen.blits(blit_seq)
