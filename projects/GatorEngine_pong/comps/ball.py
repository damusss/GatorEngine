from gator.components.component import Component
from gator.core.time import Time
import glm, random

class Ball(Component):
    hideInProperties = ["direction"]
    
    def __init__(self, id=None, active=True):
        super().__init__(id, active)
        
        self.direction = glm.vec3()
        self.speed = 200
        self.startDir()
        
        self.manager = None
        self.player = None
        self.enemy = None
        
    def start(self):
        self.manager = self.entity.scene.getEntityByName("Manager").getComponent("Manager")
        self.player = self.entity.scene.getEntityByName("Player").getComponent("Player")
        self.enemy = self.entity.scene.getEntityByName("Enemy").getComponent("Enemy")
    
    def toFile(self):
        base = super().toFile()
        base.update({
            "speed": self.speed
        })
        return base
    
    @classmethod
    def fromFile(cls, cData: dict, entity):
        ball = super().fromFile(cData, entity)
        ball.speed = cData["speed"]
        return ball
    
    def startDir(self):
        self.direction = glm.vec3(random.choice([1,-1]), random.choice([1,-1]), 0)
        
    def update(self):
        self.entity.transform.position += self.direction*self.speed*Time.dt
        
        if self.entity.transform.position.y - self.entity.transform.scale.y//2 < -4.5 or \
            self.entity.transform.position.y + self.entity.transform.scale.y//2 > 4.5:
            self.direction.y *= -1
            
        if self.entity.transform.position.x - self.entity.transform.scale.x//2 < -8:
            self.manager.leftCollide(self)
        if self.entity.transform.position.x + self.entity.transform.scale.x//2 > 8:
            self.manager.rightCollide(self)