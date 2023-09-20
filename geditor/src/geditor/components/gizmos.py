import glm
import math

from gator.resources.assets import Assets
from gator.graphics.mesh import IndexedVertexMesh, VertexTypes, IndexUIntTypes
from gator.graphics.shader import Shader
from gator.resources.texture import Texture
from gator.resources.sprite import Sprite

from gator.common.singletons import Singletons
from gator.core.mouse import Mouse
from gator.core.keys import Keyboard


class Gizmos:
    INDICES: list[int] = []
    VERTEX_SIZE: int = 9
    TRANSLATE_MODE: int = 1
    SCALE_MODE: int = 2
    ROTATE_MODE: int = 3
    ANY_MODE: int = -1

    def __init__(self):
        self.INDICES = self.genIndices()
        Assets.registerTexture("gizmos", Texture(
            "assets/images/gizmos/gizmos.png"))
        Assets.registerShader("gizmo", Shader.fromFile(
            "assets/shaders/gizmo.glsl"))

        self.gizmoTexture: Texture = Assets.getTexture("gizmos")
        self.shader: Shader = Assets.getShader("gizmo")

        self.gizmoMode: int = 0
        self.hovering: bool = False
        self.mesh: IndexedVertexMesh = IndexedVertexMesh(
            4*5, VertexTypes.FLOAT, [3, 4, 2], False, None, IndexUIntTypes.INT, self.INDICES)
        self.vertices: list[float] = [0 for _ in range(4*5*self.VERTEX_SIZE)]

        self.gizmos: list[GizmoEntity] = [
            GizmoEntity(self.gizmoTexture, "both", self.ANY_MODE),
            GizmoEntity(self.gizmoTexture, "x", self.TRANSLATE_MODE),
            GizmoEntity(self.gizmoTexture, "y", self.TRANSLATE_MODE),
            GizmoEntity(self.gizmoTexture, "x", self.SCALE_MODE),
            GizmoEntity(self.gizmoTexture, "y", self.SCALE_MODE)
        ]

    def setMode(self, mode: int):
        self.gizmoMode = mode

    def genIndices(self) -> list[int]:
        elements = [0 for i in range(6*5)]
        for i in range(5):
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

    def update(self):
        if Keyboard.getKeyDown(Keyboard.keys.KEY_1) or Keyboard.getKeyDown(Keyboard.keys.KEY_ESCAPE):
            self.gizmoMode = 0
        if Keyboard.getKeyDown(Keyboard.keys.KEY_2) or Keyboard.getKeyDown(Keyboard.keys.KEY_W):
            self.gizmoMode = self.TRANSLATE_MODE
        if Keyboard.getKeyDown(Keyboard.keys.KEY_3) or Keyboard.getKeyDown(Keyboard.keys.KEY_S):
            self.gizmoMode = self.SCALE_MODE
        if Keyboard.getKeyDown(Keyboard.keys.KEY_4) or Keyboard.getKeyDown(Keyboard.keys.KEY_R):
            self.gizmoMode = self.ROTATE_MODE

        self.hovering = False
        for i, gizmo in enumerate(self.gizmos):
            gizmo.adjustPos()
            gizmo.checkHovering()
            if (gizmo.mode == self.gizmoMode or gizmo.mode == self.ANY_MODE) and self.gizmoMode != 0:
                if gizmo.hovering:
                    self.hovering = True
            else:
                gizmo.color = glm.vec4(0, 0, 0, 0)
                gizmo.hovering = False
                gizmo.startedHovering = False
            gizmo.processInput()
            gizmo.refreshMesh(i, self.vertices)

    def render(self):
        if self.gizmoMode == 0:
            return
        if Singletons.editor.propertiesTab.selectedEntity is None:
            return

        self.shader.use()
        self.shader.uniformMat4F("uProj", Singletons.app.scene.camera.proj)
        self.shader.uniformMat4F("uView", Singletons.app.scene.camera.view)
        self.shader.uniformIntArray("uTex", 0)
        self.gizmoTexture.bind()

        self.mesh.render(self.vertices, 0, 6*5)

        self.gizmoTexture.unbind()

        self.shader.detach()

    def destroy(self):
        self.mesh.destroy()


