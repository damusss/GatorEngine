import glm
import math

from gator.components.component import Component
import gator.common.saving as saving


class Transform(Component):
    hideInProperties: list[str] = ["active", "rotatedScale"]
    
    def __init__(self, id=None, active=True):
        super().__init__(id, active)
        self.position: glm.vec3 = glm.vec3(0,0,0)
        self.scale: glm.vec2 = glm.vec2(1,1)
        self.rotatedScale: glm.vec2 = glm.vec2(self.scale)
        self.rotation: float = 0

        self._lastPos: glm.vec3 = glm.vec3(self.position)
        self._lastScale: glm.vec2 = glm.vec2(self.scale)
        self._lastRot: float = self.rotation
        
    def toFile(self):
        base = super().toFile()
        base.update({
            "position": saving.saveVec3(self.position),
            "scale": saving.saveVec2(self.scale),
            "rotation": self.rotation
        })
        return base
    
    @classmethod
    def fromFile(cls, cData, entity):
        t = Transform(cData["id"], cData["active"])
        t.position = saving.loadVec3(cData["position"])
        t.scale = saving.loadVec2(cData["scale"])
        t.rotation = cData["rotation"]
        return t

    def update(self):
        self.rotatedScale = glm.rotate(self.scale, math.radians(self.rotation))
        
        if not self.entity._renderbatch: return
        if self._lastPos != self.position or self._lastScale != self.scale or self._lastRot != self.rotation:
            self.entity.dirty = True

            self._lastPos = self.position.xyz
            self._lastScale = self.scale.xy
            self._lastRot = self.rotation
        
    def editorUpdate(self):
        self.update()
