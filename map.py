import numpy as np

import utils
import pygame
import pygame.geometry as geo
import character as chr
import math
from datetime import timedelta
from typing import NamedTuple
import textures as txt


class Side(enumerate):
    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3


class WallCollision(NamedTuple):
    side: Side
    position: utils.Vector
    x: int
    collision_tile: tuple[int, int]


class ViewCollision(NamedTuple):
    collisions: list[WallCollision]
    dire: utils.Vector
    pos: utils.Vector
    plane: utils.Vector


class Map:
    def __init__(self, screen: pygame.Surface, room_map, fov):
        self.screen = screen
        self.room_map = room_map
        self.view: ViewCollision | None = None
        self.fov = fov
        self.texture_map: dict[int, txt.Texture] = {
            1: txt.RedCross(),
            2: txt.BlueBricks(),
            3: txt.Green(),
        }
        self.wall_surface_cache = {}

    def update(self, time_delta: timedelta, char: chr.Character):
        plane = utils.normalize(utils.perpendicular(char.dire), math.tan(math.radians(self.fov / 2)))

        collisions: list[WallCollision] = []
        for x, r in enumerate(np.linspace(-1, 1, self.screen.get_width())):
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

            collisions.append(WallCollision(side, point, x, collision_tile))

        self.view = ViewCollision(plane=plane, pos=char.pos, dire=char.dire, collisions=collisions)

    def render(self):
        if self.view is None:
            return

        camera_plane = self.view.plane
        pos = self.view.pos
        cam0 = pos - camera_plane
        cam1 = pos + camera_plane

        blit_seq = []

        # Distance to camera plane (line)
        def distance_to_camera_plane(point):
            return (
                2
                / np.linalg.norm(np.cross(cam0 - cam1, cam1 - point))
                / np.linalg.norm(cam0 - cam1)
                * self.screen.get_height()
            )

        for i, col in enumerate(self.view.collisions):
            if i == len(self.view.collisions) - 1:
                continue

            h0 = distance_to_camera_plane(col.position)
            collision_tile = col.collision_tile
            texture_tile = self.room_map[collision_tile[1]][collision_tile[0]]
            texture = self.texture_map[texture_tile]

            x = self.hit_position(col)
            texture_pos = math.trunc(x * texture.size()[0])
            if col.side in (Side.NORTH, Side.SOUTH):
                tex_surface = texture.darken_val(texture_pos, 0, texture.size()[1], 1)
            else:
                tex_surface = texture.val(texture_pos, 0, texture.size()[1], 1)

            size_to_draw = (1, round(h0))
            key = (size_to_draw, col.side, texture_tile, texture_pos)
            if key not in self.wall_surface_cache:
                self.wall_surface_cache[key] = pygame.transform.scale(tex_surface, size_to_draw)
            blit_seq.append(
                (
                    self.wall_surface_cache[key],
                    (col.x, self.screen.get_height() / 2 - h0 / 2),
                )
            )

        self.screen.blits(blit_seq)

    def hit_position(self, col: WallCollision) -> float:
        match col.side:
            case Side.SOUTH:
                x = col.position[0] - int(col.position[0])
            case Side.NORTH:
                x = 1 - (col.position[0] - int(col.position[0]))
            case Side.EAST:
                x = col.position[1] - int(col.position[1])
            case Side.WEST:
                x = 1 - (col.position[1] - int(col.position[1]))

        if x >= 1:
            x = 0
        return x
