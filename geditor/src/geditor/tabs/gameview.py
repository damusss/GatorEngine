import imgui
import glm

from gator.common.singletons import Singletons
from gator.core.mouse import Mouse
from gator.common.settings import WINDOW_FLAGS, COLUMN_DIVIDER
from gator.common.gimgui import Tracker


class GameViewTab:
    def __init__(self, playFunc, stopFunc):
        self.hovered: bool = False
        self.viewportW = self.viewportH = self.posX = self.posY = self.viewportX = self.viewportY = 0
        self.viewportMousePos, self.viewportMouseWorldPos = glm.vec2(), glm.vec2()
        self.playFunc = playFunc
        self.stopFunc = stopFunc

    def imgui(self):
        imgui.set_next_window_position(Singletons.app.window._width//COLUMN_DIVIDER, Tracker.menuBarH*2)
        imgui.set_next_window_size(Singletons.app.window._width-(Singletons.app.window._width//COLUMN_DIVIDER),
                                   Singletons.app.window._height-(Tracker.menuBarH*2))
        imgui.begin("Game##GameViewWindowTab", False, imgui.WINDOW_MENU_BAR |
                    imgui.WINDOW_NO_SCROLL_WITH_MOUSE | imgui.WINDOW_NO_SCROLLBAR | WINDOW_FLAGS)
        if imgui.begin_menu_bar():
            if imgui.button("Play"):
                    self.playFunc()
            if imgui.button("Stop"):
                self.stopFunc()
            if Singletons.editor.playing:
                imgui.text("Playing")
            imgui.end_menu_bar()

        self.viewportX, self.viewportY = imgui.get_window_position()
        self.viewportW, self.viewportH = self.getSize()
        self.posX, self.posY = self.getPos(self.viewportW, self.viewportH)
        imgui.set_cursor_pos((self.posX, self.posY))

        imgui.image(Singletons.editor.framebuffer.texture.ID,
                    self.viewportW, self.viewportH, (0, 1), (1, 0))
        self.hovered = imgui.is_item_hovered()

        imgui.end()

        self.viewportMousePos = glm.vec2(((Mouse.mousePos.x-self.posX-self.viewportX)/self.viewportW)*Singletons.app.window._width,
                                         ((1-(Mouse.mousePos.y-self.posY-self.viewportY)+self.viewportH)/self.viewportH)*Singletons.app.window._height)
        pos = Singletons.app.scene.camera.position
        self.viewportMouseWorldPos = Singletons.app.scene.camera.screenToWorld(glm.vec3(
            self.viewportMousePos.x, self.viewportMousePos.y, 0))

    def getSize(self) -> tuple[int, int]:
        availW, availH = imgui.get_content_region_available()
        aspectW = availW
        aspectH = availW/Singletons.app.window.targetAspectRatio
        if aspectH > availH:
            aspectH = availH
            aspectW = aspectH*Singletons.app.window.targetAspectRatio
        return aspectW, aspectH

    def getPos(self, aspectW: int, aspectH: int) -> tuple[int, int]:
        availW, availH = imgui.get_content_region_available()

        viewportX = (availW/2)-(aspectW/2)
        viewportY = (availH/2)-(aspectH/2)
        return (viewportX+imgui.get_cursor_pos_x()), (viewportY+imgui.get_cursor_pos_y()-Tracker.menuBarH)
