from .platform import Platform
from gator.core.time import Time
from gator.core.keys import Keyboard
import glm, random

class Player(Platform):
    def __init__(self, id=None, active=True):
        super().__init__(id, active)
        
    def update(self):
        self.direction.y = 1 if Keyboard.getKey(Keyboard.keys.KEY_W) else -1 if Keyboard.getKey(Keyboard.keys.KEY_S) else 0
        
        super().update()