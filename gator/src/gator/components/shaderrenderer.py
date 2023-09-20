import glm

from gator.components.component import Component
import gator.components

from gator.resources.assets import Assets
from gator.graphics.shader import Shader

import gator.common.saving as saving
import gator.common.gimgui as gimgui
from gator.common.colors import Colors

class ShaderRenderer(Component):
    hideInProperties = ["col1", "col2", "col3", "col4", "active", "shader"]
    
    def __init__(self, shader=None, id: int = None, active: bool = True):
        super().__init__(id, active)
        
        self.shader: Shader = Assets.getShader("exampleCustom") if not shader else shader
        self.col1: glm.vec4 = Colors.WHITE
        self.col2: glm.vec4 = Colors.WHITE
        self.col3: glm.vec4 = Colors.WHITE
        self.col4: glm.vec4 = Colors.WHITE
        
        self._lastC1: glm.vec4 = glm.vec4(self.col1)
        self._lastC2: glm.vec4 = glm.vec4(self.col2)
        self._lastC3: glm.vec4 = glm.vec4(self.col3)
        self._lastC4: glm.vec4 = glm.vec4(self.col4)
        
        self.icShaderName = self.shader.assetName
        
    def init(self):
        if self.entity.hasComponent(gator.components.spriterenderer.SpriteRenderer):
            self.kill()
        
    def imgui(self):
        self.baseImgui()
        _, self.col1 = gimgui.colorEdit4("Color 1", self.col1)
        _, self.col2 = gimgui.colorEdit4("Color 2", self.col2)
        _, self.col3 = gimgui.colorEdit4("Color 3", self.col3)
        _, self.col4 = gimgui.colorEdit4("Color 4", self.col4)
        changed, self.icShaderName = gimgui.enumDropdown("Shader", list(Assets.shaders.keys()), self.icShaderName)
        if changed:
            self.shader = Assets.getShader(self.icShaderName)
            self.shaderUpdated()
        self.endImgui()
        
    def toFile(self) -> dict:
        base = super().toFile()
        base.update({
            "shader": saving.saveShader(self.shader),
            "col1": saving.saveVec4(self.col1),
            "col2": saving.saveVec4(self.col2),
            "col3": saving.saveVec4(self.col3),
            "col4": saving.saveVec4(self.col4),
        })
        return base
        
    @classmethod
    def fromFile(cls, cData: dict, entity):
        renderer = ShaderRenderer(saving.loadShader(cData["shader"]), cData["id"], cData["active"])
        renderer.col1 = saving.loadVec4(cData["col1"])
        renderer.col2 = saving.loadVec4(cData["col2"])
        renderer.col3 = saving.loadVec4(cData["col3"])
        renderer.col4 = saving.loadVec4(cData["col4"])
        return renderer
        
    def update(self):
        if not self.entity._renderbatch: return
        
        if self.col1 != self._lastC1 or self.col2 != self._lastC2 or self.col3 != self._lastC3 or self.col4 != self._lastC4:
            self.entity.dirty = True
            
            self._lastC1 = glm.vec4(self.col1)
            self._lastC2 = glm.vec4(self.col2)
            self._lastC3 = glm.vec4(self.col3)
            self._lastC4 = glm.vec4(self.col4)
            
        if self.entity.dirty:
            self.entity._renderbatch.loadVertexProperties(
                self.entity._batchindex)
            self.entity.dirty = False
        
    def shaderUpdated(self):
        self.entity.dirty = True
        self.entity._renderbatch.shaderUpdated(self)
        
    def editorUpdate(self):
        self.update()