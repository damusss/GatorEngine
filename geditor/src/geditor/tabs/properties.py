import imgui
from gator.common.singletons import Singletons
from gator.entity import Entity


class PropertiesTab:
    def __init__(self):
        self.selectedEntity: Entity = None
        
    def imgui(self):
        if not self.selectedEntity and len(Singletons.app.scene.entities) > 0:
            self.selectedEntity = Singletons.app.scene.entities[0]
        imgui.begin("Entity Properties##EntityPropertiesWindow")
        if self.selectedEntity:
            self.selectedEntity.imgui()
        else:
            imgui.text("No entity selected")
        imgui.end()
