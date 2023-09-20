import imgui

from gator.common.singletons import Singletons
from gator.components.spriterenderer import SpriteRenderer
from gator.resources.sprite import Sprite
from gator.common.settings import WINDOW_FLAGS, COLUMN_DIVIDER
from gator.common.gimgui import Tracker


class EntityListTab:
    def __init__(self):
        self.propertiesTab = Singletons.editor.propertiesTab
        
    def imgui(self):
        imgui.set_next_window_position(0, (Singletons.app.window._height-Tracker.menuBarH)//2+Tracker.menuBarH)
        imgui.set_next_window_size(Singletons.app.window._width//COLUMN_DIVIDER, (Singletons.app.window._height-Tracker.menuBarH)//2)
        
        imgui.begin("Entities##EntityListTabWindow", False, WINDOW_FLAGS)
        
        if imgui.collapsing_header("Active")[0]:
            for entity in Singletons.app.scene.entities:
                if imgui.button(f"{entity.name} ({entity.ID})"):
                    if entity is self.propertiesTab.selectedEntity:
                        self.propertiesTab.setSelected(None)
                    else:
                        self.propertiesTab.setSelected(entity)
        if imgui.collapsing_header("Inactive")[0]:
            for entity in Singletons.app.scene.inactiveEntities:
                if imgui.button(f"{entity.name} ({entity.ID})"):
                    if entity is self.propertiesTab.selectedEntity:
                        self.propertiesTab.setSelected(None)
                    else:
                        self.propertiesTab.setSelected(entity)
        if imgui.begin_popup_context_window("Entity List Options"):
            if imgui.menu_item("New Entity")[0]:
                entity = Singletons.app.scene.instantiate("New Entity", 0)
                self.propertiesTab.setSelected(entity)
            if imgui.menu_item("New Sprite Entity")[0]:
                entity = Singletons.app.scene.instantiate("New Sprite Entity", 0)
                entity.addComponent(SpriteRenderer(Sprite(None)))
                self.propertiesTab.setSelected(entity)
            imgui.end_popup()
            
        imgui.end()