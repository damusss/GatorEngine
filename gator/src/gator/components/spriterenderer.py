import glm

from gator.components.component import Component

from gator.resources.assets import Assets
from gator.resources.sprite import Sprite

import gator.common.saving as saving
import gator.common.gimgui as gimgui
from gator.common.colors import Colors


class SpriteRenderer(Component):
    hideInProperties: list[str] = ["active", "color", "sprite"]

    def __init__(self, sprite: Sprite = None, color: glm.vec4 = Colors.WHITE, id=None, active=True):
        super().__init__(id, active)
        self.sprite: Sprite = sprite if sprite else Sprite(None)
        self.color: glm.vec4 = color

        self._lastCol: glm.vec4 = self.color.xyzw
        self.icTextureName = self.sprite.texture.assetName if self.sprite.texture else "None"

    def imgui(self):
        self.baseImgui()
        _, self.color = gimgui.colorEdit4("Color", self.color)
        changed, self.icTextureName = gimgui.enumDropdown(
            "Texture Name", ["None"]+list(Assets.textures.keys()), self.icTextureName)
        if changed:
            if self.icTextureName == "None":
                self.sprite.texture = None
            else:
                self.sprite.texture = Assets.getTexture(self.icTextureName)
            self.spriteUpdated()

    def toFile(self):
        base = super().toFile()
        base.update({
            "color": saving.saveVec4(self.color),
            "sprite": saving.saveSprite(self.sprite)
        })
        return base

    @classmethod
    def fromFile(self, cData):
        return SpriteRenderer(saving.loadSprite(cData["sprite"]),
                              saving.loadVec4(cData["color"]),
                              cData["id"], cData["active"])

    def update(self):
        if not self.entity._renderbatch:
            return

        if self.color != self._lastCol:
            self.entity.dirty = True
            self._lastCol = self.color.xyzw

        if self.entity.dirty:
            self.entity._renderbatch.loadVertexProperties(
                self.entity._batchindex)
            self.entity.dirty = False

    def spriteUpdated(self):
        self.entity.dirty = True
        if not self.entity._renderbatch:
            return
        self.entity._renderbatch.spriteUpdated(self)
        
    def editorUpdate(self):
        self.update()
