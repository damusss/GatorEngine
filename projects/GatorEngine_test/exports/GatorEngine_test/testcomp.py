from gator.components.component import Component
from gator.core.time import Time


class TestComp(Component):
    hideInProperties = ["randomList"]
    
    def __init__(self, id: int = None, active: bool = True):
        super().__init__(id, active)
        
        self.randomList = [1,2,3,"hello"]
    
    def start(self):
        print("Starting!")
    
    def update(self):
        self.entity.transform.position.x += Time.dt*1
        
    def editorUpdate(self):
        return super().editorUpdate()