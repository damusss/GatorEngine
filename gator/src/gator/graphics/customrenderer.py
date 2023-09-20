import gator.common.events as events

from gator.components.shaderrenderer import ShaderRenderer
from gator.components.component import Component

from gator.graphics.mesh import VertexTypes, IndexUIntTypes
from gator.graphics.customrenderbatch import CustomRenderBatch
from gator.graphics.shader import Shader

from gator.resources.assets import Assets
from gator.core.time import Time

class CustomRenderer:
    MAX_BATCH_SIZE: int = 1000
    MAX_TEXTURES: int = 8
    MESH_CONFIG: list[int, str, list[int], bool,
                      list[float] | None, str, list[int]] = []
    
    UNIFORM_LOADERS: dict[str,object] = {}
    
    def __init__(self):
        events.register(events.COMP_ADDED, self.whenCompAdded)
        events.register(events.COMP_REMOVED, self.whenCompRemoved)
        
        CustomRenderer.MESH_CONFIG = [CustomRenderer.MAX_BATCH_SIZE*4,  # vertex amount
                                VertexTypes.FLOAT,  # vertex type
                                [3, 4],  # vertex attrib counts
                                False,  # static draw
                                None,  # vertex data
                                IndexUIntTypes.SHORT,  # index type
                                self.genIndices()  # indice
                                ]

        self.batches: list[CustomRenderBatch] = []
        self.registerUniformLoader("exampleCustom", self.exampleCustomUniformLoader)
            
    @staticmethod
    def exampleCustomUniformLoader(shader: Shader):
        shader.uniform1F("uTime", Time.getTime())
    
    @classmethod
    def registerUniformLoader(cls, shaderName: str, uniformLoaderFunc):
        cls.UNIFORM_LOADERS[shaderName] = uniformLoaderFunc
        
    def render(self):
        for batch in self.batches:
            batch.render()
            
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
        self.addComponent(event.component)
        
    def whenCompRemoved(self, event: events.Event):
        self.removeComponent(event.component)
        
    def removeComponent(self, component:Component):
        if not isinstance(component, ShaderRenderer):
            return
        for batch in self.batches:
            if batch.tryRemove(component):
                break
        
    def addComponent(self, component: Component):
        if not isinstance(component, ShaderRenderer):
            return
        added = False
        for batch in self.batches:
            if batch.hasRoom():
                shader = component.shader
                if (batch.shader is None or batch.shader.assetName == shader.assetName):
                    batch.shader = component.shader
                    batch.add(component)
                    added = True
                    break
        if not added:
            newBatch = CustomRenderBatch(self.MAX_BATCH_SIZE, self.MESH_CONFIG, component.shader)
            newBatch.add(component)
            self.batches.append(newBatch)