class GizmoEntity:
    VERTEX_SIZE: int = 9

    def __init__(self, texture: Texture, axis: str, mode: int):
        self.axis: str = axis
        self.mode: int = mode
        self.position: glm.vec3 = glm.vec3()
        self.scale: glm.vec2 = glm.vec2(0.3, 0.8 if axis != "both" else 0.3)
        self.rotation: float = 90 if axis != "y" else 180
        self.inactiveColor: glm.vec4 = glm.vec4(1, 0, 0, 0.8) if axis == "x" else glm.vec4(
            0, 1, 0, 0.8) if axis == "y" else glm.vec4(0, 0, 1, 0.8)
        self.activeColor: glm.vec4 = glm.vec4(1, 0, 0, 1) if axis == "x" else glm.vec4(
            0, 1, 0, 1) if axis == "y" else glm.vec4(0, 0, 1, 1)
        self.color: glm.vec4 = self.inactiveColor
        self.hovering: bool = False
        self.sprite: Sprite = Sprite(texture)
        self.sprite.calcOffsetSheetCords(
            *((24, 24, 0, 0) if mode == -1 else (24, 48, 24, 0) if mode == 1 else (24, 48, 24*2, 0)))
        self.startedHovering: bool = False

    def adjustPos(self):
        if Singletons.editor.propertiesTab.selectedEntity is None:
            return
        self.position = glm.vec3(
            Singletons.editor.propertiesTab.selectedEntity.transform.position)
        self.position.z = 99
        if self.axis == "x":
            self.position.x += 0.6
        elif self.axis == "y":
            self.position.y += 0.6

    def checkHovering(self):
        if Singletons.editor.propertiesTab.selectedEntity is None:
            return
        self.hovering = Singletons.app.scene.camera.rawRayCast(
            Singletons.editor.gameViewTab.viewportMouseWorldPos, self.position, self.scale, self.rotation)
        if self.hovering:
            self.startedHovering = not any(
                [gizmo.startedHovering and not gizmo is self for gizmo in Singletons.editor.gizmos.gizmos])
        self.color = self.activeColor if self.hovering or self.startedHovering else self.inactiveColor
        if self.startedHovering and not Mouse.getButton(Mouse.buttons.MOUSE_BUTTON_LEFT):
            self.startedHovering = False

    def processInput(self):
        if not self.hovering and not self.startedHovering:
            return
        if not Mouse.getButton(Mouse.buttons.MOUSE_BUTTON_LEFT):
            return
        entity = Singletons.editor.propertiesTab.selectedEntity

        if self.axis == "x":
            if self.mode == Gizmos.TRANSLATE_MODE:
                entity.transform.position.x += Singletons.app.scene.camera.mouseRelWorld.x*1.1
                if Keyboard.getKey(Keyboard.keys.KEY_LEFT_SHIFT):
                    entity.transform.position.x = int(
                        entity.transform.position.x)

            elif self.mode == Gizmos.SCALE_MODE:
                entity.transform.scale.x += Singletons.app.scene.camera.mouseRelWorld.x*1.1
        elif self.axis == "y":
            if self.mode == Gizmos.TRANSLATE_MODE:
                entity.transform.position.y -= Singletons.app.scene.camera.mouseRelWorld.y*1.1
                if Keyboard.getKey(Keyboard.keys.KEY_LEFT_SHIFT):
                    entity.transform.position.y = int(
                        entity.transform.position.y)
            elif self.mode == Gizmos.SCALE_MODE:
                entity.transform.scale.y -= Singletons.app.scene.camera.mouseRelWorld.y*1.1
        elif self.axis == "both":
            if Singletons.editor.gizmos.gizmoMode == Gizmos.TRANSLATE_MODE:
                entity.transform.position.x += Singletons.app.scene.camera.mouseRelWorld.x*1.1
                entity.transform.position.y -= Singletons.app.scene.camera.mouseRelWorld.y*1.1
                if Keyboard.getKey(Keyboard.keys.KEY_LEFT_SHIFT):
                    entity.transform.position.x = int(
                        entity.transform.position.x)
                    entity.transform.position.y = int(
                        entity.transform.position.y)

            elif Singletons.editor.gizmos.gizmoMode == Gizmos.SCALE_MODE:
                entity.transform.scale.x += Singletons.app.scene.camera.mouseRelWorld.x*1.1
                entity.transform.scale.y -= Singletons.app.scene.camera.mouseRelWorld.y*1.1
                if Keyboard.getKey(Keyboard.keys.KEY_LEFT_SHIFT):
                    entity.transform.scale.y = entity.transform.scale.x

            elif Singletons.editor.gizmos.gizmoMode == Gizmos.ROTATE_MODE:
                entity.transform.rotation -= Singletons.app.scene.camera.mouseRelWorld.x*20

    def refreshMesh(self, i, vertices):
        offset = i*4*self.VERTEX_SIZE
        rotated = self.rotation != 0.0
        if rotated:
            transformMatrix = glm.identity(glm.mat4x4)
            transformMatrix = glm.translate(
                transformMatrix, self.position)
            transformMatrix = glm.rotate(transformMatrix, float(
                math.radians(self.rotation)), glm.vec3(0, 0, 1))
            transformMatrix = glm.scale(transformMatrix, glm.vec3(
                self.scale.x, self.scale.y, 1))

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
                vertices[offset] = currentPos.x
                vertices[offset + 1] = currentPos.y
                vertices[offset + 2] = 99
            else:
                vertices[offset] = self.position.x + \
                    (xAdd * self.scale.x)
                vertices[offset+1] = self.position.y + \
                    (yAdd * self.scale.y)
                vertices[offset+2] = 99

            vertices[offset + 3] = self.color.x
            vertices[offset + 4] = self.color.y
            vertices[offset + 5] = self.color.z
            vertices[offset + 6] = self.color.w

            vertices[offset + 7] = self.sprite.texCoords[i].x
            vertices[offset + 8] = self.sprite.texCoords[i].y

            offset += self.VERTEX_SIZE
