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
