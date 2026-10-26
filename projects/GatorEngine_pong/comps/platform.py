from gator.components.component import Component
from gator.core.time import Time
import glm, random

class Platform(Component):
    def __init__(self, id=None, active=True):
        super().__init__(id, active)
        
        self.direction = glm.vec3()
        self.speed = 20
        
    def update(self):
        self.entity.transform.position += self.direction*self.speed*Time.dt
        
        if self.entity.transform.position.y - self.entity.transform.scale.y//2 < -4.5:
            self.entity.transform.position.y = -4.5+self.entity.transform.scale.y//2
            
        if self.entity.transform.position.y + self.entity.transform.scale.y//2 > 4.5:
            self.entity.transform.position.y = 4.5-self.entity.transform.scale.y//2