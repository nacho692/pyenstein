from textures.texture import Texture
import pygame
import utils


class Green(Texture):

    def __init__(self) -> None:
        self.h = 64
        self.w = 64
        self.surface = pygame.Surface((self.w, self.h))
        for x in range(self.w):
            for y in range(self.h):
                self.surface.set_at((x, y), utils.GREEN)

        self.darken_surface = self.surface.copy()
        overlay = pygame.Surface(self.darken_surface.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.darken_surface.blit(overlay, (0, 0))
