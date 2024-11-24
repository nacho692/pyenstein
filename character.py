import utils
from datetime import timedelta


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

    def update(self, time_delta: timedelta, action: Action):
        # speed is 1 unit per second
        speed = 1 * time_delta.total_seconds()
        # rotation speed is 180 degrees per second
        rotation_speed = 180 * time_delta.total_seconds()

        if action == Action.MOVE_LEFT:
            self.rotate(-rotation_speed)
        elif action == Action.MOVE_RIGHT:
            self.rotate(rotation_speed)
        elif action == Action.MOVE_FORWARD:
            self.pos += self.dire * speed
        elif action == Action.MOVE_BACK:
            self.pos -= self.dire * speed

    def render(self):
        pass
