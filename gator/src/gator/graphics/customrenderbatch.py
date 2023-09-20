import glm
import math

from gator.graphics.mesh import IndexedVertexMesh
from gator.graphics.shader import Shader

from gator.core.camera import Camera
from gator.common.singletons import Singletons
from gator.components.shaderrenderer import ShaderRenderer

class CustomRenderBatch:
    VERTEX_SIZE: int = 7
    
    def __init__(self, maxShaderRenderers, meshConfig, shader):
        self.shader: Shader = shader
        self.maxShaderRenderers: int = maxShaderRenderers
        self.meshConfig: list[int, str, list[int], bool,
                              list[float] | None, str, list[int]] = meshConfig
        self.camera: Camera = Singletons.app.scene.camera
        self.shaderRenderers: list[ShaderRenderer] = []
        self.vertices: list[float] = [
            0 for _ in range(self.maxShaderRenderers*4*self.VERTEX_SIZE)]
        self.mesh: IndexedVertexMesh = IndexedVertexMesh(*self.meshConfig)
        self.rebufferData: bool = False
        
    def reset(self):
        self.vertices: list[float] = [0 for i in range(self.maxShaderRenderers*4*self.VERTEX_SIZE)]
        self.shaderRenderers = []
        self.shader = None
        
    def render(self):
        if self.shader is None: return
        
        self.shader.use()
        self.shader.uniformMat4F("uProj", self.camera.proj)
        self.shader.uniformMat4F("uView", self.camera.view)
        if loader:=Singletons.app.scene.customRenderer.UNIFORM_LOADERS.get(self.shader.assetName,None):
            loader(self.shader)

        self.mesh.render(
            (self.vertices if self.rebufferData else None), 0, len(self.shaderRenderers)*6)
        if self.rebufferData:
            self.rebufferData = False
            
        self.shader.detach()
        
    def shaderUpdated(self, shaderRenderer: ShaderRenderer):
        if shaderRenderer.shader is None:
            return
        self.tryRemove(shaderRenderer)
        Singletons.app.scene.customRenderer.addComponent(shaderRenderer)
        
    def add(self, shaderRenderer: ShaderRenderer):
        index = len(self.shaderRenderers)
        self.shaderRenderers.append(shaderRenderer)
        shaderRenderer.entity._renderbatch = self
        shaderRenderer.entity._batchindex = index

        self.loadVertexProperties(index)
        
    def destroy(self):
        self.mesh.destroy()

    def tryRemove(self, shaderRenderer: ShaderRenderer):
        if shaderRenderer in self.shaderRenderers:
            self.shaderRenderers.remove(shaderRenderer)
            shaderRenderer.entity._renderbatch = None
            for i, s in enumerate(self.shaderRenderers):
                s.entity.dirty = True
                s.entity._batchindex = i
            return True
        return False

    def hasRoom(self) -> bool:
        return len(self.shaderRenderers) < self.maxShaderRenderers
    
    def loadVertexProperties(self, index: int):
        self.rebufferData = True
        shaderRenderer = self.shaderRenderers[index]
        transform = shaderRenderer.entity.transform
        offset = index*4*self.VERTEX_SIZE

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
                color = shaderRenderer.col2
            elif i == 2:
                xAdd = -0.5
                color = shaderRenderer.col3
            elif (i == 3):
                yAdd = 0.5
                color = shaderRenderer.col4
            elif i==0:
                color = shaderRenderer.col1
                

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

            self.vertices[offset + 3] = color.x
            self.vertices[offset + 4] = color.y
            self.vertices[offset + 5] = color.z
            self.vertices[offset + 6] = color.w

            offset += self.VERTEX_SIZE