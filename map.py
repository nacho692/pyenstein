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
    side: Side | int
    position: utils.Vector
    x: int
    collision_tile: tuple[int, int]


class FloorCollision(NamedTuple):
    left_collision: utils.Vector
    right_collision: utils.Vector
    horizontal_distance: float
    y: int


class ViewCollision(NamedTuple):
    collisions: list[WallCollision]
    floor_rays: list[FloorCollision]
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
            -1: txt.GreenBricks(),
            0: txt.Gray(),
            1: txt.RedCross(),
            2: txt.BlueBricks(),
            3: txt.Green(),
        }
        self.wall_surface_cache = {}

    def update(self, time_delta: timedelta, char: chr.Character):
        plane = utils.normalize(utils.perpendicular(char.dire), math.tan(math.radians(self.fov / 2)))

        floor_rays = []
        poz = self.screen.get_height() // 2
        for y in range(self.screen.get_height() // 2 + 1, self.screen.get_height()):
            p = y - poz
            hdist = poz / p
            hit0 = char.pos + char.dire * hdist - plane * hdist
            hit1 = char.pos + char.dire * hdist + plane * hdist
            floor_rays.append(FloorCollision(hit0, hit1, hdist, y=y))

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

        self.view = ViewCollision(
            plane=plane, floor_rays=floor_rays, pos=char.pos, dire=char.dire, collisions=collisions
        )

    def render(self):
        if self.view is None:
            return

        camera_plane = self.view.plane
        pos = self.view.pos
        cam0 = pos - camera_plane / 2
        cam1 = pos + camera_plane / 2

        blit_seq = []
        px_array = pygame.pixelarray.PixelArray(self.screen)
        for _, fc in enumerate(self.view.floor_rays):
            step = (fc.right_collision - fc.left_collision) / self.screen.get_width()
            floor_pos = fc.left_collision - step
            for x in range(0, self.screen.get_width(), 1):
                floor_pos = floor_pos + step
                tile = (math.trunc(floor_pos[0]), math.trunc(floor_pos[1]))
                if floor_pos[1] < 0 or floor_pos[1] >= len(self.room_map):
                    continue
                if floor_pos[0] < 0 or floor_pos[0] >= len(self.room_map[tile[1]]):
                    continue

                texture_tile = self.room_map[tile[1]][tile[0]]
                texture = self.texture_map[texture_tile]
                if texture_tile > 0:
                    continue

                texture_pos = floor_pos - tile
                tex_surface = texture.val(texture_pos[0] * texture.size()[0], texture_pos[1] * texture.size()[1], 1, 1)
                px_array[x, fc.y] = tex_surface.get_at((0, 0))

        px_array.close()
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (0, self.screen.get_height() // 2),
            (self.screen.get_width(), self.screen.get_height() // 2),
            3,
        )

        # Distance to camera plane (line)
        def distance_to_camera_plane(point):
            return float(
                self.screen.get_height()
                / np.linalg.norm(np.cross(cam0 - cam1, cam1 - point))
                / np.linalg.norm(cam0 - cam1)
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

            draw_start = max(self.screen.get_height() / 2 - h0 / 2, 0.0)
            draw_end = min(self.screen.get_height() / 2 + h0 / 2, self.screen.get_height())
            size_to_draw = (1, draw_end - draw_start)
            key = (size_to_draw, col.side, texture_tile, texture_pos)
            if key not in self.wall_surface_cache:
                self.wall_surface_cache[key] = pygame.transform.scale(tex_surface, size=size_to_draw)
            blit_seq.append(
                (
                    self.wall_surface_cache[key],
                    (col.x, draw_start),
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
