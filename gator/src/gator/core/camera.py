import glm
import math
import typing

from gator.core.mouse import Mouse
from gator.common.singletons import Singletons

if typing.TYPE_CHECKING:
    from gator.entity import Entity

class Camera:
    def __init__(self):
        self.position: glm.vec3 = glm.vec3(0, 0, 0)
        self.zoom: float = 1.0
        self.proj: glm.mat4x4 = glm.ortho(-8, 8, -4.5, 4.5, -100, 100)
        self.inverseProj: glm.mat4x4 = glm.inverse(self.proj)
        self.projSize: glm.vec3 = glm.vec3(16.0, 9.0, 0)
        self.projCenter: glm.vec3 = glm.vec3(16.0/2.0, 9.0/2.0, 0)

        self.view: glm.mat4x4 = glm.translate(glm.mat4(), self.position)
        self.inverseView: glm.mat4x4 = glm.inverse(self.view)
        self.mousePosWorld: glm.vec3 = self.screenToWorld(
            glm.vec3(Mouse.mousePos.x, Mouse.mousePos.y, 0))
        self.mouseRelWorld: glm.vec3 = glm.vec3()

    def update(self):
        self.view = glm.translate(glm.scale(glm.mat4(1.0), glm.vec3(
            self.zoom, self.zoom, 1)), -self.position)
        self.inverseView: glm.mat4x4 = glm.inverse(self.view)
        mousePosWorld = self.screenToWorld(
            glm.vec3(Mouse.mousePos.x, Mouse.mousePos.y, 0))
        self.mouseRelWorld = mousePosWorld-self.mousePosWorld
        self.mousePosWorld = mousePosWorld

    def screenToWorld(self, position: glm.vec3) -> glm.vec3:
        vec = glm.vec4(
            (2*((position.x-0)/(Singletons.app.window._width-0)))-1,
            (2*((position.y-0)/(Singletons.app.window._height-0)))-1,
            0.0, 1.0
        )
        pos = self.inverseProj*self.inverseView*vec
        return glm.vec3(pos.x, pos.y, 0)

    def worldToScreen(self, position: glm.vec2 | glm.vec2) -> glm.vec3:
        ndcSpacePos = glm.vec4(position.x, position.y, 0, 1)
        ndcSpacePos = self.view * self.proj * ndcSpacePos
        windowSpace = glm.vec2(
            ndcSpacePos.x, ndcSpacePos.y)*(1 / ndcSpacePos.w)
        windowSpace += glm.vec2(1, 1)
        windowSpace *= 0.5
        windowSpace *= glm.vec2(Singletons.app.window._width,
                                Singletons.app.window._height)

        return windowSpace

    def screenToProj(self, position: glm.vec3) -> glm.vec3:
        vec = glm.vec4(
            (2*((position.x-0)/(Singletons.app.window._width-0)))-1,
            (2*((position.y-0)/(Singletons.app.window._height-0)))-1,
            0,
            1.0
        )
        pos = self.inverseProj*vec
        pos.z = 0
        return glm.vec3(pos.x, pos.y, pos.z)
    
    def rayCast(self, position: glm.vec3, layers: list[int]|None = None) -> "Entity":
        if layers:
            for layer in layers:
                for entity in sorted(Singletons.app.scene._entityLayerCache[layer], key=lambda e: -e.transform.position.z):
                    if abs(position.x-entity.transform.position.x) <= abs(entity.transform.rotatedScale.x)/2 and abs(position.y-entity.transform.position.y) <= abs(entity.transform.rotatedScale.y)/2:
                        return entity
            return None
        for entity in sorted(Singletons.app.scene.entities, key=lambda e: -e.transform.position.z):
            if abs(position.x-entity.transform.position.x) <= abs(entity.transform.rotatedScale.x)/2 and abs(position.y-entity.transform.position.y) <= abs(entity.transform.rotatedScale.y)/2:
                return entity
        return None
    
    def rayCastAll(self, position: glm.vec3, layers: list[int]|None = None) -> list["Entity"]:
        entities = []
        if layers:
            for layer in layers:
                for entity in sorted(Singletons.app.scene._entityLayerCache[layer], key=lambda e: -e.transform.position.z):
                    if abs(position.x-entity.transform.position.x) <= abs(entity.transform.rotatedScale.x)/2 and abs(position.y-entity.transform.position.y) <= abs(entity.transform.rotatedScale.y)/2:
                        entities.append(entity)
            return entities
        for entity in sorted(Singletons.app.scene.entities, key=lambda e: -e.transform.position.z):
            if abs(position.x-entity.transform.position.x) <= abs(entity.transform.rotatedScale.x)/2 and abs(position.y-entity.transform.position.y) <= abs(entity.transform.rotatedScale.y)/2:
                entities.append(entity)
        return entities
    
    def singleRayCast(self, position: glm.vec3, entity: "Entity") -> bool:
        return abs(position.x-entity.transform.position.x) <= abs(entity.transform.scale.x)/2 and abs(position.y-entity.transform.position.y) <= abs(entity.transform.scale.y)/2

    def rawRayCast(self, rayPosition: glm.vec3, objPosition: glm.vec3, objScale: glm.vec2, objRotation: float) -> bool:
        objScale = glm.rotate(objScale, math.radians(objRotation))
        return abs(rayPosition.x-objPosition.x) <= abs(objScale.x)/2 and abs(rayPosition.y-objPosition.y) <= abs(objScale.y)/2