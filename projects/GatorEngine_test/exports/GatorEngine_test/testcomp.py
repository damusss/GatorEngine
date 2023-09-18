from gator.components.component import Component
from gator.core.time import Time


class TestComp(Component):
    def __init__(self, id: int = None, active: bool = True):
        super().__init__(id, active)
    
    def start(self):
        print("Starting!")
    
    def update(self):
        self.entity.transform.position.x += Time.dt*1