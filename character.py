from typing import NamedTuple
import numpy as np
import utils

class Action(enumerate):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_FORWARD = 2
    MOVE_BACK = 3

class Character:
    
    def __init__(self, pos, dire, room_map):
        self.pos = pos
        self.dire = dire
        self.room_map = room_map

    
    def rotate(self, angle: float):
        self.dire = utils.rotate(self.dire, angle)

    def update(self, action: Action):
        if action == Action.MOVE_LEFT:
            self.rotate(-10)
        elif action == Action.MOVE_RIGHT:
            self.rotate(10)
        elif action == Action.MOVE_FORWARD:
            self.pos += self.dire*0.1
        elif action == Action.MOVE_BACK:
            self.pos -= self.dire*0.1

    def render(self):
        pass