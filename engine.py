import numpy as np
import pygame

import pygame.locals as locals

import utils as u
import character as chr
import map as mp
import minimap as mnp

# This is the map as seen from above, I consider the first block as position
# (x,y) = (0,0)
roomMap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]


blockSize = 32
screenH = 600
screenW = 800

# PyGame screen
pygame.init()
screen = pygame.display.set_mode((screenW, screenH), 0, 32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
pygame.display.set_caption("Engine")

# Starting position
pos = np.array([1.5, 1.5])

# Looking right
dire = np.array([0.0, -1.0])
dire = u.normalize(dire, 1)

# Plane
plane = u.perpendicular(dire)
plane = u.normalize(plane, 1)


game_map = mp.Map(screen, screenW, screenH, roomMap)
minimap = mnp.Minimap(screen, screenW - len(roomMap[0]) * 32, 0, len(roomMap[0]), len(roomMap))
wolf_guy = chr.Character(pos, dire, roomMap)

time_delta = 0
while True:
    frame_start = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == locals.QUIT:
            pygame.quit()

    pressed = pygame.key.get_pressed()

    if pressed[locals.K_LEFT]:
        wolf_guy.update(chr.Action.MOVE_LEFT)
    if pressed[locals.K_RIGHT]:
        wolf_guy.update(chr.Action.MOVE_RIGHT)
    if pressed[locals.K_UP]:
        wolf_guy.update(chr.Action.MOVE_FORWARD)
    if pressed[locals.K_DOWN]:
        wolf_guy.update(chr.Action.MOVE_BACK)

    game_map.update(wolf_guy)
    minimap.update(game_map)

    screen.fill(BLACK)

    game_map.render()
    wolf_guy.render()
    minimap.render()

    pygame.display.update()

    time_delta = pygame.time.get_ticks() - frame_start
