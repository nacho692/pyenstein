from textures.texture import Texture
import pygame


class RedBricks(Texture):

    def __init__(self) -> None:
        self.h = 64
        self.w = 64
        self.surface = pygame.Surface((self.w, self.h))
        for x in range(self.w):
            for y in range(self.h):
                color = 65536 * 192 * ((x % 16) & (y % 16))
                r = (color >> 16) & 0xFF
                g = (color >> 8) & 0xFF
                b = color & 0xFF
                # self.surface.set_at((x, y), (192, 0, 0))
                self.surface.set_at((x, y), (r, g, b, 255))

        self.darken_surface = self.surface.copy()
        overlay = pygame.Surface(self.darken_surface.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.darken_surface.blit(overlay, (0, 0))
