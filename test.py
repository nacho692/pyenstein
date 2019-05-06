import sys
import pygame

pygame.init()

size = 320, 240
black = 0, 0, 0
red = 255, 0, 0

screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    # Either of the following works.  Without the fourth argument,
    # the rectangle is filled.
    pygame.draw.rect(screen, red, (10,10,50,50))
    #pygame.draw.rect(screen, red, (10,10,50,50), 1)
    pygame.display.flip()