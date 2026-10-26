from .platform import Platform
from gator.core.time import Time
import glm, random

class Enemy(Platform):
    def __init__(self, id=None, active=True):
        super().__init__(id, active)
        
        self.ball = None
        self.speed = 10
        
    def start(self):
        self.ball = self.entity.scene.getEntityByName("Ball").getComponent("Ball")
        
    def update(self):
        dirDiff = self.ball.entity.transform.position.y-self.entity.transform.position.y
        self.direction.y = 1 if dirDiff > 0 else -1 if dirDiff < 0 else 0
        
        if self.ball.entity.transform.position.x < 0: self.direction.y = 0
        
        super().update()