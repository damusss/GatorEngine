import glm

from gator.components.component import Component
import gator.components

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
        self.geIsSpritesheet = False
        self.geIsGrid = True
        self.geSpriteWidth = 10
        self.geSpriteHeight = 10
        self.geSpriteIndex = 0
        self.geSpriteOffsetX = 0
        self.geSpriteOffsetY = 0
    
    def init(self):
        if self.entity.hasComponent(gator.components.shaderrenderer.ShaderRenderer):
            self.kill()

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
        changedIS, self.geIsSpritesheet = gimgui.checkbox("Is Spritesheet", self.geIsSpritesheet)
        if self.geIsSpritesheet:
            changedIG, self.geIsGrid = gimgui.checkbox("Grid Sheet", self.geIsGrid)
            changedSW, self.geSpriteWidth = gimgui.dragInt("Sprite Width", self.geSpriteWidth)
            changedSH, self.geSpriteHeight = gimgui.dragInt("Sprite Height", self.geSpriteHeight)
            if self.geIsGrid:
                changedSI, self.geSpriteIndex = gimgui.inputInt("Sprite Index", self.geSpriteIndex)
                changedSOX = changedSOY = False
            else:
                changedSI = False
                changedSOX, self.geSpriteOffsetX = gimgui.dragInt("Offset X", self.geSpriteOffsetX)
                changedSOY, self.geSpriteOffsetY = gimgui.dragInt("Offset Y", self.geSpriteOffsetY)
            if changedIS or changedSW or changedSH or changedSI or changedSOX or changedSOY or changedIG:
                self.spriteUpdated()
        else:
            if changedIS: self.spriteUpdated()
        
        self.endImgui()
        
    def updateGridSheet(self, spriteWidth, spriteHeight, spriteIndex):
        self.geSpriteWidth, self.geSpriteHeight, self.geSpriteIndex = spriteWidth, spriteHeight, spriteIndex
        self.spriteUpdated()
        
    def updateOffsetSheet(self, spriteWidth, spriteHeight, offsetX, offsetY):
        self.geSpriteWidth, self.geSpriteHeight, self.geSpriteOffsetX, self.geSpriteOffsetY = spriteWidth, spriteHeight, offsetX, offsetY
        self.spriteUpdated()

    def toFile(self):
        base = super().toFile()
        base.update({
            "color": saving.saveVec4(self.color),
            "sprite": saving.saveSprite(self.sprite),
            "isSheet": self.geIsSpritesheet,
            "isGrid": self.geIsGrid,
            "sWidth": self.geSpriteWidth,
            "sHeight": self.geSpriteHeight,
            "sIndex": self.geSpriteIndex,
            "offsetX": self.geSpriteOffsetX,
            "offsetY": self.geSpriteOffsetY,
        })
        return base

    @classmethod
    def fromFile(self, cData, entity):
        sprite = SpriteRenderer(saving.loadSprite(cData["sprite"]),
                              saving.loadVec4(cData["color"]),
                              cData["id"], cData["active"])
        sprite.geIsSpritesheet = cData["isSheet"]
        sprite.geSpriteWidth = cData["sWidth"]
        sprite.geSpriteHeight = cData["sHeight"]
        sprite.geSpriteIndex = cData["sIndex"]
        sprite.geIsGrid = cData["isGrid"]
        sprite.geSpriteOffsetX = cData["offsetX"]
        sprite.geSpriteOffsetY = cData["offsetY"]
        sprite.entity = entity
        sprite.spriteUpdated()
        return sprite

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
        if self.geIsSpritesheet:
            if self.geSpriteWidth <= 0: self.geSpriteWidth = 1
            if self.geSpriteHeight <= 0: self.geSpriteHeight = 1
            if self.geSpriteIndex < 0: self.geSpriteIndex = 0
            if self.geIsGrid:
                self.sprite.calcGridSheetCords(self.geSpriteWidth, self.geSpriteHeight, self.geSpriteIndex)
            else:
                self.sprite.calcOffsetSheetCords(self.geSpriteWidth, self.geSpriteHeight, self.geSpriteOffsetX, self.geSpriteOffsetY)
        else:
            self.sprite.texCoords = self.sprite.DEFAULT_TEX_COORDS
        if not self.entity._renderbatch:
            return
        self.entity._renderbatch.spriteUpdated(self)
        
    def editorUpdate(self):
        self.update()
