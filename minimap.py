import pygame
import utils
import map as mp
from datetime import timedelta


class Minimap:

    def __init__(self, screen: pygame.Surface, map_w, map_h):
        self.screen = screen
        self.block_size = 32
        self.pos_x = screen.get_width() - map_w * self.block_size
        self.pos_y = 0
        self.map_w = map_w
        self.map_h = map_h
        self.view: mp.ViewCollision | None = None

    def draw_grid(self):
        for i in range(1, self.map_w):
            from_point = (self.pos_x + i * self.block_size, self.pos_y)
            to_point = (
                i * self.block_size + self.pos_x,
                self.pos_y + self.map_h * self.block_size,
            )
            pygame.draw.line(self.screen, utils.RED, from_point, to_point, 1)

        for j in range(1, self.map_h):
            from_point = (self.pos_x, self.pos_y + j * self.block_size)
            to_point = (self.pos_x + self.map_w * self.block_size, j * self.block_size)
            pygame.draw.line(self.screen, utils.RED, from_point, to_point, 1)

    def draw_player(self, pos):
        pygame.draw.circle(
            self.screen,
            utils.GREEN,
            (
                self.pos_x + int(pos[0] * self.block_size),
                self.pos_y + int(pos[1] * self.block_size),
            ),
            1,
        )

    def draw_ray(self, pos: utils.Vector, point, color=utils.RED):
        from_point = (
            self.pos_x + int(pos[0] * self.block_size),
            self.pos_y + int(pos[1] * self.block_size),
        )
        to_point = (
            self.pos_x + int(point[0] * self.block_size),
            self.pos_y + int(point[1] * self.block_size),
        )
        pygame.draw.line(self.screen, color, from_point, to_point, 1)

    def update(self, time_delta: timedelta, game_map: mp.Map):
        self.view = game_map.view
        self.pos_x = self.screen.get_width() - self.map_w * self.block_size
        self.pos_y = 0

    def render(self):
        self.draw_grid()
        if self.view is not None:
            self.draw_player(self.view.pos)
            # for collision in self.view.collisions:
            #     self.draw_ray(self.view.pos, collision.position)
            # for ray in self.view.floor_rays:
            #     self.draw_ray(ray.left_collision, ray.right_collision, utils.GREEN)
            self.draw_ray(
                self.view.dire + self.view.pos - self.view.plane,
                self.view.dire + self.view.pos + self.view.plane,
                utils.BLUE,
            )
