import imgui, glm
from gator.common.singletons import Singletons
from gator.entity import Entity

# temp
import gator.common.events as events


class PropertiesTab:
    def __init__(self):
        self._enityIDBeforePlay = None
        self.selectedEntity: Entity = None
        events.register(events.EDITOR_PLAY, self.whenEditorPlay)
        events.register(events.EDITOR_STOP, self.whenEditorStop)
        
    def whenEditorPlay(self, event):
        self._enityIDBeforePlay = self.selectedEntity.ID if self.selectedEntity else None
        
    def whenEditorStop(self, event):
        self.selectedEntity = None
        if self._enityIDBeforePlay is not None:
            entity = Singletons.app.scene.getEntityByID(self._enityIDBeforePlay)
            if entity is not None:
                self.selectedEntity = entity
        
    def setSelected(self, entity):
        self.selectedEntity = entity
        if Singletons.editor.playing:
            self._enityIDBeforePlay = self.selectedEntity.ID if self.selectedEntity else None
        
    def imgui(self):
        imgui.begin("Entity Properties##EntityPropertiesWindow")
        if self.selectedEntity:
            self.selectedEntity.imgui()
            if Singletons.editor.gameViewTab.hovered:
                vmwp = Singletons.editor.gameViewTab.viewportMouseWorldPos-Singletons.app.scene.camera.position
                self.selectedEntity.transform.position = glm.vec3(vmwp.x, vmwp.y, 0)
        else:
            imgui.text("No entity selected")
        imgui.end()
