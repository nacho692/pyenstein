import numpy as np
import pygame
import datetime
import math

import pygame.locals as locals

import fps
import utils as u
import character as chr
import map as mp
import minimap as mnp

# This is the map as seen from above, I consider the first block as position
# (x,y) = (0,0)
roomMap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 3, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]


blockSize = 32
screenH = 600
screenW = 800

# PyGame screen
pygame.init()
screen = pygame.display.set_mode((screenW, screenH), flags=0, depth=32)
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


fov = 120
quality = 0.2
rays = math.ceil(screenW * quality)
game_map = mp.Map(screen, screenW, screenH, roomMap, fov, rays)
minimap = mnp.Minimap(screen, screenW - len(roomMap[0]) * 32, 0, len(roomMap[0]), len(roomMap))
wolf_guy = chr.Character(pos, dire, roomMap)

c_fps = fps.FPS()
time_delta = 0
while True:
    frame_start = datetime.datetime.now()

    for event in pygame.event.get():
        if event.type == locals.QUIT:
            pygame.quit()

    pressed = pygame.key.get_pressed()

    if pressed[locals.K_LEFT]:
        wolf_guy.update(time_delta, chr.Action.MOVE_LEFT)
    if pressed[locals.K_RIGHT]:
        wolf_guy.update(time_delta, chr.Action.MOVE_RIGHT)
    if pressed[locals.K_UP]:
        wolf_guy.update(time_delta, chr.Action.MOVE_FORWARD)
    if pressed[locals.K_DOWN]:
        wolf_guy.update(time_delta, chr.Action.MOVE_BACK)

    game_map.update(time_delta, wolf_guy)
    minimap.update(time_delta, game_map)

    screen.fill(BLACK)

    game_map.render()
    wolf_guy.render()
    minimap.render()

    pygame.display.flip()

    time_delta = datetime.datetime.now() - frame_start
    c_fps.update(time_delta)
    pygame.display.set_caption(f"Engine - FPS: {c_fps.get_fps()} - Rays: {rays}")
