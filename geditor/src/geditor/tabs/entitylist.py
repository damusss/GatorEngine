import imgui
from gator.common.singletons import Singletons


class EntityListTab:
    def __init__(self):
        self.propertiesTab = Singletons.editor.propertiesTab
        
    def imgui(self):
        imgui.begin("Entity List##EntityListTabWindow")
        if imgui.collapsing_header("Active")[0]:
            for entity in Singletons.app.scene.entities:
                if imgui.button(f"{entity.name} ({entity.ID})"):
                    self.propertiesTab.setSelected(entity)
        if imgui.collapsing_header("Inactive")[0]:
            for entity in Singletons.app.scene.inactiveEntities:
                if imgui.button(f"{entity.name} ({entity.ID})"):
                    self.propertiesTab.setSelected(entity)
        imgui.end()