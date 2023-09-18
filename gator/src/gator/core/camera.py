import glm
from gator.core.mouse import Mouse
from gator.common.singletons import Singletons

class Camera:
    def __init__(self):
        self.position: glm.vec3 = glm.vec3(0, 0, 0)
        self.zoom: float = 1.0
        self.proj: glm.mat4x4 = glm.ortho(-8, 8, -4.5, 4.5, -100, 100)
        self.inverseProj = glm.inverse(self.proj)
        self.projSize = glm.vec3(16.0, 9.0, 0)
        self.projCenter = glm.vec3(16.0/2.0, 9.0/2.0, 0)
        
        self.view: glm.mat4x4 = glm.translate(glm.mat4(), self.position)
        self.inverseView: glm.mat4x4 = glm.inverse(self.view)
        self.mousePosWorld = self.screenToWorld(glm.vec3(Mouse.mousePos.x, Mouse.mousePos.y, 0))

    def update(self):
        self.view = glm.translate(glm.scale(glm.mat4(1.0), glm.vec3(
            self.zoom, self.zoom, 1)), self.position)
        self.inverseView: glm.mat4x4 = glm.inverse(self.view)
        self.mousePosWorld = self.screenToWorld(glm.vec3(Mouse.mousePos.x, Mouse.mousePos.y, 0))
        
    def screenToWorld(self, position: glm.vec3):
        vec = glm.vec4(
            (2*((position.x-0)/(Singletons.app.window._width-0)))-1,
            (2*((position.y-0)/(Singletons.app.window._height-0)))-1,
            0,
            1.0
        )
        #pos = vec * self.inverseViewProj
        pos = self.inverseView*self.inverseProj*vec
        #if pos.w == 0: pos.w = 1
        #pos.w = 1/pos.w
        #pos.x *= pos.w
        #pos.y *= pos.w
        pos.z = 0
        return glm.vec3(pos.x, pos.y, pos.z)
    
    def worldToScreen(self, position):
        ndcSpacePos = glm.vec4(position.x, position.y, 0, 1)
        ndcSpacePos = self.view * self.proj * ndcSpacePos
        windowSpace = glm.vec2(ndcSpacePos.x, ndcSpacePos.y)*(1 / ndcSpacePos.w)
        windowSpace += glm.vec2(1, 1)
        windowSpace *= 0.5
        windowSpace *= glm.vec2(Singletons.app.window._width, Singletons.app.window._height)

        return windowSpace
    
    
    def screenToProj(self, position: glm.vec3):
        vec = glm.vec4(
            (2*((position.x-0)/(Singletons.app.window._width-0)))-1,
            (2*((position.y-0)/(Singletons.app.window._height-0)))-1,
            0,
            1.0
        )
        pos = self.inverseProj*vec
        #if pos.w == 0: pos.w = 1
        #pos.w = 1/pos.w
        #pos.x *= pos.w
        #pos.y *= pos.w
        pos.z = 0
        return glm.vec3(pos.x, pos.y, pos.z)
