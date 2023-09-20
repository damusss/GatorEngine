import imgui, glm

from gator.entity import Entity
from gator.core.mouse import Mouse

from gator.common.singletons import Singletons
import gator.common.events as events
from gator.common.settings import WINDOW_FLAGS, COLUMN_DIVIDER
from gator.common.gimgui import Tracker


class PropertiesTab:
    def __init__(self):
        self._enityIDBeforePlay: int = None
        self.selectedEntity: Entity = None
        events.register(events.EDITOR_PLAY, self.whenEditorPlay)
        events.register(events.EDITOR_STOP, self.whenEditorStop)
        events.register(events.SCENE_LOADED, self.whenEditorStop)
        events.register(events.ENTITY_KILLED, self.whenEntityKilled)
        
    def whenEntityKilled(self, event):
        if event.entity is self.selectedEntity:
            self.selectedEntity = None
        
    def whenEditorPlay(self, event):
        self._enityIDBeforePlay = self.selectedEntity.ID if self.selectedEntity else None
        
    def whenEditorStop(self, event):
        self.selectedEntity = None
        if self._enityIDBeforePlay is not None:
            entity = Singletons.app.scene.getEntityByID(self._enityIDBeforePlay)
            if entity is not None:
                self.selectedEntity = entity
        
    def setSelected(self, entity: Entity):
        self.selectedEntity = entity
        Singletons.editor.gizmos.setMode(1)
        if Singletons.editor.playing:
            self._enityIDBeforePlay = self.selectedEntity.ID if self.selectedEntity else None
            
    def update(self):
        if not Singletons.editor.gameViewTab.hovered: return
        if Singletons.editor.gizmos.hovering: return
        if Mouse.getButtonDown(Mouse.buttons.MOUSE_BUTTON_LEFT):
            selAny = False
            projected = Singletons.editor.gameViewTab.viewportMouseWorldPos
            if e:= Singletons.app.scene.camera.rayCast(projected):
                self.setSelected(e)
                selAny = True
            if not selAny:
                self.setSelected(None)
        
    def imgui(self):
        imgui.set_next_window_position(0,Tracker.menuBarH)
        imgui.set_next_window_size(Singletons.app.window._width//COLUMN_DIVIDER, (Singletons.app.window._height-Tracker.menuBarH)//2)
        imgui.begin("Entity Properties##EntityPropertiesWindow", False, WINDOW_FLAGS)
        if self.selectedEntity:
            self.selectedEntity.imgui()
        else:
            imgui.text("No entity selected")
        imgui.end()
