from typing import NamedTuple
import numpy as np

class ViewCollision(NamedTuple):
    points: list[np.array]

class Character:
    
    def __init__(self, pos, dire):
        self.pos = pos
        self.dire = dire
    