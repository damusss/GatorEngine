import glm
import math

from gator.common.singletons import Singletons

from gator.graphics.mesh import IndexedVertexMesh
from gator.graphics.shader import Shader

from gator.resources.texture import Texture
from gator.core.camera import Camera
from gator.components.spriterenderer import SpriteRenderer


class RenderBatch:
    VERTEX_SIZE: int = 10

    def __init__(self, maxSprites: int, maxTexures: int, meshConfig: list[int, str, list[int], bool, list[float] | None, str, list[int]]):
        self.maxSprites: int = maxSprites
        self.maxTextures: int = maxTexures
        self.meshConfig: list[int, str, list[int], bool,
                              list[float] | None, str, list[int]] = meshConfig
        self.camera: Camera = Singletons.app.scene.camera
        self.sprites: list[SpriteRenderer] = []
        self.vertices: list[float] = [
            0 for i in range(self.maxSprites*4*self.VERTEX_SIZE)]
        self.textures: list[Texture] = []
        self.mesh: IndexedVertexMesh = IndexedVertexMesh(*self.meshConfig)
        self.rebufferData: bool = False

    def reset(self):
        self.vertices: list[float] = [0 for i in range(self.maxSprites*4*self.VERTEX_SIZE)]
        self.sprites = []
        self.textures = []

    def render(self, shader: Shader):
        shader.uniformMat4F("uProj", self.camera.proj)
        shader.uniformMat4F("uView", self.camera.view)
        shader.uniformIntArray("uTextures", list(range(8)))
        for i, texture in enumerate(self.textures):
            texture.bind(i)

        self.mesh.render(
            (self.vertices if self.rebufferData else None), 0, len(self.sprites)*6)
        if self.rebufferData:
            self.rebufferData = False

        for texture in self.textures:
            texture.unbind()

    def spriteUpdated(self, sprite: SpriteRenderer):
        if sprite.sprite.texture is None:
            return
        self.tryRemove(sprite)
        Singletons.app.scene.renderer.addComponent(sprite)

    def add(self, sprite: SpriteRenderer):
        index = len(self.sprites)
        self.sprites.append(sprite)
        sprite.entity._renderbatch = self
        sprite.entity._batchindex = index

        if sprite.sprite.texture is not None:
            if sprite.sprite.texture not in self.textures:
                self.textures.append(sprite.sprite.texture)

        self.loadVertexProperties(index)

    def loadVertexProperties(self, index: int):
        self.rebufferData = True
        sprite = self.sprites[index]
        transform = sprite.entity.transform
        offset = index*4*self.VERTEX_SIZE

        texID = -1
        if sprite.sprite.texture is not None:
            for i, texture in enumerate(self.textures):
                if texture == sprite.sprite.texture:
                    texID = i
                    break

        rotated = transform.rotation != 0.0
        if rotated:
            transformMatrix = glm.identity(glm.mat4x4)
            transformMatrix = glm.translate(
                transformMatrix, transform.position)
            transformMatrix = glm.rotate(transformMatrix, float(
                math.radians(transform.rotation)), glm.vec3(0, 0, 1))
            transformMatrix = glm.scale(transformMatrix, glm.vec3(
                transform.scale.x, transform.scale.y, 1))

        xAdd = yAdd = 0.5
        for i in range(4):
            if i == 1:
                yAdd = -0.5
            elif i == 2:
                xAdd = -0.5
            elif (i == 3):
                yAdd = 0.5

            if rotated:
                currentPos = (transformMatrix)*glm.vec4(xAdd, yAdd, 1, 1)
                self.vertices[offset] = currentPos.x
                self.vertices[offset + 1] = currentPos.y
                self.vertices[offset + 2] = currentPos.z
            else:
                self.vertices[offset] = transform.position.x + \
                    (xAdd * transform.scale.x)
                self.vertices[offset+1] = transform.position.y + \
                    (yAdd * transform.scale.y)
                self.vertices[offset+2] = transform.position.z

            self.vertices[offset + 3] = sprite.color.x
            self.vertices[offset + 4] = sprite.color.y
            self.vertices[offset + 5] = sprite.color.z
            self.vertices[offset + 6] = sprite.color.w

            self.vertices[offset + 7] = sprite.sprite.texCoords[i].x
            self.vertices[offset + 8] = sprite.sprite.texCoords[i].y

            self.vertices[offset + 9] = texID

            offset += self.VERTEX_SIZE

    def destroy(self):
        self.mesh.destroy()

    def tryRemove(self, sprite: SpriteRenderer):
        if sprite in self.sprites:
            self.sprites.remove(sprite)
            sprite.entity._renderbatch = None
            for i, sprite in enumerate(self.sprites):
                sprite.entity.dirty = True
                sprite.entity._batchindex = i
            return True
        return False

    def hasRoom(self) -> bool:
        return len(self.sprites) < self.maxSprites

    def hasTextureRoom(self) -> bool:
        return len(self.textures) < self.maxTextures

    def hasTexture(self, texture: Texture) -> bool:
        return texture in self.textures
