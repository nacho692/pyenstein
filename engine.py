import numpy as np
import pygame
import datetime
import fps
import pygame.locals as locals

# import fps
import utils as u
import character as chr
import map as mp
import minimap as mnp
import options as opt


class Engine:
    def __init__(self, options: opt.Options):
        self.options = options

    def run(self):
        # PyGame screen
        pygame.init()
        screen = pygame.display.set_mode((opts.screen_w, opts.screen_h), flags=pygame.RESIZABLE, depth=32)
        pygame.display.set_caption("Engine")

        # Starting position
        pos = np.array([1.5, 1.5])

        # Looking right
        dire = np.array([0.0, -1.0])
        dire = u.normalize(dire, 1)

        # Plane
        plane = u.perpendicular(dire)
        plane = u.normalize(plane, 1)

        drawing_canvas = pygame.Surface((opts.internal_screen_w, opts.internal_screen_h))
        game_map = mp.Map(drawing_canvas, roomMap, fov=opts.fov)
        minimap = mnp.Minimap(screen, len(roomMap[0]), len(roomMap))
        wolf_guy = chr.Character(pos, dire, roomMap)

        c_fps = fps.FPS()
        time_delta = datetime.timedelta(seconds=0)
        while True:
            frame_start = datetime.datetime.now()

            for event in pygame.event.get():
                if event.type == locals.QUIT:
                    pygame.quit()
                    exit(0)

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
            c_fps.update(time_delta)

            drawing_canvas.fill(u.BLACK)

            game_map.render()
            wolf_guy.render()
            screen.blit(pygame.transform.scale(drawing_canvas, screen.get_size()))
            minimap.render()

            pygame.display.flip()
            time_delta = datetime.datetime.now() - frame_start

            pygame.display.set_caption(f"Engine - FPS: {c_fps.get_fps()}")


# This is the map as seen from above, I consider the first block as position
# (x,y) = (0,0)
roomMap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 3, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]

if __name__ == "__main__":
    opts = opt.Options()
    engine = Engine(opts)
    engine.run()
