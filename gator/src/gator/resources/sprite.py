import glm
from gator.resources.texture import Texture


class Sprite:
    DEFAULT_TEX_COORDS: list[glm.vec2] = [
        glm.vec2(1.0, 1.0,),
        glm.vec2(1.0, 0.0,),
        glm.vec2(0.0, 0.0,),
        glm.vec2(0.0, 1.0,),
    ]

    def __init__(self, texture: Texture | None = None, texCoords: list[glm.vec2] = DEFAULT_TEX_COORDS):
        self.texture: Texture = texture
        self.texCoords: glm.vec2 = texCoords
        
    def calcGridSheetCords(self, w, h, i):
        if self.texture is None: return
        if w==0 or h==0: return
        if w >= self.texture.width or h >= self.texture.height: self.texCoords = self.DEFAULT_TEX_COORDS
        
        idx = 0
        cx = 0
        cy = 0
        while idx < 10000:
            if idx == i:
                l, t, r, b = cx/self.texture.width, cy/self.texture.height, (cx+w)/self.texture.width, (cy+h)/self.texture.height
                self.texCoords = [
                    glm.vec2(r, t),
                    glm.vec2(r, b),
                    glm.vec2(l, b),
                    glm.vec2(l, t)
                ]
                return
            cx += w
            if cx >= self.texture.width:
                cx = 0
                cy += h
            if cy >= self.texture.height:
                self.texCoords = self.DEFAULT_TEX_COORDS
                return
            idx += 1
            
    def calcOffsetheetCords(self, w, h, ox, oy):
        if self.texture is None: return
        if w==0 or h==0: return
        
        l, t, r, b = ox/self.texture.width, oy/self.texture.height, (ox+w)/self.texture.width, (oy+h)/self.texture.height
        self.texCoords = [
                glm.vec2(r, t),
                glm.vec2(r, b),
                glm.vec2(l, b),
                glm.vec2(l, t)
            ]
