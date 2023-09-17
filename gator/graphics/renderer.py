import common.events as events
from gator.components.spriterenderer import SpriteRenderer

from gator.graphics.mesh import VertexTypes, IndexUIntTypes
from gator.graphics.renderbatch import RenderBatch
from gator.graphics.shader import Shader


class Renderer:
    MAX_BATCH_SIZE: int = 1000
    MAX_TEXTURES: int = 8
    MESH_CONFIG: list[int, str, list[int], bool,
                      list[float] | None, str, list[int]] = []

    def __init__(self):
        events.register(events.COMP_ADDED, self.whenCompAdded)
        events.register(events.COMP_REMOVED, self.whenCompRemoved)

        Renderer.MESH_CONFIG = [Renderer.MAX_BATCH_SIZE*4,  # vertex amount
                                VertexTypes.FLOAT,  # vertex type
                                [3, 4, 2, 1],  # vertex attrib counts
                                True,  # static draw
                                None,  # vertex data
                                IndexUIntTypes.SHORT,  # index type
                                self.genIndices()  # indice
                                ]

        self.batches: list[RenderBatch] = []
        self.currentShader: Shader = None

    def render(self, shader: Shader):
        self.currentShader = shader
        self.currentShader.use()
        for batch in self.batches:
            batch.render(self.currentShader)
        self.currentShader.detach()

    def genIndices(self) -> list[int]:
        elements = [0 for i in range(6*self.MAX_BATCH_SIZE)]
        for i in range(self.MAX_BATCH_SIZE):
            self.loadElementIndices(elements, i)

        return elements

    def loadElementIndices(self, elements: list[int], index: int):
        offsetArrayIndex = 6 * index
        offset = 4 * index
        # 3, 2, 0, 0, 2, 1        7, 6, 4, 4, 6, 5
        elements[offsetArrayIndex] = offset + 3
        elements[offsetArrayIndex + 1] = offset + 2
        elements[offsetArrayIndex + 2] = offset + 0

        elements[offsetArrayIndex + 3] = offset + 0
        elements[offsetArrayIndex + 4] = offset + 2
        elements[offsetArrayIndex + 5] = offset + 1

    def destroy(self):
        for batch in self.batches:
            batch.destroy()

    def whenCompAdded(self, event: events.Event):
        if event.component.__class__ is not SpriteRenderer:
            return
        added = False
        for batch in self.batches:
            if batch.hasRoom():
                tex = event.component.sprite.texture
                if (tex is None or (batch.hasTexture(tex) and batch.hasTextureRoom())):
                    batch.add(event.component)
                    added = True
                    break
        if not added:
            newBatch = RenderBatch(self.MAX_BATCH_SIZE,
                                   self.MAX_TEXTURES, self.MESH_CONFIG)
            newBatch.add(event.component)
            self.batches.append(newBatch)

    def whenCompRemoved(self, event: events.Event):
        if event.component is not SpriteRenderer:
            return
        for batch in self.batches:
            if batch.tryRemove(event.component):
                break
