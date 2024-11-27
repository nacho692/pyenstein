import numpy as np
import utils
import pygame
import character as chr
import math
from datetime import timedelta
from typing import NamedTuple
from textures import red_bricks, blue_bricks, green_bricks, green, texture


class Side(enumerate):
    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3


class WallCollision(NamedTuple):
    side: Side
    position: np.array
    x: int
    collision_tile: tuple[int, int]


class ViewCollision(NamedTuple):
    collisions: list[WallCollision]
    dire: np.array
    pos: np.array
    plane: np.array


class Map:
    def __init__(self, screen: pygame.Surface, screen_w, screen_h, room_map, fov, rays: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen = screen
        self.room_map = room_map
        self.view: ViewCollision | None = None
        self.fov = fov
        self.rays = rays
        self.texture_map: dict[int, texture.Texture] = {
            1: green.Green(),
            2: green_bricks.GreenBricks(),
            3: blue_bricks.BlueBricks(),
        }

    def update(self, time_delta: timedelta, char: chr.Character):
        plane = utils.normalize(utils.perpendicular(char.dire), math.tan(math.radians(self.fov / 2)))

        collisions: list[WallCollision] = []
        size = math.ceil(self.screen_w / self.rays)
        for x, r in enumerate(np.linspace(-1, 1, self.rays)):
            point, collision_side, collision_tile = utils.raycast(char.dire + plane * r, char.pos, self.room_map)
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

            collisions.append(WallCollision(side, point, x * size, collision_tile))

        self.view = ViewCollision(plane=plane, pos=char.pos, dire=char.dire, collisions=collisions)

    def render(self):
        if self.view is None:
            return

        plane = self.view.plane
        pos = self.view.pos
        cam0 = pos - plane
        cam1 = pos + plane

        blit_seq = []
        size = math.ceil(self.screen_w / self.rays)
        for col in self.view.collisions:

            # Distance to camera plane (line)
            h = (
                1
                / np.linalg.norm(np.cross(cam0 - cam1, cam1 - col.position))
                / np.linalg.norm(cam0 - cam1)
                * self.screen_h
            )

            collision_tile = col.collision_tile
            texture_tile = self.room_map[collision_tile[1]][collision_tile[0]]
            x, y = col.position - collision_tile
            if x == 1:
                x = 0
            if y == 1:
                y = 0

            texture = self.texture_map[texture_tile]
            if col.side in (Side.NORTH, Side.SOUTH):
                tex_surface = texture.darken_val(x * texture.size()[0], 0, texture.size()[1], 1)
            else:
                tex_surface = texture.val(y * texture.size()[0], 0, texture.size()[1], 1)

            blit_seq.append((pygame.transform.scale(tex_surface, (size, h)), (col.x, self.screen_h / 2 - h / 2)))
        self.screen.blits(blit_seq)
