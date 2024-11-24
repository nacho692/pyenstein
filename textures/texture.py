import pygame


class Texture:

    def val(self, x: int, y: int, h: int, w: int) -> pygame.Surface:
        return self.surface.subsurface(x, y, w, h)

    def darken_val(self, x: int, y: int, h: int, w: int) -> pygame.Surface:
        return self.darken_surface.subsurface(x, y, w, h)

    def size(self) -> tuple[int, int]:
        return (self.w, self.h)
