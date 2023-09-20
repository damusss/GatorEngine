import glm
import math

from gator.common.singletons import Singletons
from gator.core.mouse import Mouse
from gator.core.time import Time

class EditorCamera:
    def __init__(self):
        self.dragSpeed: float = 0.255
        self.zoomSpeed: float = 2
        self.maxZoom: float = 10
        self.minZoom: float = 0.001

    def update(self):
        if not Singletons.editor.gameViewTab.hovered:
            return
        if Mouse.getButton(Mouse.buttons.MOUSE_BUTTON_MIDDLE):
            worldRel = (Singletons.app.scene.camera.screenToProj(glm.vec3(-Mouse.mouseRel.x,
                                                                          Mouse.mouseRel.y,
                                                                          0))
                        + Singletons.app.scene.camera.projCenter) * glm.normalize(Singletons.app.scene.camera.projSize).yxz

            Singletons.app.scene.camera.position += worldRel * \
                self.dragSpeed*(1/Singletons.app.scene.camera.zoom)
        Singletons.app.scene.camera.zoom += Mouse.scrollDelta.y*Time.dt * \
            math.exp(Singletons.app.scene.camera.zoom)*self.zoomSpeed
        if Singletons.app.scene.camera.zoom > self.maxZoom:
            Singletons.app.scene.camera.zoom = self.maxZoom
        if Singletons.app.scene.camera.zoom < self.minZoom:
            Singletons.app.scene.camera.zoom = self.minZoom
