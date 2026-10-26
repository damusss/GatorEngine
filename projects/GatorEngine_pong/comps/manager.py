from gator.components.component import Component
from gator.core.time import Time
import glm, random

class Manager(Component):
    def __init__(self, id=None, active=True):
        super().__init__(id, active)
        
        self.playerScore = 0
        self.enemyScore = 0
        
    def leftCollide(self, ball):
        self.enemyScore += 1
        self.collided(ball)
        
    def rightCollide(self, ball):
        self.playerScore += 1
        self.collided(ball)
        
    def collided(self, ball):
        ball.entity.transform.position = glm.vec3()
        ball.startDir()